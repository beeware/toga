#/usr/bin/env python
import io
import re
from setuptools import setup, find_packages
import sys


if sys.version_info[:3] < (3, 4):
    raise SystemExit("Toga requires Python 3.4+.")


with io.open('./toga_win32/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='toga-win32',
    version=version,
    description='A Win32 (Microsoft Windows) backend for the Toga widget toolkit.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://pybee.org/toga',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'toga-core',
    ],
    license='New BSD',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
    ],
    test_suite='tests',
)
