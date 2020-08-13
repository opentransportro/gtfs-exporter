import unittest

from exporter import __version__
from exporter.static.providers import ApiProviderBuilder, BrasovApiDataProvider


class TestGtfsExporter(unittest.TestCase):
    def setUp(self):
        pass

    def test_version(self):
        assert __version__ == "1.1.0"

    def test_midnight(self):
        midnight = BrasovApiDataProvider.midnight_today("Europe/Bucharest")
        assert midnight.day > 0
        assert midnight.month > 0
        assert midnight.year > 0

        assert midnight.tzinfo is not None
        assert midnight.hour == 0
        assert midnight.minute == 0
        assert midnight.second == 0
        assert midnight.microsecond == 0

    def test_provider_builder(self):
        builder = ApiProviderBuilder("unknown", f"unknown-feed")
        assert builder.build() is None

        for provider_key in ["bucharest", "constanta", "cluj", "brasov"]:
            builder = ApiProviderBuilder(provider_key, f"{provider_key}-feed")
            provider = builder.build()
            assert provider is not None
