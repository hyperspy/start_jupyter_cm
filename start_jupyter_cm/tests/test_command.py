import subprocess
import os
import sys
import pytest
from subprocess import PIPE

from start_jupyter_cm.utils import get_environment_label
from start_jupyter_cm.gnome import SPATH


def isadmin():
    try:
        # only windows users with admin privileges can read the C:\windows\temp
        os.listdir(os.path.join([os.environ.get('SystemRoot', 'C:\\windows'),
                                 'temp']))
        return True
    except:
        # We don't have admin right
        return False


@pytest.mark.parametrize("action", ['add', 'remove'])
def test_run_command(action):
    call = ["start_jupyter_cm"]
    if action == 'remove':
        call.append("--remove")
    # https://stackoverflow.com/questions/53209127/subprocess-unexpected-keyword-argument-capture-output
    output = subprocess.run(call, stdout=PIPE, stderr=PIPE, shell=True)
    assert output.returncode == 0
    env_label = get_environment_label()
    if sys.platform.startswith("linux"):
        for terminal in ["qtconsole", "notebook"]:
            script_path = os.path.join(SPATH, "Jupyter %s here%s" % (
                    terminal, env_label))
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


