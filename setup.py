#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import re
from setuptools import find_packages, setup
from wheel.bdist_wheel import (
    bdist_wheel as _bdist_wheel,
    get_platform,
    get_abi_tag,
    tags,
)


def get_property(prop, project):
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        open(project + "/__init__.py").read(),
    )
    return result.group(1)


# Package meta-data.
NAME = "openvideo"
DESCRIPTION = "openvideo provides convenient dataset generators for the combinatorial optimization problem"
URL = "https://github.com/heatingma/OpenVideo"
AUTHOR = get_property("__author__", NAME)
VERSION = get_property("__version__", NAME)
REQUIRED = [
    "aiohttp>=3.9.3",
    "async_timeout>=4.0.3",
    "tqdm>=4.66.1",
    "texttable>=1.7.0",
    "moviepy>=1.0.3",
    "bs4>=0.0.2",
    "selenium>=4.19.0",
    "requests>=2.31.0",
    "huggingface_hub>=0.22.2",
    "opencv-python>=4.9.0.80",
    "scenedetect>=0.6.3"
]

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class BdistWheelCommand(_bdist_wheel):
    def get_tag(self):
        if self.plat_name and not self.plat_name.startswith("macosx"):
            plat_name = self.plat_name
        else:
            plat_name = get_platform(self.bdist_dir)
        if plat_name in ("linux-x86_64", "linux_x86_64"):
            plat_name = "manylinux2014_x86_64"
        plat_name = (
            plat_name.lower().replace("-", "_").replace(".", "_").replace(" ", "_")
        )
        impl_name = tags.interpreter_name()
        impl_ver = tags.interpreter_version()
        impl = impl_name + impl_ver
        abi_tag = str(get_abi_tag()).lower()
        tag = (impl, abi_tag, plat_name)
        return tag


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_data={NAME: ["**"], NAME: ["**"]},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="Mulan PSL v2",
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        "Environment :: Console",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    # $ setup.py publish support.
    cmdclass={
        "bdist_wheel": BdistWheelCommand,
    },
)
