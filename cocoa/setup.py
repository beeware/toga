from setuptools import setup
from setuptools_scm import get_version

version = get_version(root="..")

setup(
    version=version,
    install_requires=[
        "fonttools >= 4.42.1, < 5.0.0",
        "rubicon-objc >= 0.4.5rc1, < 0.5.0",
        f"toga-core == {version}",
    ],
)
