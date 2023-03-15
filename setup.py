
from setuptools import setup, find_packages

setup(
    name='gTiger',
    version='1.0.0',
    author='Hanming Tu',
    author_email='hanming.tu@gmail.com',
    description='A collection of utils for geoTiger project',
    long_description='This project includes a collection of common functions and procedures',
    url='https://github.com/htu/gTiger/utils',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy>=1.18.5',
        'pandas>=1.0.5',
        'matplotlib>=3.2.2',
    ],
)