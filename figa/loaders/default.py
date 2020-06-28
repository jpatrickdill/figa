from pathlib import Path
from warnings import warn

from figa.util import dict_merge
from figa import typechecking
import subprocess


class Parser:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def __handler__(cls, fp, *args, default=None, required=None, **kwargs):
        parser = cls(*args, **kwargs)

        path = Path(fp).resolve()

        # check if config will be ignored and warn user if necessary
        if not kwargs.get("no_warnings"):
            try:
                ignored = subprocess.Popen(["git", "check-ignore", str(path)],
                                           stdout=subprocess.PIPE).communicate()[0].rstrip().decode("utf-8")

                if ignored == "":
                    warn("Config file {!r} isn't included in your .gitignore, meaning you could be exposing private"
                         " API keys in a public repository. To disable this warning, set figa.no_warnings = True"
                         .format(path.name))

            except FileNotFoundError:
                pass

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

        return BasicReader(data, default=default, required=required)

    def parse_string(self, s):
        raise NotImplementedError

    def parse_file(self, file):
        return self.parse_string(file.read())

    def parse_fp(self, fp):
        with open(fp, "r") as file:
            return self.parse_file(file)


class DictValueReader:
    def __init__(self, values, required=None):
        if required is not None:
            typechecking.check(required, values)

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

    def raw(self):
        return self._values

    def __getattr__(self, item):
        return self[item]


class BasicReader(DictValueReader):
    def __init__(self, values, default=None, required=None):
        super().__init__(values, required=required)

        self._list = isinstance(values, list)

        if self._list:
            self._values = values
        else:
            if default is not None:
                values = dict_merge(default, values)

            self._values = {}
            for k, v in values.items():
                self._values[k.lower()] = v
