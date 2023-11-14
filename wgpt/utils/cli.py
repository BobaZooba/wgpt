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

import os
from typing import Optional

import openai
from dotenv import load_dotenv
from loguru import logger

from wgpt import enums


def setup_cli(env_file_path: Optional[str] = None) -> None:
    load_dotenv(dotenv_path=env_file_path)
    logger.info(".env loaded")
    if enums.EnvironmentVariable.openai_api_key in os.environ:
        openai.api_key = os.environ[enums.EnvironmentVariable.openai_api_key]
