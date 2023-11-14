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

from typing import Optional

import fire
from loguru import logger

from wgpt.data.generate import DataGenerationEngine
from wgpt.openai.client import GPTClient
from wgpt.utils.cli import setup_cli


def generate(
        data_file_path: str = "./data/train.jsonl",
        fails_file_path: str = "./data/fails.jsonl",
        num_samples: int = 500,
        num_samples_per_batch: int = 3,
        num_batches_per_request: int = 3,
        num_rounds_per_call: int = 3,
        min_examples: int = 3,
        max_examples: int = 5,
        temperature: float = 1.0,
        max_tokens: int = 8192,
        top_p: float = 0.99,
        data_file_mode: str = "w",
        env_file_path: Optional[str] = "./.env",
) -> None:
    setup_cli(env_file_path=env_file_path)
    gpt_client = GPTClient(
        num_completion=num_batches_per_request,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
    )
    logger.info("GPTClient built")
    data_generation_engine = DataGenerationEngine(
        num_samples_per_batch=num_samples_per_batch,
        min_examples=min_examples,
        max_examples=max_examples,
    )
    logger.info("DataGenerationEngine built")
    data_generation_engine.generate_data(
        gpt_client=gpt_client,
        data_file_path=data_file_path,
        data_file_mode=data_file_mode,
        fails_file_path=fails_file_path,
        num_samples=num_samples,
        num_rounds_per_call=num_rounds_per_call,
    )
    logger.info("Generation complete")


if __name__ == "__main__":
    fire.Fire(generate)
