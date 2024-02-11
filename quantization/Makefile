LLAMA_CPP_PATH=llama.cpp
MERGED_ADAPTERS_PATH=merged_adapters
MODEL_GGUF_TUNED_PATH=models/Publisher/Repository/model_tuned_q8_0.gguf
LLAMAFILE_REPOSITORY_PATH=llamafile

all: run-merge-models \
	run-create-gguf-folders \
    run-quantize-llama-model

run-merge-models:
	python3 merge_model.py

run-create-gguf-folders:
	mkdir -p models/Publisher/Repository

run-quantize-llama-model:
	cd $(LLAMA_CPP_PATH) && \
	python3 convert.py ../$(MERGED_ADAPTERS_PATH) --outfile ../$(MODEL_GGUF_TUNED_PATH) --outtype q8_0