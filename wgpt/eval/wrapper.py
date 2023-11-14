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

from typing import List

from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, BatchEncoding
from xllm import Config


class WGPTWrapper:
    def __init__(
            self,
            model_name_or_path: str,
            batch_size: int = 16,
            max_length: int = 512,
            max_new_tokens: int = 128,
            cuda_index: int = 0,
            eos_token: str = "\n",
    ):
        self.batch_size = batch_size
        self.max_length = max_length
        self.max_new_tokens = max_new_tokens
        self.cuda_index = cuda_index
        self.eos_token = eos_token

        model_config = Config()

        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            torch_dtype=model_config.dtype,
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.to(self.device)

    @property
    def device(self) -> str:
        return f"cuda:{self.cuda_index}"

    def tokenize(self, texts: List[str]) -> BatchEncoding:
        tokenized = self.tokenizer(
            texts, return_tensors="pt", padding=True, truncation=True, max_length=self.max_length
        )
        tokenized = tokenized.to(f"cuda:{self.cuda_index}")
        return tokenized

    def post_processing(self, text: str) -> str:
        if "{" in text:
            text = text[text.index("{"):]

        if "}" in text:
            text = text[: text.index("}") + 1]

        return text

    def generate(self, texts: List[str]) -> List[str]:
        generated_indices = list()

        for batch_start in tqdm(range(0, len(texts), self.batch_size), desc="Generating"):
            batch = texts[batch_start: batch_start + self.batch_size]
            batch_tokenized = self.tokenize(texts=batch)
            batch_generated_indices = self.model.generate(**batch_tokenized, max_new_tokens=self.max_new_tokens).cpu()
            generated_indices.extend(batch_generated_indices)

        generated_texts: List[str] = self.tokenizer.batch_decode(generated_indices)

        generated_texts = [self.post_processing(text=text) for text in generated_texts]

        return generated_texts
