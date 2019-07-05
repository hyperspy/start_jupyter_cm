#/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2007-2011 The Jupyter developers
#
# This file is part of  Jupyter.
#
#  Jupyter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  Jupyter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  Jupyter.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import shutil
import winreg

from .utils import get_environment_label


WPSCRIPTS_FOLDER = "Scripts"
CONDA_ENV_LABEL = get_environment_label()


def add_jupyter_here():
    try:
        _add_jupyter_here(all_users=True)
    except PermissionError:
        # No admin privileges, install for single user
        _add_jupyter_here(all_users=False)


def remove_jupyter_here():
    try:
        _remove_jupyter_here(all_users=True)
    except PermissionError:
        # Admin right required to uninstall
        print("Administrator privileges are required to uninstall the context "
              "menu shortcut")
    else:
        # No context menu for all users found, uninstall for single user 
        _remove_jupyter_here(all_users=False)


def _remove_jupyter_here(all_users):
    if all_users:
        h_key_base = winreg.HKEY_LOCAL_MACHINE
        install_type = "all users"
    else:
        h_key_base = winreg.HKEY_CURRENT_USER
        install_type = "single user"

    for terminal in ('qtconsole', 'notebook', 'lab'):
        try:
            winreg.DeleteKey(
                h_key_base,
                r'Software\Classes\Directory\shell\jupyter_%s_here%s\Command' % (
                terminal, CONDA_ENV_LABEL.replace(" ", "_")))
            winreg.DeleteKey(
                h_key_base,
                r'Software\Classes\Directory\shell\jupyter_%s_here%s' % (
                terminal, CONDA_ENV_LABEL.replace(" ", "_")))
            winreg.DeleteKey(
                h_key_base,
                r'Software\Classes\Directory\Background\shell\jupyter_%s_here%s\Command' % (
                terminal, CONDA_ENV_LABEL.replace(" ", "_")))
            winreg.DeleteKey(
                h_key_base,
                r'Software\Classes\Directory\Background\shell\jupyter_%s_here%s' % (
                terminal, CONDA_ENV_LABEL.replace(" ", "_")))
            print("Jupyter %s here%s context menu entry removed for %s." % (
                    terminal, CONDA_ENV_LABEL, install_type))
        except FileNotFoundError:
            # If this fails it is because it was not installed, so nothing to
            # worry about.
            pass


def _add_jupyter_here(all_users):
    # Install the context menu entries for the qtconsole and the notebook
    logo_path = os.path.expandvars(os.path.join(
        os.path.dirname(__file__), 'icons'))
    logos = {'qtconsole': os.path.join(logo_path, 'jupyter-qtconsole.ico'),
             'notebook': os.path.join(logo_path, 'jupyter.ico'),
             'lab': os.path.join(logo_path, 'jupyter.ico')}
    if all_users:
        # directory_shell = "Directory\shell"
        # background_shell = "Directory\Background\shell"
        h_key_base = winreg.HKEY_LOCAL_MACHINE
        install_type = "all users"
    else:
        # directory_shell = "Directory\shell"
        # background_shell = "Directory\Background\shell"
        h_key_base = winreg.HKEY_CURRENT_USER
        install_type = "single user"

    for terminal in ('qtconsole', 'notebook', 'lab'):
        if shutil.which("jupyter-%s" % terminal):
            if "WINPYDIR" in os.environ:
                # Calling from WinPython
                # Paths are relative, so we have to set the env first
                script = os.path.join(os.environ["WINPYDIR"], "..",
                                      WPSCRIPTS_FOLDER,
                                      "env.bat")
                script += " & jupyter-%s" % terminal
            elif "CONDA_EXE" in os.environ:
                # Calling from a conda environment, call activation script
                # before executing script.
                script = '%windir%\system32\cmd.exe "/K" '
                script += os.path.join(
                        os.path.split(os.environ["CONDA_EXE"])[0], "activate.bat")
                if CONDA_ENV_LABEL != "":
                    script += " " + os.environ["CONDA_DEFAULT_ENV"]
                script += " & jupyter-%s.exe" % terminal
            else:
                script = os.path.join(
                    sys.prefix, 'Scripts', "jupyter-%s.exe" % terminal)
    
            shell_script = script + ' --notebook-dir "%1"' if \
                    terminal == "notebook" else script
    
            key = winreg.CreateKey(
                h_key_base,
                r'Software\Classes\Directory\shell\jupyter_%s_here%s' % (
                terminal, CONDA_ENV_LABEL.replace(" ", "_")))
            winreg.SetValueEx(
                key,
                "",
                0,
                winreg.REG_SZ,
                "Jupyter %s here%s" % (terminal, CONDA_ENV_LABEL))
            winreg.SetValueEx(
                key,
                'Icon',
                0,
                winreg.REG_SZ,
                logos[terminal]
            )
            key.Close()
            key = winreg.CreateKey(
                h_key_base,
                r'Software\Classes\Directory\shell\jupyter_%s_here%s\Command' % (
                terminal, CONDA_ENV_LABEL.replace(" ", "_")))
            winreg.SetValueEx(
                key,
                "",
                0,
                winreg.REG_EXPAND_SZ,
                shell_script)
            key.Close()
            key = winreg.CreateKey(
                h_key_base,
                r'Software\Classes\Directory\Background\shell\jupyter_%s_here%s' % (
                terminal, CONDA_ENV_LABEL.replace(" ", "_")))
            winreg.SetValueEx(
                key,
                "",
                0,
                winreg.REG_SZ,
                "Jupyter %s here%s" % (terminal, CONDA_ENV_LABEL))
            winreg.SetValueEx(
                key,
                'Icon',
                0,
                winreg.REG_SZ,
                logos[terminal]
            )
            key.Close()
            key = winreg.CreateKey(
                h_key_base,
                r'Software\Classes\Directory\Background\shell\jupyter_%s_here%s\Command' % (
                terminal, CONDA_ENV_LABEL.replace(" ", "_")))
            winreg.SetValueEx(key, "", 0, winreg.REG_EXPAND_SZ, script)
            key.Close()

            print("Jupyter %s here%s context menu entry created for %s." % (
                    terminal, CONDA_ENV_LABEL, install_type))
