#!/usr/bin/env python
import io
import re

from setuptools import setup

with io.open('./toga_flask.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    version=version,
    install_requires=[
        'flask~=1.1',
        'toga-web==%s' % version,
    ],
)
