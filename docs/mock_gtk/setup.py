#/usr/bin/env python
import io
import re

from setuptools import find_packages, setup

# This is a mock version of the GTK+ backend. It is required because RTD
# will try to `pip install toga`, which will in turn try to
# `pip install toga-gtk`. However, RTD doesn't include GTK in it's install
# image (nor should it!), so installing toga-gtk will fail.
#
# This package fulfills the pip requirement of `toga-gtk`, without
# *actually* doing anything.


with io.open('../../src/gtk/toga_gtk/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='toga-gtk',
    version=version,
    description='A mock of the GTK+ backend for the Toga widget toolkit.',
)
