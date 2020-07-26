import ipdb
from exporter.gtfs.dao import Dao

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

