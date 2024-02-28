# Kwaai PAI Assistant - Prerequisites

This document outlines the prerequisites, installation, and configuration steps required to run the project. The project involves merging LLaMA 2 7B model with fine-tuning checkpoints, quantizing the merged model in GGUF format, and setting up a REST server for AI model inferences.

## Prerequisites

Before starting, ensure your system meets the following requirements:

### Python 3

- **Description**: Python 3 is required to run the merge scripts for the LLaMA 2 7B model and fine-tuning checkpoints.
- **Installation**:
  - **Windows**: Download and install from the [official Python website](https://www.python.org/downloads/).
  - **MacOS/Linux**: Python 3 is often pre-installed. If not, use Homebrew on MacOS or the package manager for your Linux distribution.

### Make

- **Description**: Make tool is required to execute the Makefile scripts for model quantization and other setup processes.
- **Installation**:
  - **Windows**: Install via [Chocolatey](https://chocolatey.org/) (`choco install make`).
  - **MacOS**: Install using Homebrew (`brew install make`).
  - **Linux**: Install using the package manager (e.g., `sudo apt-get install build-essential` for Ubuntu/Debian).

### Docker and Docker-Compose

- **Description**: Docker is needed to run the AI assistant in a containerized environment, and docker-compose is required for orchestrating multiple containers.
- **Installation**:
  - All platforms can download Docker Desktop or appropriate Docker Engine and docker-compose from the [official Docker website](https://www.docker.com/get-started).

### tmux

- **Description**: tmux is used for managing terminal sessions, helpful for long-running processes.
- **Installation**:
  - **Windows**: Use within WSL (Windows Subsystem for Linux) for a Linux-like environment.
  - **MacOS/Linux**: Install using Homebrew (MacOS) or the package manager for your Linux distribution.

## Configuration

After installing the prerequisites, follow these steps for each tool and technology:

1. **Python 3**: Verify installation by running `python3 --version`. Ensure it's Python 3.6 or higher.
2. **Make**: Check by typing `make -v` in your terminal. Make sure it's installed correctly.
3. **Docker and Docker-Compose**: After installation, verify by running `docker --version` and `docker-compose --version`. Ensure Docker can run without sudo by adding your user to the `docker` group (Linux).
4. **tmux**: Verify its installation by running `tmux -V`.


## Operating System Considerations

- **Windows Users**: It's recommended to use WSL for a better compatibility with Linux-based tools and scripts. Docker Desktop for Windows supports WSL 2 backend, which integrates smoothly with Linux containers.
- **MacOS and Linux Users**: No specific considerations beyond the provided installation instructions. Docker and tmux should work natively without significant issues.

By following these prerequisites and setup instructions, you'll prepare your environment for running and managing the project efficiently across different operating systems.
