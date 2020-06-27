from pathlib import Path
from figa.util import dict_merge


class Parser:
    def __init__(self, *args):
        pass

    @classmethod
    def __handler__(cls, fp, *args, default=None):
        parser = cls(*args)

        path = Path(fp).resolve()

        if not path.is_file():
            raise FileNotFoundError("{} does not exist ({})".format(fp, path.absolute()))

        s_path = str(path)
        try:
            data = parser.parse_fp(s_path)
        except NotImplementedError:
            file = open(s_path, "r")

            try:
                data = parser.parse_file(file)
            except NotImplementedError:
                data = parser.parse_string(file.read())

            file.close()

        return BasicReader(data, default=default)

    def parse_string(self, s):
        raise NotImplementedError

    def parse_file(self, file):
        return self.parse_string(file.read())

    def parse_fp(self, fp):
        with open(fp, "r") as file:
            return self.parse_file(file)


class DictValueReader:
    def __repr__(self):
        return repr(self._values)

    def __str__(self):
        return str(self._values)

    def __getitem__(self, item):
        if self._list:
            val = self._values[item]
        else:
            val = self._values[item.lower()]

        if isinstance(val, dict) or isinstance(val, list):
            return BasicReader(val)
        else:
            return val

    def __contains__(self, item):
        if self._list:
            return item in self._values
        else:
            return item.lower() in self._values

    def __len__(self):
        return len(self._values)

    def keys(self):
        return self._values.keys()

    def values(self):
        return [self[key] for key in self.keys()]

    def items(self):
        return [(key, self[key]) for key in self.keys()]

    def __getattr__(self, item):
        return self[item]


class BasicReader(DictValueReader):
    def __init__(self, values, default=None):
        self._list = isinstance(values, list)

        if self._list:
            self._values = values
        else:
            if default is not None:
                values = dict_merge(default, values)

            self._values = {}
            for k, v in values.items():
                self._values[k.lower()] = v
