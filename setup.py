#!/usr/bin/env python3
import os
import re

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version("rest_framework")

setup(
    name="OSCR",
    version=version,
    url="https://github.com/STOCD/OSCR",
)
