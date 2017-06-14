import sys
import os
try: 
    from setuptools import setup, find_packages
except ImportError: 
    from distutils.core import setup
    def find_packages():
        return []

import versioneer

if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[:2] < (3, 2):
    raise RuntimeError("Python version 2.7 or >= 3.2 required.")

NAME = 'local-volume-db'
CLASSIFIERS = """\
Development Status :: 2 - Pre-Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Natural Language :: English
Topic :: Scientific/Engineering
"""
URL = 'https://github.com/kadrlica/local-volume-db'
DESCR = "Module supporting a database of Local Volume galaxies"
LONG_DESCR = "See %s for more details."%URL

setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url=URL,
    author='Alex Drlica-Wagner',
    author_email='kadrlica@fnal.gov',
    scripts = [],
    install_requires=[
        'numpy >= 1.9.0',
        'pyyaml >= 3.10',
        'psycopg2'
    ],
    packages=find_packages(),
    package_data={},
    description=DESCR,
    long_description=LONG_DESCR,
    platforms='any',
    classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f]
)
