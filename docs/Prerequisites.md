# Prerequisites - Installation - Configuration.

This document explains the setup script designed to prepare and start the project environment. The script automates the installation of Python dependencies, initializes a tmux session for running a specific task, and sets up Docker containers as defined in the project's `docker-compose.yml`.

## Script Overview

The script performs the following actions in order:

1. Creates a new detached tmux session named `llava_session`.
2. Within this tmux session, changes the directory to `quantization/` and executes a file named `llava.llamafile` with specific parameters.
3. Waits for 5 seconds to ensure the command has been executed properly.
4. Executes `docker-compose up --build` to build and start the Docker containers as per the configuration in `docker-compose.yml`.


# Dockerfile Documentation

This Dockerfile creates a Docker image based on Python 3.9 with additional libraries and configurations suitable for running a Django application that utilizes Hugging Face transformers and TensorFlow. It is tailored for both development and production environments with an emphasis on AI and machine learning projects.

## Base Image

```Dockerfile
FROM python:3.9-buster
```
The image is based on Python 3.9 running on Debian Buster, providing a stable and well-supported environment for Python applications.

## Maintainer Label

```Dockerfile
LABEL maintainer="Kwaai - AI Lab"
```
Identifies the maintainer of the Dockerfile, useful for tracking ownership and responsibility within projects or organizations.

## Environment Variables

```Dockerfile
ENV PYTHONUNBUFFERED 1
ENV HF_HOME /home/django-user/.cache/huggingface/hub
ENV TRANSFORMERS_CACHE /home/django-user/.cache/huggingface/transformers
```
- `PYTHONUNBUFFERED`: Ensures that Python output is sent straight to terminal (i.e., container logs) without being first buffered, which is useful for logging and debugging in Docker environments.
- `HF_HOME` and `TRANSFORMERS_CACHE`: Set the cache directories for Hugging Face models and transformers, optimizing performance and reducing redundant downloads.

## Copying Requirements

```Dockerfile
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
```
Copies the production and development requirement files into the temporary directory of the container.

## Application Directory Setup

```Dockerfile
COPY ./app /app
WORKDIR /app
COPY ./scripts /scripts
EXPOSE 8000
```
- Copies the application code and scripts into the container.
- Sets the working directory to `/app`.
- Exposes port `8000` for the application.

## Development Environment Argument

```Dockerfile
ARG DEV=true
```
Defines an argument `DEV` that determines whether the image is built for development (`true`) or production (`false`). This affects the installation of additional development dependencies.

## System Dependencies Installation

```Dockerfile
RUN apt-get update && \
    apt-get install -y libffi-dev libjpeg-dev libstdc++-8-dev libstdc++6 \
                       build-essential libpq-dev zlib1g-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*
```
Installs necessary system libraries and tools required for the application and its dependencies, including database and image processing libraries.

## Python Environment Setup

```Dockerfile
RUN python -m venv /py && \
    /py/bin/python -m ensurepip && \
    /py/bin/pip install --upgrade pip
```
Creates a Python virtual environment in `/py`, ensuring pip is installed and up-to-date.

## PyTorch and TensorFlow Installation

```Dockerfile
RUN /py/bin/pip install --no-cache-dir torch torchvision -f https://download.pytorch.org/whl/cu111/torch_stable.html
RUN /py/bin/pip install --no-cache-dir tensorflow
```
Installs PyTorch, torchvision, and TensorFlow without using the cache to ensure the latest versions are installed. PyTorch installation is specifically targeted for CUDA 11.1 compatible systems.

## Python Dependencies Installation

```Dockerfile
RUN /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi
```
Installs Python dependencies from `requirements.txt` for all environments and additionally from `requirements.dev.txt` if the build is for development.

## User and Permissions Setup

```Dockerfile
RUN adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media /vol/web/static /vol/temp && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts
```
Creates a non-root user `django-user` for running the application, sets up necessary volumes for media and static files, and adjusts permissions for runtime efficiency and security.

## Final Environment Setup

```Dockerfile
ENV PATH="/scripts:/py/bin:$PATH"
USER django-user
CMD ["run.sh"]
```
- Updates the `PATH` environment variable to include the Python virtual environment and scripts directory.
- Switches to the `django-user` to run the application.
- Specifies the default command to run the application using `run.sh` script.