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
from typing import List, Tuple


def parse_accuracy(json_strings: List[str]) -> Tuple[float, int, int]:
    correct_responses = 0
    incorrect_responses = 0

    for json_string in json_strings:
        try:
            json.loads(json_string)
            correct_responses += 1
        except Exception:
            incorrect_responses += 1

    correct_fraction = correct_responses / (correct_responses + incorrect_responses)

    return correct_fraction, correct_responses, incorrect_responses
