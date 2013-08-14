#!/usr/bin/env python

import os
import sys

from setuptools import setup
from distutils.command.build import build


VERSION = '0.7.3'
DESCRIPTION = "Simple Python module to fake extended attributes"
LONG_DESCRIPTION = """
Unsafe hack to fake extended attributes. This works by imitating the python
xattr module, so imports call this module instead. xattrs are stored as a dict
in files referenced by their inode number.

The files are stored in the directory pointed to by 'xattr_dir' in lib.py,
be sure to set this to something the program has write privaledges to!

Most of the code in __init__ and setup.py was stolen from the original xattr
module. I just rewrote lib.py.
"""

CLASSIFIERS = filter(bool, map(str.strip,
"""
Environment :: Console
Intended Audience :: Developers
Natural Language :: English
Operating System :: MacOS :: MacOS X
Operating System :: POSIX :: Linux
Operating System :: POSIX :: BSD :: FreeBSD
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines()))

setup(
    name="xattr",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    author="Stephen Tredger",
    author_email="stredger@uvic.ca",
    url="http://github.com/xattr/xattr",
    license="MIT License",
    packages=['xattr'],
    ext_package='xattr',
    platforms=['MacOS X', 'Linux', 'FreeBSD', 'Solaris'],
    entry_points={
        'console_scripts': [
            "xattr = xattr.tool:main",
        ],
    },
    zip_safe=False,
)
