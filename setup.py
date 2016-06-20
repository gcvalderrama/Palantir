# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Palantir',
    version='0.0.1',
    description='Extracting news information',
    long_description=readme,
    author='Gregory Valderrama',
    author_email='gcvalderrama@hotmail.com',
    url='https://github.com/gcvalderrama/Palantir',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

