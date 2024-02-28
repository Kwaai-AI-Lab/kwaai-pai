# Quantize Llama2 7B model -> 8bits

This document provides an overview of the steps involved in running the Makefile for setting up and processing a LLaMA model with custom adaptations and quantization. The Makefile consists of several targets, each responsible for a specific part of the setup and execution process.
This process 

## Targets Overview

- **all**: This is the default target, which orchestrates the entire process by calling other targets in the correct sequence.
- **run-install-python-dependencies**: Installs Python dependencies required for the project.
- **run-download-llamafile**: Downloads the LLaMA model file from Hugging Face.
- **run-clone-repositories**: Clones necessary GitHub repositories for the model setup and processing.
- **run-merge-models**: Merges model adapters or modifications into the base LLaMA model.
- **run-quantize-llama-model**: Quantizes the LLaMA model for optimized performance.

### run-install-python-dependencies

The `run-install-python-dependencies` target in the Makefile installs the necessary Python packages for the project. These dependencies are listed in the `requirements.local.txt` file and are crucial for ensuring that all scripts and operations run smoothly. Below are the dependencies specified in `requirements.local.txt`:

- `torch>=1.8.0`: PyTorch is an open-source machine learning library used for applications such as computer vision and natural language processing, specified to be at least version 1.8.0.
- `transformers>=4.0.0`: The Hugging Face's Transformers library provides thousands of pre-trained models to perform tasks on texts such as classification, information extraction, and more, with a minimum version requirement of 4.0.0.
- `peft`: This package is likely a project-specific or less commonly known dependency, which could be used for performance enhancements or task-specific functionalities.
- `sentencepiece`: A library for unsupervised text tokenization and detokenization mainly used for neural network models in natural language processing (NLP), without specifying a minimum version, indicating that the latest version available will be installed.

These dependencies are essential for the project's Python environment, enabling the processing and handling of LLaMA models, among other functionalities. Ensure that your Python environment is properly set up and that these packages are installed to avoid runtime issues.


### run-download-llamafile

This target is responsible for downloading a specific LLaMA model file from Hugging Face, which is instrumental in setting up a REST server for model inference. The downloaded file enables the deployment of a server on port 8080, facilitating the consumption of the merged LLaMA 2 model. This model incorporates fine-tuning checkpoints, allowing for inference in GGUF format. The process involves:

- Downloading the LLaMA model file using `wget` from the specified Hugging Face URL.
- Renaming the downloaded file to `llava.llamafile` for consistent reference within the project's infrastructure.

The establishment of the REST server through this downloaded file is a critical step for enabling model inference capabilities, making it easier for developers and systems to leverage the power of the LLaMA 2 model merged with specific fine-tuning adjustments. This setup facilitates a seamless integration and utilization of the model for various NLP tasks, ensuring efficient and effective inference performance.


### run-clone-repositories

This target is crucial for setting up the infrastructure needed to quantize and run inferences on the LLaMA model. It involves cloning two specific repositories: `llama.cpp` and `llamafile`. Each plays a distinct role in the process:

- **llama.cpp**: This repository contains tools and scripts essential for quantizing the merged LLaMA 2 model. Quantization is a process that converts the model from a standard floating-point format to a more compact 8-bit integer format, reducing the model's size and computational demands while maintaining inference accuracy. In this project, `llama.cpp` is used specifically to quantize the merged LLaMA 2 7B model, preparing it for efficient execution.

- **llamafile**: After quantization, the `llamafile` repository comes into play for running inferences on the quantized model. It provides the necessary infrastructure to interact with the GGUF-adapted, 8-bit quantized LLaMA model, facilitating seamless model inference. This tool is integral for leveraging the quantized model's capabilities, allowing for efficient and effective natural language processing tasks.

Cloning these repositories ensures that all necessary components are in place for the subsequent steps of model preparation and utilization. `llama.cpp` sets the stage for model optimization through quantization, while `llamafile` enables the practical application of the optimized model in real-world scenarios.


### run-merge-models

This target handles the integration of fine-tuning checkpoints with the base LLaMA 2 7B model. It executes a Python script designed to merge these components into a cohesive, enhanced model. To ensure this process is executed correctly, it is imperative to follow these preparation steps:

- **Checkpoint Placement**: Before running this script, you must place the checkpoint file you intend to merge into the `quantization/checkpoints` directory. This checkpoint should represent the fine-tuning adjustments made to the LLaMA 2 7B model. Proper placement is crucial for the script to locate and integrate the checkpoint correctly.

- **Checkpoint Selection**: It is recommended to merge only one checkpoint at a time. This checkpoint should be the result of a fine-tuning process on the LLaMA 2 7B model. Merging multiple checkpoints simultaneously is not advised, as it could complicate the model's structure and potentially degrade performance. Select the most effective checkpoint that embodies the desired enhancements or optimizations for your specific application.

By adhering to these guidelines, you ensure that the `run-merge-models` target can effectively combine the selected fine-tuning checkpoint with the base model. This step is critical for customizing the LLaMA model to suit specific needs or improve its performance on particular tasks. After merging, the model is prepared for quantization and further processing.



### run-quantize-llama-model

Quantizes the merged LLaMA model to a specific format (`q8_0`), optimizing it for performance on certain hardware. This step involves changing to the `llama.cpp` directory and executing the conversion script with the appropriate parameters.

## Execution

To run the entire process, simply execute the `make` command without any arguments. This will trigger the `all` target, which in turn calls the other targets in the specified order.