#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="dare3d",
    version="0.0.1",
    description="Division Axis Recognition in 3d",
    author="Romain Karpinski, Marc Karnat, Alice Gros, JF Rupprecht",
    author_email="rupprecht.jf at gmail.com",
    url="h",
    packages=find_packages(),
    # use this to customize global commands available in the terminal after installing the package
    entry_points={
        "console_scripts": [
            "train_command = deletme3D.train:main",
            "eval_command = deletme3D.eval:main",
        ]
    },
)
