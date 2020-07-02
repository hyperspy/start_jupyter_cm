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
# To use a consistent encoding
from codecs import open

import start_jupyter_cm

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="start_jupyter_cm",
    package_dir={'start_jupyter_cm': 'start_jupyter_cm'},
    version=start_jupyter_cm.__version__,
    packages=['start_jupyter_cm', ],
    requires=[],
    package_data={'start_jupyter_cm': ['scripts/*.py',
                                       'icons/*.ico',
                                       'icons/*.png',
                                       'prototype.workflow/Contents/*',
                                       ]},
    author="The HyperSpy Developers",
    description="Add entries to start Jupyter from context menu.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="BSDv3",
    url="https://github.com/hyperspy/start_jupyter_cm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
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
            'start_jupyter_cm = start_jupyter_cm.command:_run',
        ], }
)
