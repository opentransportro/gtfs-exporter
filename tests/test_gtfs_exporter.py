import unittest

from exporter import __version__
from exporter.api.brasov import midnight_today
from exporter.api import ApiBuilder


class TestGtfsExporter(unittest.TestCase):
    def setUp(self):
        pass

    def test_version(self):
        assert __version__ == "1.0.0"

    def test_midnight(self):
        midnight = midnight_today("Europe/Bucharest")
        assert midnight.day > 0
        assert midnight.month > 0
        assert midnight.year > 0

        assert midnight.tzinfo is not None
        assert midnight.hour == 0
        assert midnight.minute == 0
        assert midnight.second == 0
        assert midnight.microsecond == 0

    def test_provider_builder(self):
        builder = ApiBuilder("unknown", f"unknown-feed")
        assert builder.build() is None

        for provider_key in ["bucharest", "constanta", "cluj", "brasov", "iasi"]:
            builder = ApiBuilder(provider_key, f"{provider_key}-feed")
            provider = builder.build()
            assert provider is not None
