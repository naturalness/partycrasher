# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages


def slurp(filename):
    with open(filename) as text_file:
        return text_file.read()


setup(
    name='partycrasher',
    version='0.1.0-dev0',
    packages=find_packages(),
    author='Joshua Charles Campbell, Eddie Antonio Santos',
    license='GPLv3+',
    long_description=slurp('README.md'),
    install_requires=slurp('requirements.txt').splitlines(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'requests'],
)
