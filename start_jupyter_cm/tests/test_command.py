import subprocess
import os
import sys
import pytest

from start_jupyter_cm.utils import get_environment_label
from start_jupyter_cm.gnome import SPATH


@pytest.mark.parametrize("action", ['add', 'remove'])
def test_run_command(action):
    output = subprocess.run(["jupyter_context-menu_%s" % action],
                            capture_output=True)
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
        h_key_base = winreg.HKEY_CURRENT_USER
        for terminal in ["qtconsole", "notebook"]:
            key = r'Software\Classes\Directory\shell\jupyter_%s_here%s\Command' % (
                terminal, env_label.replace(" ", "_"))
            if action == "add":
                # Check if we can open the key to test if the key is present.
                winreg.OpenKey(h_key_base, key)
                winreg.CloseKey(h_key_base, key)
            else:
                with pytest.raises(FileNotFoundError):
                    # If the key have been properly removed, we will expect
                    # a `FileNotFoundError` to be raised
                    winreg.OpenKey(h_key_base, key)

    output_string_list = output.stdout.decode().split("\n")[:-1]
    print(output_string_list)
    # If running from a conda environment, it should have the name of the
    # environemnt in brackend if not running from base environment
    out = "created" if action == "add" else "removed"
    expected_out = ['Jupyter qtconsole here%s %s.' % (env_label, out),
                    'Jupyter notebook here%s %s.' % (env_label, out),
                    ]
    if env_label != "":
        expected_out.insert(0, "Using conda environment: %s" %
                            os.environ["CONDA_DEFAULT_ENV"])
    assert output_string_list == expected_out
