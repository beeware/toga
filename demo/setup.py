#/usr/bin/env python
import io
import re

from setuptools import setup, find_packages

with io.open('./toga_demo/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='toga-demo',
    version=version,
    description='A demonstration of the capabilities of the Toga widget toolkit.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://beeware.org/toga-demo',
    include_package_data=True,
    packages=find_packages(),
    python_requires='>=3.5',
    package_data={
        'toga_demo': ['icons/*.icns', 'icons/*.png'],
    },
    install_requires=[
        'toga==%s' % version
    ],
    entry_points={
        'console_scripts': [
            'toga-demo = toga_demo.__main__:run',
        ]
    },
    license='New BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    options={
        'app': {
            'formal_name': 'Toga Demo',
            'bundle': 'org.beeware',
        },
        'ios': {
            'app_requires': [
                'toga-ios==%s' % version,
            ]
        },
        'django': {
            'app_requires': [
                'toga-django==%s' % version,
            ]
        },
        'macos': {
            'app_requires': [
                'toga-cocoa==%s' % version,
            ]
        },
        'linux': {
            'app_requires': [
                'toga-gtk==%s' % version,
            ]
        },
        'windows': {
            'app_requires': [
                'toga-winform==%s' % version,
            ]
        },
        'android': {
            'app_requires': [
                'toga-android==%s' % version,
            ]
        }
    }
)
