from exporter.provider import ApiDataProvider


class IasiApiDataProvider(ApiDataProvider):
    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__()
