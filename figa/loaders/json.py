from figa.loaders.parser import Parser
import json


class JSONParser(Parser):
    def parse_string(self, s):
        return json.loads(s)
