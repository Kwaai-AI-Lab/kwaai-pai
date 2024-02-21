LLAMA_CPP_PATH=llama.cpp
MERGED_ADAPTERS_PATH=merged_adapters
MODEL_GGUF_TUNED_PATH=models/Publisher/Repository/model_tuned_q8_0.gguf
LLAMAFILE_REPOSITORY_PATH=llamafile

all: run-install-python-dependencies \
	run-download-llamafile \
	run-clone-repositories \
	run-merge-models \
	run-create-gguf-folders \
    run-quantize-llama-model

run-install-python-dependencies:
	cd .. && \
	pip3 install -r requirements.local.txt

run-download-llamafile:
	wget https://huggingface.co/jartine/llava-v1.5-7B-GGUF/resolve/main/llava-v1.5-7b-q4.llamafile?download=true && \
	mv llava-v1.5-7b-q4.llamafile?download=true llava.llamafile

run-clone-repositories:
	git clone https://github.com/ggerganov/llama.cpp.git && \
	git clone https://github.com/Mozilla-Ocho/llamafile.git

run-merge-models:
	python3 merge_model.py


run-create-gguf-folders:
	mkdir -p models/Publisher/Repository

run-quantize-llama-model:
	cd $(LLAMA_CPP_PATH) && \
	python3 convert.py ../$(MERGED_ADAPTERS_PATH) --outfile ../$(MODEL_GGUF_TUNED_PATH) --outtype q8_0