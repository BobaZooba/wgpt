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

from dataclasses import dataclass


@dataclass
class Field:
    role: str = "role"
    content: str = "content"

    description: str = "description"
    data: str = "data"


@dataclass
class GPTRole:
    system: str = "system"
    assistant: str = "assistant"
    user: str = "user"


@dataclass
class EnvironmentVariable:
    openai_api_key: str = "OPENAI_API_KEY"

# @dataclass
# class Rating:
#     correct: str = "correct"
#     minor_inaccuracies: str = "minor inaccuracies"
#     incorrect: str = "incorrect"
