'''
    CAI DICOM2CLOUD: setup_mac.py (Mac OSX package)
    *******************************************************************************
    Copyright (C) 2017  QBI Software, The University of Queensland

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

Usage:
    python setup_mac.py py2app --matplotlib-backends='-'


Notes:
    Clean on reruns:
    > rm -rf build dist __pycache__ .eggs
    May need to use system python rather than virtualenv
    > /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 setup_mac.py py2app --matplotlib-backends='-' > build.log

    Macholib version=1.7 required to prevent endless recursions
    Specify matplotlib backends with '-'

TODO: wxPython - remove Scrollbars from ListCtls
TODO: Find mac with hypervisor CPU - required for Docker
>sysctl kern.hv_support
Should return 1 for yes, 0 for no
'''
from os import getcwd
from os.path import join

from setuptools import setup

from dicom2cloud.clientgui import __version__

# Self -bootstrapping https://py2app.readthedocs.io
# import ez_setup
# ez_setup.use_setuptools()
application_title = 'Dicom2Cloud'
main_python_file = join('.','dicom2cloud','clientgui.py')
exe_name='dicom2cloud'
#mainpython = "/Library/Frameworks/Python.framework/Versions/3.6/bin/python3"

# Add info to MacOSX plist
plist = dict(
    CFBundleName=exe_name,
    CFBundleDisplayName=application_title,
    NSHumanReadableCopyright='Copyright (c) 2018 The University of Queensland',
    CFBundleTypeIconFile='favicon.ico.icns',
    CFBundleVersion=__version__
            )

APP = [main_python_file]
DATA_FILES = [join('dicom2cloud','config')]
PARENTDIR= join(getcwd(),'.')
OPTIONS = {'argv_emulation': False,
           #'use_pythonpath': True,
           'plist': plist,
           'iconfile': join('dicom2cloud','gui','favicon.ico.icns'),
           'packages': ['sqlite3','wx','dicom2cloud','numpy','google'],
           'includes':['six','appdirs','packaging','packaging.version','packaging.specifiers','packaging.requirements','os','numbers','future_builtins','html.parser','google'],
           'bdist_base': join(PARENTDIR, 'build'),
           'dist_dir': join(PARENTDIR, 'dist'),
           }

setup(
    name=application_title,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app','pyobjc-framework-Cocoa','numpy','google'],
)
