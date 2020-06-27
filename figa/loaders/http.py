from figa.loaders.default import BasicReader
from figa.loaders import parsers_full
import requests


class HttpParser:
    def __init__(self, *args, default=None):
        url = args[-1]
        parser = args[-2] if len(args) > 1 else url.split(".")[-1]  # try to detect parser from URL

        if parser not in parsers_full:
            raise NotImplementedError("No parser found for {!r}".format(parser))

        parser = parsers_full[parser]("")

        data = requests.get(url)
        self.reader = BasicReader(parser.parse_string(data.text), default=default)

    @classmethod
    def __handler__(cls, *args, default=None):
        parser = cls(*args, default=default)
        return parser.reader
