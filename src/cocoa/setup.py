#!/usr/bin/env python
import re

from setuptools import setup

# Version handline needs to be programatic because
# we can't import toga_cocoa to compute the version;
# and to support versioned subpackage dependencies
with open('src/toga_cocoa/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file.read(),
        re.M
    )
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    version=version,
    install_requires=[
        'rubicon-objc>=0.4.2',
        'toga-core==%s' % version,
    ],
    test_suite='tests',
    test_require=[
        'toga-dummy==%s' % version,
    ]
)
