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


from distutils.core import setup
import os
import sys

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
    version="1.0",
    packages=['start_jupyter_cm', ],
    requires=install_req,
    scripts=scripts,
    package_data={'start_jupyter_cm': ['scripts/*.py', 'icons/*.ico', ]},
    author="The HyperSpy Developers",
    description="Add entries to start Jupyter from context menu",
    license="BSDv3",
    # classifiers=[
    #     "Programming Language :: Python :: 2.7",
    #     "Development Status :: 4 - Beta",
    #     "Environment :: Console",
    #     "Intended Audience :: Science/Research",
    #     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    #     "Natural Language :: English",
    #     "Operating System :: OS Independent",
    #     "Topic :: Scientific/Engineering",
    #     "Topic :: Scientific/Engineering :: Physics",
    # ],
)
