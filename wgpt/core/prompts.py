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

GENERERATE_DATA_PROMPT = """Your task is to create diverse examples where a free-form description of weather is translated into a JSON file format.

Each description should be between 2 to 5 sentences long with as much diversity as possible. Feel free to omit some fields, add new information, or write in a variety of styles.

The JSON format requires the following fields: weather (str), temperature (int), wind_speed (float), humidity (float), precipitation (str), visibility (str), air_quality (str), and real_feel_temperature (int). If any value is unknown, use null.

The "temperature" and "real_feel_temperature" should be in degrees, wind_speed should be in kilometers per hour, and "humidity" is in percentage. The fields "weather", "precipitation", "visibility" should be single word descriptions.

The format of your answer should be:

1. Input: ...
Output: ...
2. Input: ...
Output: ...
{examples_prompt}
You need to create a dataset where plain text weather descriptions are converted into valid JSON files. Provide {num_samples} diverse samples similar to the example given."""

LABELING_PROMPT = """Your task is to validate whether the model has correctly parsed the weather description into JSON. The model was given a free-form weather description in natural language. Its task was to transform this description into valid JSON. Your job: understand whether the model has correctly parsed what was stated in the text, whether it correctly filled in the fields, with the correct values.

The JSON format requires the following fields: weather (str), temperature (int), wind_speed (float), humidity (float), precipitation (str), visibility (str), air_quality (str), and real_feel_temperature (int). If any value is unknown, use null.

The "temperature" and "real_feel_temperature" should be in degrees, wind_speed should be in kilometers per hour, and "humidity" is in percentage. The fields "weather", "precipitation", "visibility" should be single word descriptions.

Weather description: {weather_description}

Model response: {model_response}

Ground truth: {ground_truth}

You need to consider whether the model has parsed the answer correctly and give your assessment. The rating options can only be: correct, minor inaccuracies, incorrect.

Format of your answer.
Reasoning: ...
Assessment: ..."""

ASSISTANT_PROMPT = "You are helpful assistant for data generation"
