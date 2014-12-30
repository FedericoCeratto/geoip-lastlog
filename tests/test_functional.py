# Functional tests
#
# Copyright (C) 2014 Federico Ceratto
# Released under GPLv3+ license, see LICENSE

import pytest

import geoip_lastlog


@pytest.fixture
def mock_out_GEOIP_CITY_PATH(monkeypatch):
    monkeypatch.setattr('geoip_lastlog.GEOIP_CITY_PATH', None)


def test_load_tor_exit_nodes():
    addrs = geoip_lastlog.load_tor_exit_nodes('tests/data/exit-addresses')
    assert len(addrs) == 1216
    assert '1.120.132.14' in addrs


def test_load_real_wtmp_file():
    logins = geoip_lastlog.load_wtmp_file()
    assert logins


def test_geolocator():
    gl = geoip_lastlog.Geolocator()
    assert 'City Edition' in gl._geodb.database_edition
    d = gl.locate_address('8.8.8.8')
    assert d['country_name'] == 'United States'
    assert d['city'] == 'Mountain View'


def test_geolocator_without_city_edition(mock_out_GEOIP_CITY_PATH):
    gl = geoip_lastlog.Geolocator()
    assert 'Country Edition' in gl._geodb.database_edition
    d = gl.locate_address('8.8.8.8')
    assert d == {'country_name': 'United States'}


def test_geolocate_and_format():
    logins = (
        (1234567890, 'should_not_appear', '127.0.0.1'),
        (1234567891, 'localhost', '127.0.0.1'),
        (1234567892, 'eight', '8.8.8.8'),
        (1234567893, 'tor', '96.250.162.128'),
    )
    output = geoip_lastlog.geolocate_and_format(
        logins,
        3,
        'tests/data/exit-addresses',
        False
    )
    assert output == [
        'Last logins: Fri Feb 13 23:31:31 2009 localhost from 127.0.0.1',
        '             Fri Feb 13 23:31:32 2009 eight from 8.8.8.8 United States, Mountain View',
        '             Fri Feb 13 23:31:33 2009 tor from 96.250.162.128 United States, Yonkers [tor]'
    ]
