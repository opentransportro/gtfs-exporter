from exporter import __version__

from exporter.api.builder import ProviderBuilder
from exporter.api.iasi import IasiApiDataProvider
from exporter.api.brasov import BrasovApiDataProvider


def test_version():
    assert __version__ == "1.0.0"


def test_provider_builder():
    builder = ProviderBuilder("unknown", f"unknown-feed")
    assert builder.build() is None

    for provider_key in ["bucharest", "constanta", "cluj", "brasov", "iasi"]:
        builder = ProviderBuilder(provider_key, f"{provider_key}-feed")
        provider = builder.build()
        assert provider is not None


def test_iasi_export():
    provider = IasiApiDataProvider("test")
    provider._load_agencies()


def test_brasov_export():
    provider = BrasovApiDataProvider("test")
    provider._load_agencies()
