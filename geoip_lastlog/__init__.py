#!/usr/bin/env python
#
# Geolocalization for MOTD / SSH last login
#
# Copyright (C) 2014 Federico Ceratto
# Released under AGPLv3+ license, see LICENSE

from argparse import ArgumentParser
import GeoIP
import UTMPCONST
import arrow
import os.path
import socket
import struct
import utmp

GEOIP_PATH = "/usr/share/GeoIP/GeoIP.dat"
GEOIP_CITY_PATH = '/usr/share/GeoIP/GeoLiteCity.dat'


def convert_ut_addr_v6(v6):
    """Convert ut_addr_v6 structure"""
    if v6[1:] == (0, 0, 0):
        v4 = v6[0]
        p = struct.pack('i', v4)
        return socket.inet_ntoa(p)

    else:
        p = struct.pack('4i', *v6)
        return socket.inet_ntop(socket.AF_INET6, p)


def extract_ip_addr(ut_user, ut_addr_v6):
    if ut_addr_v6 == (0, 0, 0, 0):
        if ' via mosh ' in ut_user:
            # Mosh sets ut_user to "<ipaddr> via mosh ..."
            return ut_user.split()[0]

        return None  # local connection

    # IPv4 or IPV6
    return convert_ut_addr_v6(ut_addr_v6)


def load_tor_exit_nodes(fname):
    """Load Tor exit nodes IP addresses"""
    with open(fname) as f:
        addrs = set(
            line.split()[1]
            for line in f
            if line.startswith('ExitAddress')
        )

    return addrs


def load_wtmp_file():
    """Parse wtmp file and extract login data
    """
    logins = []
    wf = utmp.UtmpRecord(UTMPCONST.WTMP_FILE)
    while True:
        user = wf.getutent()
        if not user:
            break

        if user[0] == UTMPCONST.USER_PROCESS:
            logins.append((user.ut_tv[0], user.ut_user, user.ut_host,
                           user.ut_addr_v6))

    wf.endutent()
    return sorted(logins)


class Geolocator(object):
    def __init__(self):
        if os.path.isfile(GEOIP_CITY_PATH):
            self._geodb = GeoIP.open(GEOIP_CITY_PATH, GeoIP.GEOIP_MEMORY_CACHE)
        else:
            self._geodb = GeoIP.open(GEOIP_PATH, GeoIP.GEOIP_MEMORY_CACHE)

    def locate_address(self, addr):
        """Check if the argument is an IP address and try to geolocate it

        :returns: dict
        """
        if not addr:
            return {}

        if 'City Edition' in self._geodb.database_edition:
            # City Edition supports record_by_addr
            return self._geodb.record_by_addr(addr)

        elif 'Country Edition' in self._geodb.database_edition:
            # it's a Country Edition, use country_name_by_addr
            country_name = self._geodb.country_name_by_addr(addr)
            return dict(country_name=country_name)


def geolocate_and_format(logins, max_logins, tor, humanize_date):
    """Geolocate logins and format for printing"""
    output = []
    logins = logins[-max_logins:]
    gl = Geolocator()

    if tor:
        tor_ip_addrs = load_tor_exit_nodes(tor)

    for i, login_data in enumerate(logins):
        if i == 0 and max_logins == 1:
            line = 'Last login: '
        elif i == 0:
            line = 'Last logins: '
        else:
            line = '             '

        date, login_name, ut_user, ut_addr_v6 = login_data
        date = arrow.get(date)
        ipaddr = extract_ip_addr(ut_user, ut_addr_v6)
        location = gl.locate_address(ipaddr)
        if humanize_date:
            date = date.humanize()
        else:
            date = date.format('ddd MMM DD HH:mm:ss YYYY')

        line += "%s %s" % (date, login_name)
        if ut_user:
            line += " from %s" % ut_user

        if location and  location['country_name']:
            line += " %s" % location['country_name']

            if location.get('city', None) is not None:
                line += ", %s" % location['city']

        if tor and ipaddr in tor_ip_addrs:
            line += ' [tor]'

        output.append(line)

    return output


def parse_args():  # pragma: no cover
    ap = ArgumentParser()
    ap.add_argument('n', nargs='?', default=1, type=int,
                    help="Number of lines to print")
    ap.add_argument('-H', '--humanize', action='store_true',
                    help="Humanize login date")
    ap.add_argument('-t', '--tor', nargs='?',
                    const='/var/lib/geoip-lastlog/exit-addresses',
                    default=False, help="Guess Tor exit nodes")
    return ap.parse_args()


def main():
    args = parse_args()

    logins = load_wtmp_file()

    output = geolocate_and_format(logins, args.n, args.tor, args.humanize)
    for o in output:
        print o

if __name__ == '__main__':
    main()
