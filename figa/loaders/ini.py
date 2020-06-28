from figa.loaders.parser import Parser
from configobj import ConfigObj
from io import StringIO


class IniParser(Parser):
    def parse_string(self, s):
        config = ConfigObj(s.splitlines())

        return config.dict()
