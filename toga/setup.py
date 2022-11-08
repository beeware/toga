#!/usr/bin/env python
from setuptools import setup

version = "0.0.1rc10"

setup(
    version=version,
    extras_require={
        # Automatically installed platform backends
        ':sys_platform=="win32"': ["toga-winforms==%s" % version],
        ':sys_platform=="linux"': ["toga-gtk==%s" % version],
        ':sys_platform=="darwin"': ["toga-cocoa==%s" % version],
    },
)
