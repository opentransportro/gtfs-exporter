import pytest
import json
from os.path import abspath, dirname
from unittest import mock

from gtfslib.dao import Dao

from exporter.api.radcom import RadcomApiDataProvider
from exporter.api.brasov import BrasovApiDataProvider

base_path = dirname(abspath(__file__))


class MockedLinesDetailsRequest:
    def __call__(self, *args):
        with open(base_path + "/data/providers/radcom/lines.json") as f:
            return json.load(f)


class MockedLineInfoDetailsRequest:
    def __call__(self, *args):
        with open(base_path + "/data/providers/radcom/lines_{0}_direction_{1}.json".format(*args)) as f:
            return json.load(f)


class MockedLineStopDetailsRequest:
    def __call__(self, *args):
        with open(base_path + "/data/providers/radcom/lines_{0}_stops_{1}.json".format(*args)) as f:
            return json.load(f)


def _request_mock(url):
    if(url == "/lines/"):
        return MockedLinesDetailsRequest()

    if(url == "/lines/{0}/direction/{1}"):
        return MockedLineInfoDetailsRequest()

    if(url == "/lines/{0}/stops/{1}"):
        return MockedLineStopDetailsRequest()

    return None


@mock.patch("exporter.api.radcom.Request")
def test_radcom_provider(mocked_request, dao_fixture: Dao):
    mocked_request.side_effect = _request_mock
    radcomProvider = RadcomApiDataProvider("", feed_id="1")
    assert radcomProvider is not None

    # load data from provider
    load_result = radcomProvider.load_data_source(dao_fixture)
    assert load_result is True

    # check calendars
    assert len(dao_fixture.calendars()) == 2

    # check routes
    routes_len = 0
    for route in dao_fixture.routes():
        routes_len = routes_len + 1
        assert route.route_id == '43'
        assert route.route_short_name == '1'
        assert route.route_long_name == 'Bulevardul Tomis - Sere (C.L.)'
    assert routes_len == 1

    # check stops
    stops_len = 0
    for stop in dao_fixture.stops():
        stops_len = stops_len + 1
        assert len(stop.stop_times) > 0
        assert stop.stop_lat != 0.0
        assert stop.stop_lon != 0.0
    assert stops_len == 35

    # check trips
    trips_len = 0
    for trip in dao_fixture.trips():
        trips_len = trips_len + 1
        assert trip.shape != None
        expected_shape_id = "shp1_{0}_{1}".format(trip.route_id, trip.direction_id)
        assert trip.shape_id == expected_shape_id
    assert trips_len == 14

    # cleanup
    dao_fixture.delete_feed('1')
    dao_fixture.flush()


def test_brasov_export(dao_fixture: Dao):
    provider = BrasovApiDataProvider("2")
    provider.dao = dao_fixture

    provider._load_agencies()
    assert provider.agency_id is not None
    assert len(dao_fixture.agencies()) == 1

    provider._load_service()
    assert len(dao_fixture.calendars()) == 2

    assert len(provider.routes) == 0
    provider._load_routes()
    assert len(provider.routes) > 0
    assert len(dao_fixture.routes()) > 0

    assert len(provider.stop_map) == 0
    provider._load_schedule()
    assert len(provider.stop_map) > 0
    assert len(list(dao_fixture.stops())) > 0
    assert len(list(dao_fixture.trips())) > 0

    # stops_visited_by_route_trips = len(list(dao_fixture.stops()))
    # provider._load_stops()
    # assert len(list(dao_fixture.stops())) == stops_visited_by_route_trips

    # cleanup
    dao_fixture.delete_feed('2')
    dao_fixture.flush()