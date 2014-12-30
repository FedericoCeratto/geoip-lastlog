# Functional tests
#
# Copyright (C) 2014 Federico Ceratto
# Released under AGPLv3+ license, see LICENSE

import pytest
import geoip_lastlog

ut_addr_v6_test_data = (
    ((432532482, 0, 0, 0), '2.236.199.25'),
    ((-358490843, 0, 0, 0), '37.221.161.234'),
    ((34014986, 0, 0, 0), '10.7.7.2'),
    ((288, 1275505235, -912671968, 327825832), '2001:0:53aa:64c:20bb:99c9:a839:8a13'),
    ((0, 0, 0, 0), '0.0.0.0'),
)

@pytest.fixture(params=ut_addr_v6_test_data)
def v6_sample(request):
    return request.param

@pytest.fixture
def mock_out_GEOIP_CITY_PATH(monkeypatch):
    monkeypatch.setattr('geoip_lastlog.GEOIP_CITY_PATH', '_not_a_real_file_')



def test_convert_ut_addr_v6(v6_sample):
    v6, expected = v6_sample
    assert geoip_lastlog.convert_ut_addr_v6(v6) == expected


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
        (1234567890, 'should_not_appear', '127.0.0.1', (0, 0, 0, 0)),
        (1234567891, 'local_user', 'localhost', (0, 0, 0, 0)),
        (1234567892, 'user', 'some.host.name', (34014986, 0, 0, 0)),  # 10.7.7.2
        (1234567892, 'mosh_user', '1.2.3.4 via mosh [1234]', (0 , 0, 0, 0)),
        (1234567893, 'tor_user', 'tor.node.name', (-358490843, 0, 0, 0)),  # 37.221.161.234
        (1234567894, 'ipv6_user', 'ipv6.host.name', (288, 1275505235, -912671968, 327825832)),
            # 2001:0:53aa:64c:20bb:99c9:a839:8a13
    )
    output = geoip_lastlog.geolocate_and_format(
        logins,
        5,
        'tests/data/exit-addresses',
        False
    )
    assert output == [
        u'Last logins: Fri Feb 13 23:31:31 2009 local_user from localhost',
        u'             Fri Feb 13 23:31:32 2009 user from some.host.name',
        u'             Fri Feb 13 23:31:32 2009 mosh_user from 1.2.3.4 via mosh [1234] United States, Mukilteo',
        u'             Fri Feb 13 23:31:33 2009 tor_user from tor.node.name Romania',
        u'             Fri Feb 13 23:31:34 2009 ipv6_user from ipv6.host.name']
