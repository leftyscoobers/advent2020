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
    packages=find_packages(include=['advent*', 'utils']),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
    ],
    extras_require={
        'dev': [
            'setuptools==38.5.2',
            'pytest',
        ]
    },
    entry_points={}
)
