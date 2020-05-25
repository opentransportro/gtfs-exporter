import ipdb
from gtfslib.dao import Dao

from exporter import __version__

from exporter.api.builder import ProviderBuilder
from exporter.api.brasov import BrasovApiDataProvider, midnight_today
from exporter.api.iasi import IasiApiDataProvider


def test_version():
    assert __version__ == "1.0.0"


def test_midnight():
    midnight = midnight_today("Europe/Bucharest")
    assert midnight.day > 0
    assert midnight.month > 0
    assert midnight.year > 0

    assert midnight.tzinfo is not None
    assert midnight.hour == 0
    assert midnight.minute == 0
    assert midnight.second == 0
    assert midnight.microsecond == 0


def test_provider_builder():
    builder = ProviderBuilder("unknown", f"unknown-feed")
    assert builder.build() is None

    for provider_key in ["bucharest", "constanta", "cluj", "brasov", "iasi"]:
        builder = ProviderBuilder(provider_key, f"{provider_key}-feed")
        provider = builder.build()
        assert provider is not None


def test_iasi_export():
    provider = IasiApiDataProvider("test")
    # provider._load_agencies()


def test_brasov_export(dao_fixture: Dao):
    provider = BrasovApiDataProvider("test")
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

    stops_visited_by_route_trips = len(list(dao_fixture.stops()))
    provider._load_stops()
    assert len(list(dao_fixture.stops())) == stops_visited_by_route_trips
