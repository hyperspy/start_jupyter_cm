import subprocess
import os
import sys
import pytest
import shutil
from subprocess import PIPE

from start_jupyter_cm.utils import get_environment_label
from start_jupyter_cm.linux import get_file_manager_config


def isadmin():
    try:
        # only windows users with admin privileges can read the C:\windows\temp
        os.listdir(os.path.join([os.environ.get('SystemRoot', 'C:\\windows'),
                                 'temp']))
        return True
    except:
        # We don't have admin right
        return False

def run_command(**kwargs):
    action = kwargs.get('action')
    file_manager = kwargs.get('file_manager')
    call = ["start_jupyter_cm"]

    if file_manager is not None:
        call.extend(["-f", file_manager])
    if action == 'remove':
        call.append("--remove")

    print("call:", call)

    try:
        # https://stackoverflow.com/questions/53209127/subprocess-unexpected-keyword-argument-capture-output
        subprocess.run(call, stdout=PIPE, stderr=PIPE, check=True)
    except subprocess.CalledProcessError as err:
        print("returncode", err.returncode)
        print("cmd", err.cmd)
        print("output", err.output)
        print("stdout", err.stdout)
        print("stderr", err.stderr)


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux only")
@pytest.mark.parametrize("file_manager", ['nautilus', 'caja', 'dolphin', 'nemo'])
@pytest.mark.parametrize("action", ['add', 'remove'])
def test_run_command_linux(action, file_manager):
    run_command(action=action, file_manager=file_manager)

    if shutil.which(file_manager) is None:
        pytest.skip(f"{file_manager} is not installed.")

    manager_config_path = get_file_manager_config(file_manager)
    env_label = get_environment_label()
    if sys.platform.startswith("linux"):
        name, scripts_folder_path = file_manager, manager_config_path[file_manager]
        print('file_manager:', name)
        print('scripts_folder_path:', scripts_folder_path)
        print("content of script folder:", os.listdir(scripts_folder_path))
        for terminal in ["qtconsole", "notebook", 'lab']:
            shortcut_name = f"Jupyter {terminal.capitalize()} here{env_label}"
            if name == 'dolphin':
                script_path = os.path.join(scripts_folder_path, f"{shortcut_name}.desktop")
            elif name == 'nemo':
                script_path = os.path.join(scripts_folder_path, f"{shortcut_name}.nemo_action")
            else:
                script_path = os.path.join(scripts_folder_path, shortcut_name)

            print('script_path:', script_path)
            shorcut_present = (action == "add" and shutil.which(f"jupyter-{terminal}") is not None)
            assert shorcut_present is os.path.exists(script_path)


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="Windows only")
@pytest.mark.parametrize("action", ['add', 'remove'])
def test_run_command_windows(action):
    run_command(action=action)
    env_label = get_environment_label()

    import winreg
    if isadmin:
        h_key_base = winreg.HKEY_LOCAL_MACHINE
    else:
        h_key_base = winreg.HKEY_CURRENT_USER
    for terminal in ["qtconsole", "notebook", "lab"]:
        key = rf'Software\Classes\Directory\shell\jupyter_{terminal}_here{env_label.replace(" ", "_")}\Command'
        if action == "add" and shutil.which(f"jupyter-{terminal}") is not None:
            # Check if we can open the key to test if the key is present.
            registry_key = winreg.OpenKey(h_key_base, key)
            winreg.CloseKey(registry_key)
        else:
            with pytest.raises(FileNotFoundError):
                # If the key have been properly removed, we will expect
                # a `FileNotFoundError` to be raised
                winreg.OpenKey(h_key_base, key)

