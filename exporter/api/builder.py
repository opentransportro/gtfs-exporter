from exporter.api.bucharest import BucharestApiDataProvider
from exporter.api.cluj import ClujApiDataProvider
from exporter.api.constanta import ConstantaApiDataProvider
from exporter.api.iasi import IasiApiDataProvider
from exporter.provider import ApiDataProvider


class ProviderBuilder:
    def __init__(self, provider: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        self.provider = provider
        self.feed_id = feed_id
        self.lenient = lenient
        self.disable_normalization = disable_normalization

    def build(self) -> ApiDataProvider:
        switcher = {
            'bucharest': BucharestApiDataProvider(self.feed_id, self.lenient, self.disable_normalization),
            'constanta': ConstantaApiDataProvider(self.feed_id, self.lenient, self.disable_normalization),
            'iasi': IasiApiDataProvider(self.feed_id, self.lenient, self.disable_normalization),
            'cluj': ClujApiDataProvider(feed_id=self.feed_id, lenient=self.lenient,
                                        disable_normalization=self.disable_normalization),
        }

        return switcher.get(self.provider)
