# Copyright 2023 Boris Zubarev. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import concurrent
import json
import os
import random
from concurrent.futures import ThreadPoolExecutor
from typing import IO, Any, Dict, List, Optional

from loguru import logger
from tqdm import tqdm

from wgpt import enums
from wgpt.core.examples import EXAMPLES
from wgpt.core.prompts import GENERERATE_DATA_PROMPT
from wgpt.openai.client import GPTClient


class DataGenerationEngine:
    def __init__(
            self,
            num_samples_per_batch: int = 50,
            min_examples: int = 2,
            max_examples: int = 5,
            input_placeholder: str = "Input:",
            examples_separator: str = "\n\n",
    ):
        assert min_examples >= 2

        self.num_samples_per_batch = num_samples_per_batch
        self.min_examples = min_examples
        self.max_examples = max_examples
        self.input_placeholder = input_placeholder
        self.examples_separator = examples_separator

        self._file: Optional[IO[Any]] = None
        self._fails_file: Optional[IO[Any]] = None
        self._progress_bar: Optional[tqdm] = None
        self._counter = 0
        self._fails_counter = 0
        self._batch_separator_fails_counter = 0

    def format_examples_prompt(self, examples: List[str]) -> str:
        text_parts = ["Examples:"] + [f"{n}. {text}" for n, text in enumerate(examples)]
        text = "\n" + self.examples_separator.join(text_parts) + "\n"
        return text

    def format_generate_batch_prompt(self) -> str:
        num_examples = random.randint(self.min_examples, self.max_examples)

        examples = random.sample(EXAMPLES, num_examples)
        examples_prompt = self.format_examples_prompt(examples=examples)

        prompt = GENERERATE_DATA_PROMPT.format(examples_prompt=examples_prompt, num_samples=self.num_samples_per_batch)
        return prompt

    def parse_generated_sample(self, sample: str) -> Dict[str, str]:
        input_text, output_text = sample.split("\n")
        weather_description = input_text[input_text.find(self.input_placeholder) + len(self.input_placeholder) + 1:]
        weather_data = json.loads(output_text[output_text.find("{"):])
        parsed_sample = {
            enums.Field.description: weather_description,
            enums.Field.data: weather_data,
        }
        return parsed_sample

    def save_parsed_sample(self, sample: Dict[str, str]) -> None:
        if self._file is None:
            raise ValueError("File is not open")

        self._file.write(json.dumps(sample) + "\n")
        self._counter += 1

        if self._progress_bar is not None:
            self._progress_bar.update()

    def parse_generated_data(self, generated_data: List[str]) -> None:
        for raw_generated_batch in generated_data:
            if self.examples_separator in raw_generated_batch:
                # Yes, we drop gpt response if there's something wrong with them. Rare situation (I hope)
                generated_batch = raw_generated_batch.split(self.examples_separator)
                for generated_sample in generated_batch:
                    try:
                        parsed_sample = self.parse_generated_sample(generated_sample)
                        self.save_parsed_sample(sample=parsed_sample)
                    except Exception as exception:
                        self._fails_counter += 1
                        if self._fails_file is not None:
                            self._fails_file.write(json.dumps({"failed": generated_sample}) + "\n")
                        logger.error(f"Exception cathed: {exception}")
            else:
                self._batch_separator_fails_counter += 1

    def generate_batch(self, gpt_client: GPTClient, num_rounds: int = 1) -> None:
        prompt = self.format_generate_batch_prompt()
        generated_data = list()
        with ThreadPoolExecutor(max_workers=num_rounds) as executor:
            futures = {executor.submit(gpt_client.one_turn_generation, prompt) for i in range(num_rounds)}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                generated_data.extend(result)
        self.parse_generated_data(generated_data=generated_data)

    def _build(self, data_file_path: str, fails_file_path: str, num_samples: int, data_file_mode: str = "w") -> None:
        self._file = open(data_file_path, mode=data_file_mode)
        self._fails_file = open(fails_file_path, mode="w")
        self._progress_bar = tqdm(total=num_samples, desc="Generating data")
        self._counter = 0
        self._fails_counter = 0
        self._batch_separator_fails_counter = 0

    def generate_data(
            self,
            gpt_client: GPTClient,
            data_file_path: str,
            fails_file_path: str,
            data_file_mode: str = "w",
            num_samples: int = 5_000,
            num_rounds_per_call: int = 4,
    ) -> None:
        self._build(
            data_file_path=data_file_path,
            fails_file_path=fails_file_path,
            data_file_mode=data_file_mode,
            num_samples=num_samples,
        )

        global_batch_size = gpt_client.num_completion * num_rounds_per_call * self.num_samples_per_batch

        logger.info(
            f"Start data generation. Required num samples: {num_samples}. Global batch size: {global_batch_size}"
        )

        while True:
            self.generate_batch(gpt_client=gpt_client, num_rounds=num_rounds_per_call)
            num_sample_left = num_samples - self._counter
            num_sample_left = num_sample_left if num_sample_left >= 0 else 0
            logger.info(f"Generation round complete. Generated data: {self._counter}. Left: {num_sample_left}")
            if self._counter >= num_samples:
                break

        if self._file is not None:
            self._file.close()

        if self._fails_file is not None:
            self._fails_file.close()

        logger.info("Data generation complete")

        if self._fails_counter > 0:
            fails_fraction = self._fails_counter * 100 / (self._fails_counter + self._counter)
            logger.warning(f"Num fails: {fails_fraction:.2f} % - {self._fails_counter}")
        else:
            os.remove(fails_file_path)

        if self._batch_separator_fails_counter > 0:
            logger.warning(f"Batch separator num fails: {self._batch_separator_fails_counter}")
