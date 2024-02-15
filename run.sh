#!/bin/bash

tmux new-session -d -s llava_session 'cd quantization/executables && ./llava.llamafile -m ../models/Publisher/Repository/model_tuned_q8_0.gguf'

sleep 5

docker-compose up --build