#!/bin/bash

tmux new-session -d -s llava_session 'cd quantization && ./llava.llamafile -m ./merged_adapters/ggml-model-q8_0.gguf'

sleep 5

sudo docker-compose up --build