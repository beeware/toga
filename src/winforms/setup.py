#!/usr/bin/env python
import re

from setuptools import setup

# Version handline needs to be programatic because
# we can't import toga_winforms to compute the version;
# and to support versioned subpackage dependencies
with open('src/toga_winforms/__init__.py', encoding='utf8') as version_file:
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
        # The Python.net team hasn't published 2.X wheels for Python 3.9 or 3.10,
        # and their development effort seems to be focussed on the 3.X branch;
        # they've indicated they're not planning to make the 2.X branch compatible
        # with Python 3.10. If we want to be able to support "current" Python,
        # we need to use the 3.0 branch.
        #
        # At time of writing, the most recent (and only) version of Python.net 3.0
        # that has been released is the alpha version 3.0.0a1.
        'pythonnet>=3.0.0a1',
        'toga-core==%s' % version,
    ],
    test_suite='tests',
    test_require=[
        'toga-dummy==%s' % version,
    ]
)
