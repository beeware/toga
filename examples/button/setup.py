#!/usr/bin/env python
import io
import re
from setuptools import setup, find_packages
import sys

with io.open('./button/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='button',
    version=version,
    description='A demonstration of all features of a button example for (macOS) of the native GUI toolkit, Toga.',
    long_description=long_description,
    author='Dayanne Fernandes',
    author_email='dayannefernandesc@gmail.com',
    license='Other',
    packages=find_packages(exclude=['docs', 'tests']),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Other',
    ],
    install_requires=[
    ],
    options={
        'app': {
            'formal_name': 'button',
            'bundle': 'button.toga.example'
        },

        'macos': {
            'app_requires': [
                'toga-cocoa',
            ]
        },
    }
)
