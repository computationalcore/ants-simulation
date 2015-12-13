#! coding: utf-8
from setuptools import setup

# All versions
install_requires = [
    'configparser',
    'gameobjects',
    'pygame',
    'setuptools'
]

setup(
    name='Ants Simulation',
    version='0.1.0',
    description='.',
    author=[],
    author_email='computationalcore@gmail.com',
    url='',
    packages=[],
    install_requires=install_requires,
    dependency_links=['https://github.com/computationalcore/gameobjects/tarball/master#egg=package-0.0.3']
)