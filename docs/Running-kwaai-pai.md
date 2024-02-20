# Running the Project

## How to Use the Script

1. **Ensure the Script is Accessible**: Save the script in a file, for example, `run.sh`, within the root directory of your project.

2. **Make the Script Executable**: Change the script's permissions to make it executable. Open a terminal and run:

   ```bash
   chmod +x run.sh
   ```

3. **Run the Script**: Execute the script by running:

   ```bash
   ./run.sh
   ```

### Step 1: Create a tmux Session

```bash
tmux new-session -d -s llava_session 'cd quantization && ./llava.llamafile -m ../models/Publisher/Repository/model_tuned_q8_0.gguf'
```

A new tmux session named `llava_session` is created and detached. It navigates to the `quantization/executables` directory and executes the `llava.llamafile` with a model as its parameter.

### Step 2: Wait for Execution

```bash
sleep 5
```

The script pauses for 5 seconds to ensure the previous command has time to execute properly.

### Step 3: Docker Compose

```bash
docker-compose up --build
```

Finally, Docker Compose is used to build and start all services defined in your `docker-compose.yml`, setting up your project's environment.

## Troubleshooting

- **tmux Session**: If the tmux session does not start as expected, verify that tmux is installed and that the paths and filenames in the command are correct.
- **Docker Compose**: Should there be issues with Docker Compose, check that Docker is running on your system and that the `docker-compose.yml` file is correctly configured.