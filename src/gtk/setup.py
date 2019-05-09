#/usr/bin/env python
import io
import re

from setuptools import setup, find_packages


with io.open('toga_gtk/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='toga-gtk',
    version=version,
    description='A GTK+ backend for the Toga widget toolkit.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://beeware.org/toga',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.5',
    install_requires=[
        'toga-core==%s' % version,
        'gbulb>=0.5.3',
        'pycairo>=1.17.0',
        'pygobject>=3.14.0',
    ],
    tests_require=[
        'toga-dummy==%s' % version
    ],
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: X11 Applications :: GTK',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
    ],
    test_suite='tests',
)
