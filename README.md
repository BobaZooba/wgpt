# WeatherGPT: Generate valid JSON from weather descriptions

This repository features an example of how to utilize the `xllm` library. Included is a solution for a common type of
assessment given to LLM engineers. The work, which took 6-7 hours to complete, is representative of actual tasks in the field.

[<img src="https://github.com/BobaZooba/xllm/blob/main/static/images/xllm-badge.png" alt="Powered by X—LLM" width="175" height="32"/>](https://github.com/BobaZooba/xllm)

# Task

Convert weather description to valid JSON using LLM

### Example

**Description:** Today will be mostly sunny with temperatures reaching 25 degrees. There will be a strong wind blowing
at 30 km/h. Humidity levels are unknown and there is no precipitation expected.

**JSON**

```json
{
  "weather": "sunny",
  "temperature": 25,
  "wind_speed": 30.0,
  "humidity": null,
  "precipitation": null,
  "visibility": "good",
  "air_quality": null,
  "real_feel_temperature": null
}
```

# Installation

Run in terminal:

```bash
pip install -e .
```

## Environment

Python3.8+, CUDA 11.8

**Suggested docker:** huggingface/transformers-pytorch-gpu:latest

All entry points at **Makefile**

# Implementation

- Generate data
  - ChatGPT with few-shot variable examples
- Train model
  - QLoRA
  - DeepSpeed Stage 2
  - 4 bit quantization
  - Gradient checkpointing
  - Mistal AI 7B
- Evaluate
  - Output can be parsed
  - ChatGPT labeling

# Reproduce

1. Install requirements

```sh
make install
```

2. Make **.env** and fill it with your values (please take a look at _.env.template_)

3. _[Optional]_ Generate data

```sh
make generate-data
```

Also example data is provided in _data_ folder

4. Prepare data and model

```sh
make prepare
```

5. Train the model

```sh
make train
```

Or train with DeepSpeed (if you have multiple GPUs, please specify `CUDA_VISIBLE_DEVICES` to use only one)

```sh
make train-deepspeed
```

6. Fuse LoRA weights

```sh
make fuse
```

7. Evaluate

```sh
make evaluate
```

# Data generation

### Why generated?

- ChatGPT was chosen for data collection because I couldn't find similar datasets and because this method scales to
  other domains and many companies will need to do this in one way or another
- Previously, NLP engineers suffered from the lack of datasets, but now they can be generated and this will serve as a
  great starting point for problem-solving
- The cost of compiling the initial dataset has decreased from thousands of dollars to a few bucks

## Prompt

Please also check `wgpt/core/prompts.py`

### Example

```txt
Your task is to create diverse examples where a free-form description of weather is translated into a JSON file format.
Each description should be between 2 to 5 sentences long with as much diversity as possible. Feel free to omit some fields, add new information, or write in a variety of styles.
The JSON format requires the following fields: weather (str), temperature (int), wind_speed (float), humidity (float), precipitation (str), visibility (str), air_quality (str), and real_feel_temperature (int). If any value is unknown, use null.
The "temperature" and "real_feel_temperature" should be in degrees, wind_speed should be in kilometers per hour, and "humidity" is in percentage. The fields "weather", "precipitation", "visibility" should be single word descriptions.
The format of your answer should be: 1. Input: ...
Output: ...
2. Input: ...
Output: ...
Examples:
1. Input: The skies are clear with a temperature of about 25 degrees. The wind is blowing gently at around 7kph. Visibility is high and the air is quite dry with a humidity around 30%. There's no precipitation. Feels like it's exactly 25 degrees. The air quality is very good today.
Output: {"weather": "clear", "temperature": 25, "wind_speed": 7.0, "humidity": 30.0, "precipitation": "none", "visibility": "high", "air_quality": "good", "real_feel_temperature": 25}
2. Input: It's snowing outside and the temperature is -5 degrees. There's a strong wind blowing at 25kph. Visibility is very low because of the snow. Humidity is around 80%. Air quality is moderate today. The real feel is much lower at -10 degrees due to wind chill.
Output: {"weather": "snow", "temperature": -5, "wind_speed": 25.0, "humidity": 80.0, "precipitation": "snow", "visibility": "low", "air_quality": "moderate", "real_feel_temperature": -10}
3. Input: Expect a cloudy evening with a temperature of about 18 degrees. There is a slight chance of light showers, and the wind is gentle at 5 km/h.
Output: {"weather": "cloudy", "temperature": 18, "wind_speed": 5.0, "humidity": null, "precipitation": "light", "visibility": "good", "air_quality": null, "real_feel_temperature": null}
You need to create a dataset where plain text weather descriptions are converted into valid JSON files. Provide {num_samples} diverse samples similar to the example given.
```

<details>
  <summary>Detailed explanation</summary>

#### Task

  ```txt
  Your task is to create diverse examples where a free-form description of weather is translated into a JSON file format.
  ```

#### Description requirements

  ```txt
  Each description should be between 2 to 5 sentences long with as much diversity as possible. Feel free to omit some fields, add new information, or write in a variety of styles.
  ```

#### JSON and fields requirements

  ```txt
  The JSON format requires the following fields: weather (str), temperature (int), wind_speed (float), humidity (float), precipitation (str), visibility (str), air_quality (str), and real_feel_temperature (int). If any value is unknown, use null.

  The "temperature" and "real_feel_temperature" should be in degrees, wind_speed should be in kilometers per hour, and "humidity" is in percentage. The fields "weather", "precipitation", "visibility" should be single word descriptions.
```

#### Format of response

```txt
  The format of your answer should be:
  1. Input: ...
  Output: ...
  2. Input: ...
  Output: ...
  ```

#### Few-shot examples

Randomly selected from 3 to 5 of the pre-prepared. It is necessary to provide variety and explain the task.

  ```txt
  Examples:
1. Input: The skies are clear with a temperature of about 25 degrees. The wind is blowing gently at around 7kph. Visibility is high and the air is quite dry with a humidity around 30%. There's no precipitation. Feels like it's exactly 25 degrees. The air quality is very good today.
Output: {"weather": "clear", "temperature": 25, "wind_speed": 7.0, "humidity": 30.0, "precipitation": "none", "visibility": "high", "air_quality": "good", "real_feel_temperature": 25}
2. Input: It's snowing outside and the temperature is -5 degrees. There's a strong wind blowing at 25kph. Visibility is very low because of the snow. Humidity is around 80%. Air quality is moderate today. The real feel is much lower at -10 degrees due to wind chill.
Output: {"weather": "snow", "temperature": -5, "wind_speed": 25.0, "humidity": 80.0, "precipitation": "snow", "visibility": "low", "air_quality": "moderate", "real_feel_temperature": -10}
3. Input: Expect a cloudy evening with a temperature of about 18 degrees. There is a slight chance of light showers, and the wind is gentle at 5 km/h.
Output: {"weather": "cloudy", "temperature": 18, "wind_speed": 5.0, "humidity": null, "precipitation": "light", "visibility": "good", "air_quality": null, "real_feel_temperature": null}
  ```

#### Direct call to action

Also, indicating the number of desired examples

  ```txt
  You need to create a dataset where plain text weather descriptions are converted into valid JSON files. Provide {num_samples} diverse samples similar to the example given.
  ```

</details>

### Example of output

```txt
1. Input: The sun is shining brightly with a temperature reaching a scorching 38 degrees. There is a moderate breeze blowing at a speed of 15kph. Visibility is clear with no obstructions. Humidity is quite low at around 20%. No precipitation is expected. The real feel temperature is similar to the actual temperature.
Output: {"weather": "sunny", "temperature": 38, "wind_speed": 15.0, "humidity": 20.0, "precipitation": "none", "visibility": "clear", "air_quality": null, "real_feel_temperature": 38}
2. Input: It's a hot and humid day with a temperature of 32 degrees. There is no wind present and the air is quite heavy. Visibility is reduced due to haze. Humidity is extremely high at around 90%. No precipitation is predicted. The real feel temperature is slightly higher at 34 degrees.
Output: {"weather": null, "temperature": 32, "wind_speed": null, "humidity": 90.0, "precipitation": null, "visibility": "reduced", "air_quality": null, "real_feel_temperature": 34}
3. Input: The weather today is cloudy with a temperature of 22 degrees. A light breeze is blowing at 10kph. Visibility is good and there is no precipitation expected. Humidity is moderate at around 50%. The real feel temperature is the same as the actual temperature.
Output: {"weather": "cloudy", "temperature": 22, "wind_speed": 10.0, "humidity": 50.0, "precipitation": "none", "visibility": "good", "air_quality": null, "real_feel_temperature": 22}
4. Input: It's a gloomy day with overcast skies. The temperature is a chilly 8 degrees. Strong winds are howling at 40kph. Visibility is reduced due to fog. Humidity is high at 85%. Light rain is expected. The real feel temperature is lower at 5 degrees due to wind chill.
Output: {"weather": "overcast", "temperature": 8, "wind_speed": 40.0, "humidity": 85.0, "precipitation": "rain", "visibility": "reduced", "air_quality": null, "real_feel_temperature": 5}
5. Input: Enjoy a beautiful spring day with clear blue skies and a temperature of 20 degrees. A gentle breeze is rustling the leaves at 12kph. Visibility is excellent with no obstructions. Humidity is moderate at 55%. No precipitation is expected. The real feel temperature matches the actual temperature.
Output: {"weather": "clear", "temperature": 20, "wind_speed": 12.0, "humidity": 55.0, "precipitation": "none", "visibility": "excellent", "air_quality": null, "real_feel_temperature": 20}
```

## Results of data generation

- There were 5848 examples generated for training (including the validation set), which took about 10 minutes
- The ChatGPT model was used because it is 30 times cheaper and much faster. In real projects, I would use ChatGPT,
  GPT4, as well as open models, to obtain as diverse a dataset as possible
- The examples turned out to be quite lively and met the requirements of the task

# Training

- Model: [Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1)
- Boilerplate (QLoRA, DeepSpeed Stage 2, 4 bit quantization, Gradient
  checkpointing): [xllm](https://github.com/BobaZooba/xllm)

`xllm` is a user-friendly library that streamlines training optimization, so you can focus on enhancing your models and
data. Equipped with cutting-edge training techniques, `xllm` is engineered for efficiency by engineers who understand
your needs.

[<img src="https://github.com/BobaZooba/xllm/blob/main/static/images/xllm-badge.png" alt="Powered by X—LLM" width="175" height="32"/>](https://github.com/BobaZooba/xllm)

### Methods

- **QLoRA (and 4 bit bnb quantization)**. The preferred method of fine-tuning, as it usually ensures a higher quality
  than full fine-tuning due to effective management of catastrophic forgetting. And of course, it optimizes the memory
  utilized during training
  - I use LoRA for all linear layers except lm_head and embeddings
    - The original paper does not investigate which layers are better to apply. Please
      check [AdaLoRA paper](https://arxiv.org/pdf/2303.10512.pdf)
  - I also use a fairly high rank for low-rank optimization: 64 (alpha is 32)
- **DeepSpeed Stage 2 (with CPU offloading)**. I'm using Deepspeed for training on multiple GPUs. Stage 2 was used
  because there are observed issues with the use of Stage 3 and quantized models
- **Gradient Checkpointing**. Very strong optimization of used memory at the expense of slowing down training

### `xllm` details

In the xllm library, there are several important steps: prepare, train, fuse, quantize

- **Prepare**. The data preprocessing and model download step has been separated to avoid doing it on each of the
  processes in distributed learning mode
- **Train**. Training the model and saving checkpoints. I save checkpoints in HuggingFace Hub. Since I am training
  through LoRA, those weights are specifically saved.
- **Fuse**. Fusing LoRA weights with the backbone model and push it to HF Hub
- _[Optional]_ **Quantize**. GPTQ quantization of the model

### Task details

I only calculated the loss for the json part, didn't calculate it for the description

<img src="https://github.com/BobaZooba/wgpt/blob/main/images/completion_scheme.jpg" alt="Completion scheme"/>

### Results of the training

- [LoRA weights](https://huggingface.co/BobaZooba/WGPT-LoRA)
- [Fused model](https://huggingface.co/BobaZooba/WGPT)
- [W&B link](https://api.wandb.ai/links/bobazooba/8v7pqflf)

<img src="https://github.com/BobaZooba/wgpt/blob/main/images/loss_curve.jpg" alt="Loss curve"/>

# Evaluation

## Metrics

### Why no BLEU / ROUGE / etc?

I have been evaluating generative models for several years and believe that currently using n-gram methods to evaluate
generative models is an extremely poor practice. BertScore is also not a sufficiently good method. Currently, there are
only two good ways to evaluate generative models: human evaluation and emulation of human evaluation (GPT-like
instructional models and training of rankers/classifiers on human evaluations).

### Output can be parsed

Simple proxy metric: we try to parse the model's response. We calculate the percentage of responses that we were able to
parse

### ChatGPT labeling

Emulation of human assessment. ChatGPT is given an instruction and the output of my model. ChatGPT must provide one of
several responses: the correct answer, there are minor inaccuracies, incorrect answer. In real projects, I would use
only GPT-4, but it is too expensive.

#### ChatGPT labeling instruction

```txt
Your task is to validate whether the model has correctly parsed the weather description into JSON. The model was given a free-form weather description in natural language. Its task was to transform this description into valid JSON. Your job: understand whether the model has correctly parsed what was stated in the text, whether it correctly filled in the fields, with the correct values.
The JSON format requires the following fields: weather (str), temperature (int), wind_speed (float), humidity (float), precipitation (str), visibility (str), air_quality (str), and real_feel_temperature (int). If any value is unknown, use null.
The "temperature" and "real_feel_temperature" should be in degrees, wind_speed should be in kilometers per hour, and "humidity" is in percentage. The fields "weather", "precipitation", "visibility" should be single word descriptions.
Weather description: {weather_description}
Model response: {model_response}
Ground truth: {ground_truth}
You need to consider whether the model has parsed the answer correctly and give your assessment. The rating options can only be: correct, minor inaccuracies, incorrect.
Format of your answer.
Reasoning: ...
Assessment: ...
```

## Results

Output can be parsed: **100%**

### ChatGPT labeling

| Correct | Minor inaccuracies | Incorrect |
|---------|--------------------|-----------|
| 48%     | 51%                | 1%        |

# Future works

- Improve evaluation
  - Need to add a method that compares the JSON response with the generated JSON. We know the types of fields. For
    numeric fields, you should use MSE, and for text fields, you should use the proximity of text embeddings, having
    previously selected the model
- If the quality of the current model is satisfactory, it should be deployed into production (in a quantized version)
  using TGI at least for a limited number of users.
- It is crucial to gather real data from production to fine-tune the model. Then these data need to be labeled, train a
  discriminator model (which would assess the quality of responses), filter the data and further train the model. For
  this task, I wouldn't apply RL, only the ReST ([link](It is crucial to gather real data from production to fine-tune
  the model. Then these data need to be labeled, train a discriminator model (which would assess the quality of
  responses), filter the data and further train the model. For this task, I wouldn't apply RL, only the ReST (link)
  method, which I would improve. Such actions on labeling and further training should be performed regularly. Ideally,
  an infrastructure for constant retraining should be developed. The recommended frequency depends on the traffic
  volumes. Usually, for manual re-learning the frequency is monthly, for automatic – weekly. Also, because we apply
  labeling, we can track model improvements. This will be particularly useful when the labeling instruction is
  stabilized. With the help of the discriminator we can adjust the hyperparameters for training and inference, for
  example, generation parameters. Also, with the discriminator, we can immediately assess several hypotheses from the
  generative model and deliver only the best one to the user. Currently, this method is not widely used due to the
  significantly increasing load on the generative model, so I would focus on the further training of the generative
  model using the discriminator.)) method, which I would improve. Such actions on labeling and further training should
  be performed regularly. Ideally, an infrastructure for constant retraining should be developed. The recommended
  frequency depends on the traffic volumes. Usually, for manual re-learning the frequency is monthly, for automatic –
  weekly. Also, because we apply labeling, we can track model improvements. This will be particularly useful when the
  labeling instruction is stabilized. With the help of the discriminator we can adjust the hyperparameters for training
  and inference, for example, generation parameters. Also, with the discriminator, we can immediately assess several
  hypotheses from the generative model and deliver only the best one to the user. Currently, this method is not widely
  used due to the significantly increasing load on the generative model, so I would focus on the further training of the
  generative model using the discriminator.
- If the quality of the current model is not satisfactory, similar steps will need to be taken with synthetic data,
  deploy it into production, and then perform the same steps with the data from production.

# Useful materials

- [X—LLM Repo](https://github.com/BobaZooba/xllm): main repo of the `xllm` library
- [Quickstart](https://github.com/BobaZooba/xllm#quickstart-): basics of `xllm`
- [Examples](https://github.com/BobaZooba/xllm/examples): minimal examples of using `xllm`
- [Guide](https://github.com/BobaZooba/xllm/blob/main/GUIDE.md): here, we go into detail about everything the library
  can
  do
- [Demo project](https://github.com/BobaZooba/xllm-demo): here's a minimal step-by-step example of how to use X—LLM and
  fit it
  into your own project
- [WeatherGPT](https://github.com/BobaZooba/wgpt): this repository features an example of how to utilize the xllm
  library. Included is a solution for a common type of assessment given to LLM engineers, who typically earn between
  $120,000 to $140,000 annually
- [Shurale](https://github.com/BobaZooba/shurale): project with the finetuned 7B Mistal model

## Tale Quest

`Tale Quest` is my personal project which was built using `xllm` and `Shurale`. It's an interactive text-based game
in `Telegram` with dynamic AI characters, offering infinite scenarios

You will get into exciting journeys and complete fascinating quests. Chat
with `George Orwell`, `Tech Entrepreneur`, `Young Wizard`, `Noir Detective`, `Femme Fatale` and many more

Try it now: [https://t.me/talequestbot](https://t.me/TaleQuestBot?start=Z2g)
