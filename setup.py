#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="deletme3D",
    version="0.0.1",
    description="DEep Learning Epithelial Tissue MEchanics",
    author="",
    author_email="",
    url="https://github.com/Wordam/deletme-pytorch",
    packages=find_packages(),
    # use this to customize global commands available in the terminal after installing the package
    entry_points={
        "console_scripts": [
            "train_command = deletme3D.train:main",
            "eval_command = deletme3D.eval:main",
        ]
    },
)
