#/usr/bin/env python
# import sys

from setuptools import setup
from tailor import VERSION

try:
    readme = open('README.rst')
    long_description = str(readme.read())
finally:
    readme.close()

required_pkgs = [

]
# if sys.version_info < (2, 7):
#     required_pkgs.append('argparse')

setup(
    name='tailor',
    version=VERSION,
    description='A Python native, OS native GUI toolkit.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://pybee.org/tailor',
    packages=[
        'tailor',
    ],
    install_requires=required_pkgs,
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    test_suite='tests'
)
