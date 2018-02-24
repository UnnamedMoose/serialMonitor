""" A setuptools-based setup module for the Serial Monitor.

Author: Aleksander Lidtke
URL: https://github.com/AleksanderLidtke
"""
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os

# Get the long description from the README file
with open(os.path.join(os.getcwd(), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get the version from a file, which is included with the distribution (listed in MANIFEST.in).
with open(os.path.join(os.getcwd(), 'VERSION'), encoding='utf-8') as version_file:
    ver=version_file.read().strip()

setup(
    name='SerialMonitor',
    version=ver, # Use the version from the file.

    description='Application that reads and writes to a serial port.',
    long_description=long_description, # From the README.md

    # The project's main homepage.
    url='https://github.com/UnnamedMoose/serialMonitor',

    # Author details
    author='Aleksander Lidtke',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: enthusiasts',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='serial port, serial monitor, logging, debugging',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['wxpython>=4.0.1','pyserial','logging'],

    extras_require={
        'dev': ['pdb'],
        'test': ['unittest'],
    },

    package_data={
    },

    # Automatically install the entry-point scripts.
    entry_points={
        'console_scripts': [
            'serialMonitor=SerialMonitor:main',
        ],
    },
)
