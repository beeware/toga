#!/usr/bin/env python
from setuptools import setup

# This is a mock version of the GTK+ backend. It is required because RTD
# will try to `pip install toga`, which will in turn try to
# `pip install toga-gtk`. However, RTD doesn't include GTK in it's install
# image (nor should it!), so installing toga-gtk will fail.
#
# This package fulfills the pip requirement of `toga-gtk`, without
# *actually* doing anything.

setup(
    name="toga-gtk",
    version="0.3.0.dev39",
    description="A mock of the GTK+ backend for the Toga widget toolkit.",
)
