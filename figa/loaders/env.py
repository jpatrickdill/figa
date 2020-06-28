import os

from figa.loaders.default import BasicReader, DictValueReader
from figa.util import dict_merge


class EnvParser:
    def __init__(self, prefix="", default=None, required=None):
        self.reader = PrefixableReader(os.environ, prefix=prefix, default=default, required=required)

    @classmethod
    def __handler__(cls, *args, default=None, required=None):
        parser = cls(*args, default=default, required=required)
        return parser.reader


class PrefixableReader(DictValueReader):
    def __init__(self, values, prefix="", default=None, required=None):
        super().__init__(values, required=required)

        self._list = False

        self._prefix = prefix.lower()

        self._values = {}
        for k_, v in values.items():
            k = k_.lower()
            if k.startswith(self._prefix):
                self._values[k[len(self._prefix):]] = v

        if default is not None:
            self._values = dict_merge(default, self._values)

    def __getitem__(self, item):
        item = item.lower()

        if item in self._values:
            val = self._values[item]
            if isinstance(val, dict) or isinstance(val, list):
                return BasicReader(val)
            else:
                return val
        else:
            # see if key could be a sub-dictionary
            new_prefix = item + "_"
            for key in self._values.keys():
                if key.startswith(new_prefix):
                    return PrefixableReader(self._values, prefix=new_prefix)

            # no potential value
            raise KeyError(item)

