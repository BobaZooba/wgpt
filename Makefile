.DEFAULT_GOAL:=help

.EXPORT_ALL_VARIABLES:

ifndef VERBOSE
.SILENT:
endif

#* Variables
PYTHON := python3
PYTHON_RUN := $(PYTHON) -m
ENV_FILE := ./.env

DATASET_KEY := desc2json
COLLATOR_KEY := completion
MODEL_NAME_OR_PATH := mistralai/Mistral-7B-v0.1
USE_FLASH_ATTENTION_2 := False  # For mistral

TRAIN_DATA_SAMPLES := 5000
TEST_DATA_SAMPLES := 150

TRAIN_DATA_FILE_PATH := ./data/train.jsonl
TEST_DATA_FILE_PATH := ./data/test.jsonl

LORA_HUB_MODEL_ID := BobaZooba/WGPT-LoRA
HUB_MODEL_ID := BobaZooba/WGPT
GPTQ_HUB_MODEL_ID := BobaZooba/WGPT-GPTQ

NUM_GPUS := 2

FUSED_MODEL_LOCAL_PATH := ./fused_model/

EVAL_LOCAL_PATH_TO_DATA := ./eval.jsonl

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

#* Installation
.PHONY: install-xllm-source
install-xllm-source:  ## Production installation
	$(PYTHON_RUN) pip install git+https://github.com/BobaZooba/xllm

.PHONY: install
install:  ## Production installation
	$(PYTHON_RUN) pip install .

.PHONY: dev-install
dev-install:  ## Development installation
	make install
	$(PYTHON_RUN) pip install -r requirements-dev.txt
	$(PYTHON_RUN) pip install -e .
	
.PHONY: train-install
train-install:  ## Development installation
	$(PYTHON_RUN) pip install -r requirements-train.txt
	$(PYTHON_RUN) pip install .

.PHONY: pre-commit-install
pre-commit-install:  ## Install Pre-Commit Hooks
	pre-commit install

#* Generate data
.PHONY: generate-train-data
generate-train-data:  ## Run train data
	$(PYTHON) wgpt/cli/run_generate_data.py \
		--num_samples=$(TRAIN_DATA_SAMPLES) \
		--num_samples_per_batch=5 \
		--num_rounds_per_call=8 \
		--data_file_path=$(TRAIN_DATA_FILE_PATH) \
		--fails_file_path=./train_fails.jsonl

.PHONY: generate-test-data
generate-test-data:  ## Run test data
	$(PYTHON) wgpt/cli/run_generate_data.py \
		--num_samples=$(TEST_DATA_SAMPLES) \
		--num_samples_per_batch=5 \
		--num_rounds_per_call=8 \
		--data_file_path=$(TEST_DATA_FILE_PATH) \
		--fails_file_path=./data/test_fails.jsonl

.PHONY: generate-data
generate-data:  ## Run data
	make generate-train-data
	make generate-test-data

#* Run
.PHONY: prepare
prepare:  ## Run prepare
	$(PYTHON) wgpt/cli/run_prepare.py \
	  --dataset_key $(DATASET_KEY) \
	  --model_name_or_path $(MODEL_NAME_OR_PATH) \
	  --path_to_raw_train_file $(TRAIN_DATA_FILE_PATH) \
	  --path_to_raw_train_file $(TRAIN_DATA_FILE_PATH) \
	  --eval_local_path_to_data $(EVAL_LOCAL_PATH_TO_DATA) \
	  --do_eval True \
	  --max_eval_samples 100 \
	  --path_to_env_file ./.env

.PHONY: train
train:  ## Run train
	$(PYTHON) wgpt/cli/run_train.py \
	  --dataset_key $(DATASET_KEY) \
	  --collator_key $(COLLATOR_KEY) \
	  --eval_local_path_to_data $(EVAL_LOCAL_PATH_TO_DATA) \
	  --use_gradient_checkpointing True \
	  --deepspeed_stage 0 \
	  --stabilize True \
	  --model_name_or_path $(MODEL_NAME_OR_PATH) \
	  --use_flash_attention_2 $(USE_FLASH_ATTENTION_2) \
	  --load_in_4bit True \
	  --apply_lora True \
	  --raw_lora_target_modules all \
	  --per_device_train_batch_size 8 \
	  --gradient_accumulation_steps 4 \
	  --warmup_steps 100 \
	  --save_total_limit 0 \
	  --push_to_hub True \
	  --hub_model_id $(LORA_HUB_MODEL_ID) \
	  --hub_private_repo False \
	  --report_to_wandb True \
	  --logging_steps 1 \
	  --num_train_epochs 3 \
	  --save_steps 300 \
	  --save_safetensors True \
	  --use_gradient_checkpointing True \
	  --max_length 2048 \
	  --prepare_model_for_kbit_training True \
	  --label_smoothing_factor 0.1 \
	  --path_to_env_file ./.env

