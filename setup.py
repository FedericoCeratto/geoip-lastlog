#!/usr/bin/env python

from setuptools import setup

__version__ = '0.6'

CLASSIFIERS = map(str.strip,
"""Environment :: Console
License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)
Natural Language :: English
Operating System :: POSIX :: Linux
Programming Language :: Python
Programming Language :: Python :: 2.7
Topic :: Security
""".splitlines())

setup(
    name="geoip-lastlog",
    version=__version__,
    author="Federico Ceratto",
    author_email="federico.ceratto@gmail.com",
    description="GeoIP-based location for the last logins",
    license="AGPLv3+",
    url="https://github.com/FedericoCeratto/geoip-lastlog",
    long_description="""Geolocalize IP addresses in user logins, typically SSH
traffic. Optionally detects SSH connections from Tor exit nodes.""",
    keywords="ssh security",
    classifiers=CLASSIFIERS,
    install_requires=[
        'setuptools',
        'arrow',
        'geoip',
    ],
    platforms=['Linux'],
    zip_safe=False,
    packages = ['geoip_lastlog'],
    entry_points = {
        'console_scripts': ['geoip-lastlog=geoip_lastlog:main'],
    },
)
