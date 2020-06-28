import platform
from functools import wraps

from figa.loaders import detect_and_parse
from figa.loaders.default import BasicReader, DictValueReader
from os import environ as env

# ease of use

system = platform.system().lower()
version = platform.python_version()

no_warnings = False


def config(cls):
    # add __required__ if not included
    cls.__required__ = getattr(cls, "__required__", {})


    @wraps(cls)
    def get_config(environment: str = None, **kwargs) -> DictValueReader:
        no_warn = kwargs.get("no_warnings", no_warnings)

        # detect env
        if environment is None:
            if not hasattr(cls, "get_env"):
                raise NotImplementedError("No get_env() method defined, can't detect environment")

            environment = cls.get_env(cls)

            if environment is None:
                raise ValueError("No environment was provided or could be detected")

        # find config arguments
        args = getattr(cls, environment, None)
        if args is None:
            raise ValueError("No environment named {!r}".format(environment))
        if not isinstance(args, tuple):
            args = (args,)

        # get default values if not currently default
        default = get_config("default")._values if environment != "default" and hasattr(cls, "default") else None

        # get reader
        if isinstance(args[0], dict):  # dict object
            return BasicReader(args[0], default=default, required=cls.__required__)
        elif isinstance(args[0], str):  # string parser name
            parsed = detect_and_parse(args, default=default, required=cls.__required__, no_warnings=no_warn)
        else:
            # parser specified explicitly
            parsed = args[0].__handler__(*args[1:], default=default, required=cls.__required__, no_warnings=no_warn)

        return parsed

    return get_config
