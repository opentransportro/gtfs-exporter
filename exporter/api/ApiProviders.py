from exporter.Providers import DataProvider

class BucharestApiDataProvider(DataProvider):
    pass

class IasiApiDataProvider(DataProvider):
    pass


class ApiProviderBuilder:
    def __init__(self, provider: str):
        self.provider = provider

    def build(self) -> DataProvider:
        if self.provider == "bucharest":
            return BucharestApiDataProvider()
        else:
            return IasiApiDataProvider()
