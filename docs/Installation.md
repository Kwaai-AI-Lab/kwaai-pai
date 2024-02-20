# Installation and Configuration Guide

This guide provides detailed instructions on how to use the provided installation and configuration script for setting up the necessary environment and services for the project. The script automates the process of starting a session with specific tasks and then initiating Docker containers as defined in the project's `docker-compose.yml`.

## Script Overview

The script performs the following actions:

1. Creates a new detached session in `tmux` named `llava_session`.
2. Within this session, it changes the directory to `quantization/executables` and executes a file named `llava.llamafile` with specific parameters.
3. Waits for 5 seconds to ensure the first command has been executed properly.
4. Executes `docker-compose up --build` to build and start the Docker containers as per the configuration in `docker-compose.yml`.

## Prerequisites

Before running the script, ensure you have the following installed:

- `tmux`: A terminal multiplexer that allows you to switch easily between several programs in one terminal.
- `Docker` and `Docker Compose`: Required for creating and managing the application's containers.

## How to Use the Script

1. **Save the Script**: Ensure the script is saved in a file, for example, `run.sh`, and located in the root directory of your project.

2. **Make the Script Executable**: Change the script's permissions to make it executable by running the following command in your terminal:

   ```bash
   chmod +x run.sh
   ```

3. **Execute the Script**: Run the script by executing the following command in your terminal:

   ```bash
   ./run.sh
   ```

## Expected Outcomes

- A new `tmux` session named `llava_session` will be created and detached. This session will execute the `llava.llamafile` with the specified model, performing necessary initializations or computations.
- After a brief pause, Docker Compose will build and start all services defined in your `docker-compose.yml`, setting up your project's environment.

## Troubleshooting

- **tmux Session Not Found**: If you encounter issues where the `tmux` session does not seem to start, ensure `tmux` is correctly installed and try running the commands manually to check for errors.
- **Docker Compose Failures**: If `docker-compose up --build` fails, verify your Docker and Docker Compose installations, and check the `docker-compose.yml` for any configuration errors.

## Additional Notes

- You can attach to the `tmux` session at any time to monitor the output of the `llava.llamafile` execution by running `tmux attach-session -t llava_session`.
- Ensure that the paths and filenames specified in the script match your project's structure and naming conventions.