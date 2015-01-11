from setuptools import setup, find_packages
import os

VERSION = '0.1'
LONG_DESCRIPTION = os.linesep.join([open('README.md').read()])

setup(
    name='pymongo_genomes',
    version=VERSION,

    author='Kensuke NUMAKURA',
    author_email='knmkr3gma+pip@gmail.com',

    description='Python library for handlig personal genome data in MongoDB.',
    long_description=LONG_DESCRIPTION,
    url='',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords=['bioinformatics', 'personal genome'],
    license='GNU AGPLv3',

    packages=find_packages(),
    # package_data={'pymongo-genomes': ['test/test_*']},
    entry_points={'console_scripts': ['pymongo_genomes = pymongo_genomes:main']},
    # test_suite='test.test_all'
)
