"""
@author: Vlad Vesa <vlad@opentransport.ro>
"""
import ast
import os
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open(os.path.join('exporter', '__init__.py')) as fh:
    for line in fh:
        if line.startswith('__version__'):
            __version__ = ast.parse(line).body[0].value.s

setuptools.setup(
    name='exporter',
    version=__version__,
    description="GTFS processing app",
    long_description=long_description,
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
    packages=setuptools.find_packages(),
    install_requires=[
        'pyinstaller',
        'packaging',
        "requests",
        "polyline",
        "PyGithub",
        "docopt",
        "environs",
        "clint",
        "ratelimit",
        "pandas",
        "dateutils",
        "sqlalchemy",
        "six",
        "pyshp",
        "pyqtree",
        'paramiko',
        'scp'
    ],
    entry_points = {
        'console_scripts': [
            'exporter=exporter.static:main',
        ],
    },
)
