# Setup Script Documentation

This document explains the setup script designed to prepare and start the project environment. The script automates the installation of Python dependencies, initializes a tmux session for running a specific task, and sets up Docker containers as defined in the project's `docker-compose.yml`.

## Script Overview

The script performs the following actions in order:

1. Installs Python dependencies from the `requirements.local.txt` file.
2. Creates a new detached tmux session named `llava_session`.
3. Within this tmux session, changes the directory to `quantization/executables` and executes a file named `llava.llamafile` with specific parameters.
4. Waits for 5 seconds to ensure the command has been executed properly.
5. Executes `docker-compose up --build` to build and start the Docker containers as per the configuration in `docker-compose.yml`.

## How to Use the Script

1. **Ensure the Script is Accessible**: Save the script in a file, for example, `setup.sh`, within the root directory of your project.

2. **Make the Script Executable**: Change the script's permissions to make it executable. Open a terminal and run:

   ```bash
   chmod +x setup.sh
   ```

3. **Run the Script**: Execute the script by running:

   ```bash
   ./setup.sh
   ```

## Detailed Steps

### Step 1: Create a tmux Session

```bash
tmux new-session -d -s llava_session 'cd quantization/executables && ./llava.llamafile -m ../models/Publisher/Repository/model_tuned_q8_0.gguf'
```

A new tmux session named `llava_session` is created and detached. It navigates to the `quantization/executables` directory and executes the `llava.llamafile` with a model as its parameter.

### Step 3: Wait for Execution

```bash
sleep 5
```

The script pauses for 5 seconds to ensure the previous command has time to execute properly.

### Step 4: Docker Compose

```bash
docker-compose up --build
```

Finally, Docker Compose is used to build and start all services defined in your `docker-compose.yml`, setting up your project's environment.

## Troubleshooting

- **Python Dependencies**: If the pip install command fails, ensure you have Python and pip correctly installed and that your `requirements.local.txt` file exists and is correctly formatted.
- **tmux Session**: If the tmux session does not start as expected, verify that tmux is installed and that the paths and filenames in the command are correct.
- **Docker Compose**: Should there be issues with Docker Compose, check that Docker is running on your system and that the `docker-compose.yml` file is correctly configured.