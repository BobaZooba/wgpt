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
import random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple

from loguru import logger

from wgpt import enums
from wgpt.core.prompts import LABELING_PROMPT
from wgpt.openai.client import GPTClient

from .wrapper import WGPTWrapper


class Labeler:
    def __init__(
            self,
            wrapper: WGPTWrapper,
            gpt_client: GPTClient,
            num_requests: int = 8,
            assessment_placeholder: str = "Assessment:",
    ):
        self.wrapper = wrapper
        self.gpt_client = gpt_client
        self.num_requests = num_requests
        self.assessment_placeholder = assessment_placeholder

    def format_prompt(self, weather_description: str, generated_json_string: str, true_json_string: str) -> str:
        prompt = LABELING_PROMPT.format(
            weather_description=weather_description,
            model_response=generated_json_string,
            ground_truth=true_json_string,
        )
        return prompt

    def label_batch(self, prompts: List[str]) -> List[str]:
        generated_data = list()
        with ThreadPoolExecutor(max_workers=self.num_requests) as executor:
            futures = {executor.submit(self.gpt_client.one_turn_generation, prompt) for prompt in prompts}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                generated_data.extend(result)
        return generated_data

    def parse_assessment(self, text: str) -> str:
        if self.assessment_placeholder in text:
            text = text[text.find(self.assessment_placeholder) + len(self.assessment_placeholder):]
        text = text.lower().split()[0]
        return text

    def run(self, data: List[Dict[str, str]]) -> Tuple[List[str], List[str]]:
        weather_descriptions = list()
        true_json_strings = list()

        for sample in data:
            weather_descriptions.append(sample.get(enums.Field.description) + "\n")
            true_json_strings.append(json.dumps(sample.get(enums.Field.data)))

        generated_json_strings = self.wrapper.generate(texts=weather_descriptions)

        samples_to_show = random.sample(generated_json_strings, 3)

        for sample_to_show in samples_to_show:
            logger.info(f"Generated: {sample_to_show}")

        assert len(generated_json_strings) == len(weather_descriptions) == len(true_json_strings)

        prompts = list()

        for sample_index in range(len(weather_descriptions)):
            sample_prompt = self.format_prompt(
                weather_description=weather_descriptions[sample_index],
                generated_json_string=generated_json_strings[sample_index],
                true_json_string=true_json_strings[sample_index],
            )
            prompts.append(sample_prompt)

        raw_assessments = self.label_batch(prompts=prompts)

        assessments = [self.parse_assessment(assessment) for assessment in raw_assessments]

        counter = Counter(assessments)

        num_elements = len(assessments)

        for key, value in counter.items():
            fraction = value / num_elements
            logger.info(f"{key}: {fraction:.2f}")

        return generated_json_strings, assessments
