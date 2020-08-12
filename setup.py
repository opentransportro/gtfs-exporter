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
        'Programming Language :: Python :: 3.6',
    ],
    keywords='GTFS transit exporter',
    packages=find_packages(),
    install_requires=['clint', 'pandas', 'pygithub', 'environs', 'polyline', 'ratelimit', 'sqlalchemy', 'six', 'docopt', 'requests', 'pyqtree', 'pyshp'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'gtfs-process=exporter.static:main',
        ],
    },
)
