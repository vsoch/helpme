#!/usr/bin/env python

"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from setuptools import setup, find_packages
import codecs
import os


# HELPER FUNCTIONS #############################################################


def get_lookup():
    lookup = dict()
    version_file = os.path.join("helpme", "version.py")
    with open(version_file) as filey:
        exec(filey.read(), lookup)
    return lookup


# Read in requirements


def get_reqs(lookup=None, key="INSTALL_REQUIRES"):
    """get requirements, meaning reading in requirements and versions from
    the lookup obtained with get_lookup"""

    if lookup == None:
        lookup = get_lookup()

    install_requires = []
    for module in lookup[key]:
        module_name = module[0]
        module_meta = module[1]
        if "exact_version" in module_meta:
            dependency = "%s==%s" % (module_name, module_meta["exact_version"])
        elif "min_version" in module_meta:
            if module_meta["min_version"] == None:
                dependency = module_name
            else:
                dependency = "%s>=%s" % (module_name, module_meta["min_version"])
        install_requires.append(dependency)
    return install_requires


# Make sure everything is relative to setup.py
install_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(install_path)

# Get version information from the lookup
lookup = get_lookup()
VERSION = lookup["__version__"]
NAME = lookup["NAME"]
AUTHOR = lookup["AUTHOR"]
AUTHOR_EMAIL = lookup["AUTHOR_EMAIL"]
PACKAGE_URL = lookup["PACKAGE_URL"]
KEYWORDS = lookup["KEYWORDS"]
DESCRIPTION = lookup["DESCRIPTION"]
LICENSE = lookup["LICENSE"]
with open("README.md") as filey:
    LONG_DESCRIPTION = filey.read()


# MAIN #########################################################################


if __name__ == "__main__":

    INSTALL_REQUIRES = get_reqs(lookup, "INSTALL_ALL")
    INSTALL_USERVOICE = get_reqs(lookup, "INSTALL_USERVOICE")
    INSTALL_ASCIINEMA = get_reqs(lookup, "INSTALL_ASCIINEMA")
    INSTALL_DISCOURSE = get_reqs(lookup, "INSTALL_DISCOURSE")

    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        url=PACKAGE_URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        keywords=KEYWORDS,
        install_requires=INSTALL_REQUIRES,
        extras_require={
            "all": [INSTALL_REQUIRES],
            "asciinema": [INSTALL_ASCIINEMA],
            "uservoice": [INSTALL_USERVOICE],
            "discourse": [INSTALL_DISCOURSE],
        },
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            "Programming Language :: C",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Topic :: Scientific/Engineering",
            "Operating System :: Unix",
            "Programming Language :: Python :: 3",
        ],
        entry_points={"console_scripts": ["helpme=helpme.client:main"]},
    )
