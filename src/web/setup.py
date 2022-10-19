#!/usr/bin/env python
import re

from setuptools import setup

# Version handline needs to be programatic because
# we can't import toga_web to compute the version;
# and to support versioned subpackage dependencies
with open('src/toga_web/__init__.py', encoding='utf8') as version_file:
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
        # TODO: Due to https://github.com/pyodide/pyodide/issues/2408, the name
        # toga-core is ambigous when on the package hasn't been published to
        # PyPI. As a workaround, don't specify the dependency, and manually
        # ensure that toga-core is installed.
        # 'toga-core==%s' % version,
    ],
)
