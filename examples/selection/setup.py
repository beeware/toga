#!/usr/bin/env python
import io
import re

from setuptools import setup, find_packages

with io.open('./selection/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='selection',
    version=version,
    description='A demonstration of all features of a toga.Selection example for the native GUI toolkit, Toga.',
    long_description=long_description,
    author='BeeWare',
    author_email='contact@beeware.org',
    license='New BSD',
    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
    ],
    options={
        'app': {
            'formal_name': 'Selection',
            'bundle': 'org.beeware'
        },
        'macos': {
            'app_requires': [
                'toga-gtk',
            ]
        },
    }
)
