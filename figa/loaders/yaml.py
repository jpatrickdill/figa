from figa.loaders.parser import Parser
import yaml


class YamlParser(Parser):
    def parse_file(self, file):
        return yaml.safe_load(file)
