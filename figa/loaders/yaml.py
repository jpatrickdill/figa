from figa.loaders.default import Parser
import yaml


class YamlParser(Parser):
    def parse_file(self, file):
        return yaml.safe_load(file)
