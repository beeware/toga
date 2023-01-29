from setuptools import setup
from setuptools_scm import get_version

version = get_version(root="..")

setup(
    version=version,
    install_requires=[
        "toga-core==%s" % version,
        "gbulb>=0.5.3",
        "pycairo>=1.17.0",
        "pygobject>=3.14.0",
    ],
)
