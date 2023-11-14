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
import random
from typing import List, Optional, Tuple

from xllm import dist_logger
from xllm import enums as xllm_enums
from xllm.datasets.base import BaseDataset
from xllm.types import RawSample

from wgpt import enums
from wgpt.core.config import WGPTConfig


class DescriptionToJsonDataset(BaseDataset):
    @classmethod
    def get_data(cls, config: WGPTConfig) -> Optional[Tuple[List[RawSample], Optional[List[RawSample]]]]:
        data = list()

        with open(config.path_to_raw_train_file) as file_object:
            for line in file_object:
                sample = json.loads(line)
                data.append(sample)

        if config.shuffle:
            random.shuffle(data)

        train_data = data[config.max_eval_samples:]
        eval_data = data[: config.max_eval_samples]

        dist_logger(f"Train data length: {len(train_data)}")
        dist_logger(f"Eval data length: {len(eval_data)}")

        return train_data, eval_data

    def get_sample(self, index: int) -> RawSample:
        sample = self.data[index]

        description = sample.get(enums.Field.description)
        json_string = json.dumps(sample.get(enums.Field.data))

        sample = {xllm_enums.General.text_parts: [description, json_string + "\n"]}

        return sample
