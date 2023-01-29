from setuptools import setup
from setuptools_scm import get_version

version = get_version(root="..")

setup(
    version=version,
    install_requires=[
        "pythonnet>=3.0.0",
        "toga-core==%s" % version,
    ],
)
