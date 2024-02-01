import subprocess
from utilities.config import MODEL_NAME, EMAILS_DATA_SET_PATH

class CommandExecutor:
    """Command executor for fine-tunning a model."""

    def __init__(self):
        self.model_name = MODEL_NAME

    def execute_fine_tunning(self):
        """Execute the fine-tunning command."""

        base_command = "python3 ./examples/scripts/sft.py"
        model_option = f"--model_name {MODEL_NAME}"
        dataset_option = f"--dataset_name {EMAILS_DATA_SET_PATH}"
        load_option = "--load_in_4bit"
        use_peft_option = "--use_peft"

        command = f"{base_command} {model_option} {dataset_option} {load_option} {use_peft_option}"

        # try:
        #     # Run the command
        #     subprocess.run(command, shell=True, check=True)
        # except subprocess.CalledProcessError as e:
        #     print(f"Command execution failed with error code {e.returncode}")
        #     print(e)
