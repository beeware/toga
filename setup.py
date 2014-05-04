#/usr/bin/env python
# import sys
from setuptools import setup
from toga import VERSION

try:
    readme = open('README.rst')
    long_description = str(readme.read())
finally:
    readme.close()

required_pkgs = [
    'cassowary',
]
# if sys.version_info < (2, 7):
#     required_pkgs.append('argparse')

setup(
    name='toga',
    version=VERSION,
    description='A Python native, OS native GUI toolkit.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://pybee.org/toga',
    packages=[
        'toga',
    ],
    install_requires=required_pkgs,
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
    ],
    test_suite='tests',
)
