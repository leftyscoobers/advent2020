#!/usr/bin/env python3
# coding:utf-8

from setuptools import setup, find_packages

with open('advent2020/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")

setup(
    name='advent2020',
    version=version,
    packages=find_packages(include=['advent*'], utils),
    python_requires='>=3.6',
    install_requires=[
        'matplotlib>=3.1.0',
        'numpy',
        'pandas',
    ],
    extras_require={
        'dev': [
            'twine==1.10.0',
            'setuptools==38.5.2',
            'wheel==0.30.0',
            'Sphinx',
            'pytest',
            'astroid==2.2.5',
            'pylint==2.3.1'
        ]
    },
    entry_points={}
)