.PHONY: train-deepspeed
train-deepspeed:  ## Run train using deepspeed
	deepspeed --num_gpus=$(NUM_GPUS) wgpt/cli/run_train.py \
	  --dataset_key $(DATASET_KEY) \
	  --collator_key $(COLLATOR_KEY) \
	  --eval_local_path_to_data $(EVAL_LOCAL_PATH_TO_DATA) \
	  --do_eval True \
	  --use_gradient_checkpointing True \
	  --deepspeed_stage 2 \
	  --stabilize True \
	  --model_name_or_path $(MODEL_NAME_OR_PATH) \
	  --use_flash_attention_2 $(USE_FLASH_ATTENTION_2) \
	  --load_in_4bit True \
	  --apply_lora True \
	  --raw_lora_target_modules all \
	  --per_device_train_batch_size 8 \
	  --gradient_accumulation_steps 2 \
	  --warmup_steps 100 \
	  --eval_steps 300 \
	  --save_total_limit 0 \
	  --push_to_hub True \
	  --hub_model_id $(LORA_HUB_MODEL_ID) \
	  --hub_private_repo False \
	  --report_to_wandb True \
	  --logging_steps 1 \
	  --num_train_epochs 5 \
	  --save_steps 300 \
	  --save_safetensors True \
	  --use_gradient_checkpointing True \
	  --max_length 2048 \
	  --prepare_model_for_kbit_training True \
	  --label_smoothing_factor 0.1 \
	  --path_to_env_file ./.env

.PHONY: fuse
fuse:  ## Run fuse
	$(PYTHON) wgpt/cli/run_fuse.py \
	  --model_name_or_path $(MODEL_NAME_OR_PATH) \
	  --lora_hub_model_id $(LORA_HUB_MODEL_ID) \
	  --hub_model_id $(HUB_MODEL_ID) \
	  --hub_private_repo False \
	  --force_fp16 True \
	  --fused_model_local_path $(FUSED_MODEL_LOCAL_PATH) \
	  --max_shard_size 1GB \
	  --push_to_hub True \
	  --path_to_env_file ./.env

.PHONY: quantize
quantize:  ## Run GPTQ quantization
	$(PYTHON) wgpt/cli/run_quantize.py \
	  --dataset_key $(DATASET_KEY) \
	  --collator_key $(COLLATOR_KEY) \
	  --model_name_or_path $(FUSED_MODEL_LOCAL_PATH) \
	  --apply_lora False \
	  --stabilize False \
	  --quantization_max_samples 64 \
	  --quantized_model_path ./quantized_model/ \
	  --prepare_model_for_kbit_training False \
	  --quantized_hub_model_id $(GPTQ_HUB_MODEL_ID) \
	  --quantized_hub_private_repo False \
	  --path_to_env_file ./.env

.PHONY: run-all
run-all:  ## Run all
	make prepare
	make train
	make fuse
	make quantize

.PHONY: run-all-deepspeed
run-all-deepspeed:  ## Run all using deepspeed
	make prepare
	make train-deepspeed
	make fuse
	make quantize

.PHONY: eval
eval:  ## Run test data
	$(PYTHON) wgpt/cli/run_eval.py \
		--path_to_data=$(TEST_DATA_FILE_PATH) \
		--model_name_or_path=$(FUSED_MODEL_LOCAL_PATH)

#* Formatters
.PHONY: codestyle
codestyle:  ## Apply codestyle (black, ruff)
	$(PYTHON_RUN) black --config pyproject.toml .
	$(PYTHON_RUN) ruff check . --fix --preview

.PHONY: check-black
check-black:  ## Check black
	$(PYTHON_RUN) black --diff --check --config pyproject.toml src/xllm

.PHONY: check-ruff
check-ruff:  ## Check ruff
	$(PYTHON_RUN) ruff check src/xllm --preview

.PHONY: check-codestyle
check-codestyle:  ## Check codestyle
	make check-black
	make check-ruff

#* Linting
.PHONY: mypy
mypy:  ## Run static code analyzer
	$(PYTHON_RUN) mypy --config-file pyproject.toml ./wgpt
