from figa.loaders.default import Parser
import toml


class TomlParser(Parser):
    def parse_string(self, s):
        return toml.loads(s)
