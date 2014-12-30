
geoip-lastlog
=============

Geolocation for motd / ssh last login based on lastlog

.. image:: https://pypip.in/download/geoip_lastlog/badge.png
    :target: https://pypi.python.org/pypi/geoip-lastlog/
    :alt: Downloads

.. image:: https://pypip.in/version/geoip_lastlog/badge.png
    :target: https://pypi.python.org/pypi/geoip-lastlog/
    :alt: Latest Version

.. image:: https://pypip.in/license/geoip_lastlog/badge.png
    :target: https://pypi.python.org/pypi/geoip-lastlog/
    :alt: License

Rationale
---------

SSH's "Last login" message is a security feature meant to help you spot unauthorized logins.
Yet, remembering login times and IP addresses is not easy.

geoip-lastlog is here to help you by: 

* geolocalizing the country and city
* printing "humanized" login times
* detecting connections from Tor exit nodes

Installation
------------

On Debian and its derivatives, install the dependencies:

   $ apt-get install python-arrow python-geoip geoip-database-contrib python-utmp

geoip-database-contrib provides geolocation at city level. In alternative, you can install geoip-database which provides only the country names:

   $ apt-get install python-arrow python-geoip geoip-database

Then, install geoip-lastlog from GitHub or from PyPI:

   $ git clone git://github.com/FedericoCeratto/geoip-lastlog

or use the handy pypi-install tool:

   $ sudo pypi-install geoip-lastlog

or, create a virtualenv and then fetch it from PyPI:

   $ pip install geoip-lastlog


Usage
-----

Add the script to the end of your /etc/profile

   /<fullpath>/geoip_lastlog.py

Optionally, you can specify how many entries to print:

   /<fullpath>/geoip_lastlog.py <N>

Use -h for help and -H to "humanize" the time since the last logins (see examples).

Use -t to flag if the IP address belongs to a Tor exit node.
To use this feature you have to fetch the exit node list from https://check.torproject.org/exit-addresses

Examples
--------

Default configuration::

   $ ssh somehost
   Last login: Wed Oct 29 14:43:06 2014 tom from 12.34.56.78 Ireland, Dublin
 
Configured to print 3 logins, with humanized time and Tor detection.::

   $ ssh somehost
    Last logins: 30 minutes ago tom from 12.34.56.78 Ireland, Dublin
                18 minutes ago tom from 162.247.72.217 United States, New York [tor]
                just now tom from 178.20.55.18 France [tor]
