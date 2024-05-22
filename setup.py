import os
import sys

base_directory = os.path.dirname(__file__)

try:
    from setuptools import setup, find_packages
except ImportError:
    print('This project needs setuptools in order to build. Install it using your package')
    print('manager (usually python-setuptools) or via pip (pip install setuptools).')
    sys.exit(1)

try:
    with open(os.path.join(base_directory, 'README.md')) as file_h:
        long_description = file_h.read()
except OSError:
    sys.stderr.write('README.md is unavailable, cannot generate the long description\n')
    long_description = None

DESCRIPTION = """\
Parse nmap files according the the README
"""

setup(
    name='nmapy',
    version='0.0.0',
    packages=find_packages(),
    author='Skyler Knecht',
    author_email='skyler.knecht@outlook.com',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/skylerknecht/nmapy',
    license='BSD-3-Clause',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    scripts=['run_nmapy']
)
