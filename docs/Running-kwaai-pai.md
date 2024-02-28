# How to Run the Kwaai PAI Assistant

This document provides comprehensive instructions for running the Kwaai PAI Assistant across different operating systems. It's important to note that the project operates in two distinct stages related to the fine-tuning of the LLaMA 2 7B model. Understanding these stages is crucial for successfully deploying and utilizing the Kwaai PAI Assistant.

## Project Stages

### Stage 1: Pre-Fine Tuning

Before the fine-tuning process has been executed with user-specific data, the project should be run as outlined in this document. This initial stage involves:

- Downloading user data via IMAP.
- Executing the fine-tuning process of the LLaMA 2 7B model with the user's data. The duration and success of this process will depend on several factors, including the computing hardware (specifically, the GPU used), the volume of data to be processed, and the initial state of the model.

It's imperative to run the project following the instructions provided herein to ensure the fine-tuning process is initiated correctly and completed efficiently.

### Stage 2: Post-Fine Tuning

After the fine-tuning process has been completed and the learning checkpoints have been generated, it's necessary to adapt the model for consumption by the Kwaai PAI Assistant. This involves:

- Reading and following the guidelines specified in the `Creating-Llama2-quantized-model.md` document. This document outlines the steps to quantize the model, integrating the fine-tuning adjustments into the LLaMA 2 7B model, making it ready for use with the Kwaai PAI Assistant.

Adapting the model as per the instructions in the `Creating-Llama2-quantized-model.md` file is essential for the successful deployment and operation of the Kwaai PAI Assistant in its fully optimized form.

## Running Instructions

This section provides step-by-step instructions on how to run the Kwaai PAI Assistant on different operating systems. The process involves making a script executable and then running it.

### All Operating Systems

1. **Make the Script Executable**: Before running the script, you need to change its permissions to make it executable. This step varies slightly depending on your operating system.

2. **Run the Script**: Once the script is executable, you can run it to start the PAI Assistant.

### Linux and MacOS

For Linux and MacOS users, the process is straightforward:

1. Open a terminal.

2. Navigate to the directory containing `run.sh`.

3. Make the script executable by running:

   ```bash
   chmod +x run.sh
   ```

4. Execute the script with:

   ```bash
   ./run.sh
   ```

### Windows

Running scripts on Windows can be different due to the operating system's distinct command-line environment and script execution policies.

1. **Using Windows Subsystem for Linux (WSL)**: For a similar experience to Linux/MacOS, Windows users can utilize WSL. After setting up WSL:

   - Open a WSL terminal.

   - Navigate to the script's directory (ensure it's accessible within WSL).

   - Follow the Linux/MacOS instructions to make the script executable and run it.

2. **Using PowerShell or Command Prompt**: If you prefer not to use WSL, you may need to convert the script to a `.bat` file or use an equivalent command in PowerShell. PowerShell has different commands for changing file permissions and execution might not require explicit permission changes as in Unix-like systems.

   - To run a PowerShell script, you might first need to adjust the execution policy with:

     ```powershell
     Set-ExecutionPolicy RemoteSigned
     ```

   - Then, you can run the script directly if it's a `.ps1` file, or execute a `.bat` version of your script designed for Windows.

### Considerations

- **File Paths**: Be aware of differences in file path conventions between operating systems. Windows uses backslashes (`\`) while Linux and MacOS use forward slashes (`/`).
- **Environment Variables**: Setting environment variables can differ across systems. Use `export` in Linux/MacOS and `set` in Windows Command Prompt, or `$env:` in PowerShell.
- **Permissions**: Windows file permissions are managed differently than in Unix-like systems. Typically, making a script executable is not necessary on Windows.

By following these instructions tailored to your operating system, you'll be able to run the Kwaai PAI Assistant smoothly on your machine.
By carefully following these instructions and understanding the project's stages, you will be prepared to run the Kwaai PAI Assistant effectively on your system, regardless of the project's phase.