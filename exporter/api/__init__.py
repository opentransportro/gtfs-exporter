from exporter.api.radcom import BucharestApiDataProvider, ConstantaApiDataProvider
from exporter.api.cluj import ClujApiDataProvider
from exporter.api.iasi import IasiApiDataProvider
from exporter.api.brasov import BrasovApiDataProvider
from exporter.provider import ApiDataProvider


class ApiBuilder:
    def __init__(
        self,
        provider: str,
        feed_id="",
        lenient=False,
        disable_normalization=False,
        **kwargs
    ):
        self.provider = provider
        self.feed_id = feed_id
        self.lenient = lenient
        self.disable_normalization = disable_normalization
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def build(self) -> ApiDataProvider:
        switcher = {
            "bucharest": BucharestApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
            "constanta": ConstantaApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
            "iasi": IasiApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
            "cluj": ClujApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
            "brasov": BrasovApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
        }

        return switcher.get(self.provider)
