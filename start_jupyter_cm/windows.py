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
try:
    import winreg
except ImportError:
    # Python 2
    import _winreg as winreg
from win32com.shell import shell

WPSCRIPTS_FOLDER = "Scripts"

def remove_jupyter_here():
    for env in ('qtconsole', 'notebook'):
        try:
            winreg.DeleteKey(
                winreg.HKEY_CLASSES_ROOT,
                r'Directory\shell\jupyter_%s_here\Command' %
                env)
            winreg.DeleteKey(
                winreg.HKEY_CLASSES_ROOT,
                r'Directory\shell\jupyter_%s_here' %
                env)
            winreg.DeleteKey(
                winreg.HKEY_CLASSES_ROOT,
                r'Directory\Background\shell\jupyter_%s_here\Command' %
                env)
            winreg.DeleteKey(
                winreg.HKEY_CLASSES_ROOT,
                r'Directory\Background\shell\jupyter_%s_here' %
                env)
            print("Jupyter %s here context menu entry removed." % env)
        except:
            # If this fails it is because it was not installed, so nothing to
            # worry about.
            pass


def add_jupyter_here():
    # Install the context menu entries for the qtconsole and the notebook
    logo_path = os.path.expandvars(os.path.join(
        os.path.dirname(__file__), 'icons'))
    logos = {'qtconsole': os.path.join(logo_path, 'jupyter-qtconsole.ico'),
             'notebook': os.path.join(logo_path, 'jupyter.ico')}
    for env in ('qtconsole', 'notebook'):
        if "WINPYDIR" in os.environ:
            # Calling from WinPython
            # Paths are relative, so we have to set the env first
            script = os.path.join(os.environ["WINPYDIR"], "..",
                                  WPSCRIPTS_FOLDER,
                                  "env.bat")
            script += " & jupyter-%s" % env
        else:
            script = os.path.join(
                sys.prefix, 'Scripts', "jupyter-%s.exe" % env)

        shell_script = script + ' --notebook-dir "%1"' if env == "notebook"\
            else script

        key = winreg.CreateKey(
            winreg.HKEY_CLASSES_ROOT,
            r'Directory\shell\jupyter_%s_here' %
            env)
        winreg.SetValueEx(
            key,
            "",
            0,
            winreg.REG_SZ,
            "Jupyter %s here" %
            env)
        winreg.SetValueEx(
            key,
            'Icon',
            0,
            winreg.REG_SZ,
            logos[env]
        )
        key.Close()
        key = winreg.CreateKey(
            winreg.HKEY_CLASSES_ROOT,
            r'Directory\shell\jupyter_%s_here\Command' %
            env)
        winreg.SetValueEx(
            key,
            "",
            0,
            winreg.REG_EXPAND_SZ,
            shell_script)
        key.Close()
        key = winreg.CreateKey(
            winreg.HKEY_CLASSES_ROOT,
            r'Directory\Background\shell\jupyter_%s_here' %
            env)
        winreg.SetValueEx(
            key,
            "",
            0,
            winreg.REG_SZ,
            "Jupyter %s here" %
            env)
        winreg.SetValueEx(
            key,
            'Icon',
            0,
            winreg.REG_SZ,
            logos[env]
        )
        key.Close()
        key = winreg.CreateKey(
            winreg.HKEY_CLASSES_ROOT,
            r'Directory\Background\shell\jupyter_%s_here\Command' %
            env)
        winreg.SetValueEx(key, "", 0, winreg.REG_EXPAND_SZ, script)
        key.Close()

        print("Jupyter %s here context menu entry created." % env)
