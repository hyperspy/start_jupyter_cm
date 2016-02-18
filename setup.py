# -*- coding: utf-8 -*-
# Copyright 2007-2011 The HyperSpy developers
#
# This file is part of  HyperSpy.
#
#  HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  HyperSpy.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
import os
import sys
# To use a consistent encoding
from codecs import open

import start_jupyter_cm

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

install_req = ['jupyter', 'qtconsole', ]


def are_we_building4windows():
    for arg in sys.argv:
        if 'wininst' in arg:
            return True

scripts = []

if are_we_building4windows() or os.name in ['nt', 'dos']:
    # In the Windows command prompt we can't execute Python scripts
    # without a .py extension. A solution is to create batch files
    # that runs the different scripts.
    # (code adapted from scitools)
    scripts.extend(('scripts/win_post_installation.py',))

setup(
    name="start_jupyter_cm",
    package_dir={'start_jupyter_cm': 'start_jupyter_cm'},
    version=start_jupyter_cm.__version__,
    packages=['start_jupyter_cm', ],
    requires=install_req,
    scripts=scripts,
    package_data={'start_jupyter_cm': ['scripts/*.py',
                                       'icons/*.ico',
                                       'icons/*.png',
                                       ]},
    author="The HyperSpy Developers",
    description="Add entries to start Jupyter from context menu.",
    long_description=long_description,
    license="BSDv3",
    url="https://github.com/hyperspy/start_jupyter_cm",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Topic :: Desktop Environment :: Gnome",
    ],
    entry_points={
        'console_scripts': [
            'jupyter_context-menu_add = start_jupyter_cm:_add',
            'jupyter_context-menu_remove = start_jupyter_cm:_remove',
        ], }
)
