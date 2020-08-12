import json
import unittest
from os.path import abspath, dirname
from unittest import mock

from sqlalchemy.orm import clear_mappers

from exporter.static.providers import BrasovApiDataProvider
from exporter.static.providers import RadcomApiDataProvider
from exporter.gtfs.dao import Dao

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
    if url == "/lines/":
        return MockedLinesDetailsRequest()

    if url == "/lines/{0}/direction/{1}":
        return MockedLineInfoDetailsRequest()

    if url == "/lines/{0}/stops/{1}":
        return MockedLineStopDetailsRequest()

    return None


class TestProviders(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        clear_mappers()
        self.dao_object = Dao()

    @mock.patch("exporter.static.providers.Request")
    def test_radcom_provider(self, mocked_request):
        mocked_request.side_effect = _request_mock
        radcomProvider = RadcomApiDataProvider("", feed_id="1")
        assert radcomProvider is not None

        # load data from provider
        load_result = radcomProvider.load_data_source(self.dao_object)
        assert load_result is True

        # check calendars
        assert len(self.dao_object.calendars()) == 2

        # check routes
        routes_len = 0
        for route in self.dao_object.routes():
            routes_len = routes_len + 1
            assert route.route_id == '43'
            assert route.route_short_name == '1'
            assert route.route_long_name == 'Bulevardul Tomis - Sere (C.L.)'
        assert routes_len == 1

        # check stops
        stops_len = 0
        for stop in self.dao_object.stops():
            stops_len = stops_len + 1
            assert len(stop.stop_times) > 0
            assert stop.stop_lat != 0.0
            assert stop.stop_lon != 0.0
        assert stops_len == 35

        # check trips
        trips_len = 0
        for trip in self.dao_object.trips():
            trips_len = trips_len + 1
            assert trip.shape != None
            expected_shape_id = "shp1_{0}_{1}".format(trip.route_id, trip.direction_id)
            assert trip.shape_id == expected_shape_id
        assert trips_len == 14

        # cleanup
        self.dao_object.delete_feed('1')
        self.dao_object.flush()

    def test_brasov_export(self):
        provider = BrasovApiDataProvider("2")
        provider.dao = self.dao_object

        provider._load_agencies()
        assert provider.agency_id is not None
        assert len(self.dao_object.agencies()) == 1

        provider._load_service()
        assert len(self.dao_object.calendars()) == 2

        assert len(provider.routes) == 0
        provider._load_routes()
        assert len(provider.routes) > 0
        assert len(self.dao_object.routes()) > 0

        assert len(provider.stop_map) == 0
        provider._load_schedule()
        assert len(provider.stop_map) > 0
        assert len(list(self.dao_object.stops())) > 0
        assert len(list(self.dao_object.trips())) > 0

        # stops_visited_by_route_trips = len(list(dao_fixture.stops()))
        # provider._load_stops()
        # assert len(list(dao_fixture.stops())) == stops_visited_by_route_trips

        # cleanup
        self.dao_object.delete_feed('2')
        self.dao_object.flush()
