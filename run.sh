#!/bin/bash

tmux new-session -d -s llava_session 'cd quantization/executables && ./llava.llamafile'

sleep 5

docker-compose up --build