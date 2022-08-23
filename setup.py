#!/usr/bin/env python
"""
Builds wheel for the project
"""

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()


def parse_requirements(requirements_path):
    """
    Parse the given file and remove all lines starting with '#' as per
    requirements.txt specs. It does not support all valid values in a
    requirements file, only those that can be easily substituted into the
    install_requires setuptools attr
    :param requirements_path: a path to a requirements file
    :return: a list of the string representations of requirements
    """
    requirements = []
    for line in open(requirements_path):
        line = line.strip()
        if line.startswith("--index") or line.startswith("#") or not line:
            continue

        if line.startswith("-r"):
            requirements.extend(parse_requirements(line[3:]))

        if line.startswith("-"):
            raise Exception("Invalid package name in %s" % requirements_path)

        requirements.append(line.split("#")[0])
    return requirements


setup(
    name="synology_cloudflare_ddns",
    version="0.0.1",
    description="cloudflare dns plugin for synology ddns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=parse_requirements("requirements.txt"),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "synology_cloudflare_ddns=synology_cloudflare_ddns.__main__:main"
        ]
    },
)
