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

import json
from typing import Optional

import fire
from loguru import logger

from wgpt.eval.labeling import Labeler
from wgpt.eval.parse import parse_accuracy
from wgpt.eval.wrapper import WGPTWrapper
from wgpt.openai.client import GPTClient
from wgpt.utils.cli import setup_cli


def evaluation(path_to_data: str, model_name_or_path: str, env_file_path: Optional[str] = "./.env") -> None:
    setup_cli(env_file_path=env_file_path)

    data = list()

    with open(path_to_data) as file_object:
        for line in file_object:
            data.append(json.loads(line))

    logger.info(f"Data size: {len(data)}")

    wrapper = WGPTWrapper(model_name_or_path=model_name_or_path)
    gpt_client = GPTClient(num_completion=1)
    labeler = Labeler(wrapper=wrapper, gpt_client=gpt_client)
    generated_json_strings, assessments = labeler.run(data=data)
    parse_accuracy_value, _, _ = parse_accuracy(json_strings=generated_json_strings)
    logger.info(f"Parse accuracy value: {parse_accuracy_value:.2f}")


if __name__ == "__main__":
    fire.Fire(evaluation)
