from figa.loaders.default import Parser
import json


class JSONParser(Parser):
    def parse_string(self, s):
        return json.loads(s)
