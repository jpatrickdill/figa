from figa.loaders.parser import Parser
from pyhocon import ConfigFactory, HOCONConverter
import json


class HoconParser(Parser):
    def parse_string(self, s):
        conf = ConfigFactory.parse_string(s)
        return json.loads(HOCONConverter.to_json(conf))

    def parse_fp(self, fp):
        conf = ConfigFactory.parse_file(fp)
        return json.loads(HOCONConverter.to_json(conf))
