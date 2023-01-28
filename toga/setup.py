from setuptools import setup
from setuptools_scm import get_version

version = get_version(root="..")

setup(
    version=version,
    extras_require={
        # Automatically installed platform backends
        ':sys_platform=="win32"': ["toga-winforms==%s" % version],
        ':sys_platform=="linux"': ["toga-gtk==%s" % version],
        ':sys_platform=="darwin"': ["toga-cocoa==%s" % version],
    },
)
