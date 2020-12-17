"""
@author: Vlad Vesa <vlad@opentransport.ro>
"""

from setuptools import setup, find_packages

setup(
    name='gtfs-exporter',
    version="1.0.0",
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
        'Programming Language :: Python :: 3.7',
    ],
    keywords='GTFS transit exporter',
    packages=find_packages(),
    install_requires=[
        "python>=3.7"
        "requests==2.23.*"
        "polyline==1.4.*"
        "PyGithub==1.51.*"
        "docopt==0.6.*"
        "environs==7.4.*"
        "clint==0.5.1"
        "ratelimit==2.2.1"
        "pandas==1.0.3"
        "dateutils==0.6.8"
        "sqlalchemy==1.3.18"
        "six==1.15.0"
        "pyshp==2.1.0"
        "pyqtree==1.0.0"
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'gtfs-process=exporter.main:main',
        ],
    },
)
