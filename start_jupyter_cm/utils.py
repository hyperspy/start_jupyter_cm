import os


def get_environment_label():
    environment_label = ""
    if ("CONDA_DEFAULT_ENV" in os.environ and
        os.environ["CONDA_DEFAULT_ENV"] != "base"):
        print(f"Using conda environment: {os.environ['CONDA_DEFAULT_ENV']}\n")
        # Add environment name if necessary
        environment_label = " (%s)" % os.environ["CONDA_DEFAULT_ENV"]
    return environment_label
