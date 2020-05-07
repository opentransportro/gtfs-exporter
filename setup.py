"""
@author: Vlad Vesa <vlad@opentransport.ro>
"""

from setuptools import setup, find_packages
import exporter


setup(
    name='gtfs-exporter',
    version=exporter.__version__,
    description="GTFS processing app",
    long_description="An open source library for reading, databasing, querying and manipulating GTFS-based transit data",
    url='https://github.com/opentransportro/gtfs-exporter',
    author='VLAD VESA',
    author_email='vlad@opentransport.ro',
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    keywords='GTFS transit exporter',
    packages=find_packages(),
    install_requires=['gtfslib', 'clint', 'pandas'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'gtfsprocess=exporter.main:main',
        ],
    },
)