import sys
import os
import sys
import setuptools
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version

if StrictVersion(setuptools_version) < StrictVersion('38.3.0'):
    raise SystemExit(
        'Your `setuptools` version is old. '
        'Please upgrade setuptools by running `pip install -U setuptools` '
        'and try again.'
    )
def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='satadd',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/samapriya/satadd',
    install_requires=['gbdxtools>=0.15.12','Shapely>=1.6.4.post1','geopandas>=0.4.0','requests>=2.19.1','geojson>=2.4.0',
    'earthengine-api>=0.1.138','gitpython>=2.1.11','pendulum>=2.0.2','Pygments>=2.2.0'],
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Simple CLI for piping Planet, Satellogic & GBDX Assets',
    entry_points={
        'console_scripts': [
            'satadd=satadd.satadd:main',
        ],
    },
)
