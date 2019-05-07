#!/usr/bin/env python
import io
import re

from setuptools import setup, find_packages

with io.open('./beeliza/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='beeliza',
    version=version,
    description='A Bee-themed Eliza chat-bot.',
    long_description=long_description,
    author='BeeWare Project',
    author_email='contact@beeware.org',
    license='BSD license',
    packages=find_packages(
        exclude=[
            'docs', 'tests',
            'windows', 'macOS', 'linux',
            'iOS', 'android',
            'django'
        ]
    ),
    python_requires='>=3.5',
    package_data={
        'beeliza': ['resources/*'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD license',
    ],
    install_requires=[
    ],
    options={
        'app': {
            'formal_name': 'Beeliza',
            'bundle': 'org.beeware'
        },

        # Desktop/laptop deployments
        'macos': {
            'app_requires': [
                'toga-cocoa',
            ]
        },
        'linux': {
            'app_requires': [
                'toga-gtk',
            ]
        },
        'windows': {
            'app_requires': [
                'toga-winforms',
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [
                'toga-ios',
            ]
        },
        'android': {
            'app_requires': [
                'toga-android',
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [
                'toga-django',
            ]
        },
    }
)
