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

from dataclasses import dataclass, field

from xllm import Config


@dataclass
class WGPTConfig(Config):
    path_to_raw_train_file: str = field(
        default="./data/train.jsonl",
        metadata={"help": "Path to raw train file"},
    )
    path_to_raw_test_file: str = field(
        default="./data/test.jsonl",
        metadata={"help": "Path to raw train file"},
    )