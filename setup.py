"""
Setup for Netrunner

"""

from setuptools import find_packages
import setuptools
import os

requirements_path = './requirements.txt'

# check if path exists
if os.path.isfile(requirements_path):
    with open(requirements_path) as file:
        install_requires = [package for package in file.read().splitlines()]

# setup
setuptools.setup(
    name='netrunner',
    packages=find_packages(),
    version='0.0.1',
    author='Chris Smith',
    install_requires=install_requires,
    tests_require=['pytest'],
    author_email='chrissmith700@gmail.com',
    description='Combine Networkx and Pandas for fast network creation and analysis'
)
