from exporter.provider import ApiDataProvider
from exporter.api.bucharest import BucharestApiDataProvider
from exporter.api.iasi import IasiApiDataProvider


class ProviderBuilder:
    def __init__(self, provider: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        self.provider = provider
        self.feed_id = feed_id
        self.lenient = lenient
        self.disable_normalization = disable_normalization

    def build(self) -> ApiDataProvider:
        if self.provider == "bucharest":
            return BucharestApiDataProvider(self.feed_id, self.lenient, self.disable_normalization)
        else:
            return IasiApiDataProvider(self.feed_id, self.lenient, self.disable_normalization)