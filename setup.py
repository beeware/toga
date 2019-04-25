#/usr/bin/env python
import io
import re
from setuptools import setup


with io.open('src/core/toga/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='toga',
    version=version,
    description='A Python native, OS native GUI toolkit.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='https://beeware.org/project/projects/libraries/toga/',
    extras_require={
        # Automatically installed platform backends
        ':sys_platform=="win32"': ['toga-winforms==%s' % version],
        ':sys_platform=="linux"': ['toga-gtk==%s' % version],
        ':sys_platform=="darwin"': ['toga-cocoa==%s' % version],
    },
    license='New BSD',
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
    package_urls={
        'Funding': 'https://beeware.org/contributing/membership/',
        'Documentation': 'https://toga.readthedocs.io/',
        'Tracker': 'https://github.com/pybee/toga/issues',
        'Source': 'https://github.com/pybee/toga',
    },
)
