#!/usr/bin/env python
import re

from setuptools import setup

# Version handline needs to be programatic because
# we can't import toga to compute the version;
# and to support versioned extra dependencies
with open('src/core/toga/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    version=version,
    extras_require={
        # Automatically installed platform backends
        ':sys_platform=="win32"': ['toga-winforms==%s' % version],
        ':sys_platform=="linux"': ['toga-gtk==%s' % version],
        ':sys_platform=="darwin"': ['toga-cocoa==%s' % version],
    },
)
