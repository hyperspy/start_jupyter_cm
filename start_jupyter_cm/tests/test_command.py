import subprocess
import os
import sys
import pytest
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


@pytest.mark.parametrize("file_manager", [None, 'nautilus', 'caja', 'dolphin'])
@pytest.mark.parametrize("action", ['add', 'remove'])
def test_run_command(action, file_manager):
    call = ["start_jupyter_cm"]
    if action == 'remove':
        call.append("--remove")
    if file_manager is not None:
        call.append(f"-f {file_manager}")
    try:
        # https://stackoverflow.com/questions/53209127/subprocess-unexpected-keyword-argument-capture-output
        subprocess.run(call, stdout=PIPE, stderr=PIPE, check=True)
    except subprocess.CalledProcessError as err:
        print("returncode", err.returncode)
        print("cmd", err.cmd)
        print("output", err.output)
        print("stdout", err.stdout)
        print("stderr", err.stderr)

    manager_config_path = get_file_manager_config(file_manager)
    env_label = get_environment_label()
    if sys.platform.startswith("linux"):
        for name, scripts_folder_path in manager_config_path.items():
            for terminal in ["qtconsole", "notebook", 'lab']:
                shortcut_name = f"Jupyter {terminal} here{env_label}"
                if name == 'dolphin':
                    script_path = os.path.join(scripts_folder_path, f"{shortcut_name}.desktop")
                else:
                    script_path = os.path.join(scripts_folder_path, 'scripts', shortcut_name)

            script_exist = os.path.exists(script_path)
            if action == "add":
                assert script_exist
            else:
                assert not script_exist

    elif sys.platform == "win32":
        import winreg
        if isadmin:
            h_key_base = winreg.HKEY_LOCAL_MACHINE
        else:
            h_key_base = winreg.HKEY_CURRENT_USER
        for terminal in ["qtconsole", "notebook"]:
            key = r'Software\Classes\Directory\shell\jupyter_%s_here%s\Command' % (
                terminal, env_label.replace(" ", "_"))
            if action == "add":
                # Check if we can open the key to test if the key is present.
                registry_key = winreg.OpenKey(h_key_base, key)
                winreg.CloseKey(registry_key)
            else:
                with pytest.raises(FileNotFoundError):
                    # If the key have been properly removed, we will expect
                    # a `FileNotFoundError` to be raised
                    winreg.OpenKey(h_key_base, key)


