#!/usr/bin/env python3
import os
import re

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version("OSCR")

setup(
    name="OSCR",
    long_description="Open Source Conbat Reader",
    version=version,
    url="https://github.com/STOCD/OSCR",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "PyQt6",
        "numpy",
        "matplotlib",
    ],
    package_data={
        "OSCR.ui": ["**/*.mplstyle"],
    },
    py_modules=["main"],
    entry_points={"console_scripts": ["OSCR=main:main"]},
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
