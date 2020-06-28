import platform
from functools import wraps

from figa.loaders import detect_and_parse
from figa.loaders.default import BasicReader, DictValueReader
from os import environ as env

# ease of use

system = platform.system().lower()
version = platform.python_version()


def config(cls):
    @wraps(cls)
    def get_config(environment: str = None) -> DictValueReader:
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

        default = get_config("default")._values if environment != "default" and hasattr(cls, "default") else None

        if isinstance(args[0], dict):  # dict object
            return BasicReader(args[0], default=default)
        elif isinstance(args[0], str):  # string parser name
            parsed = detect_and_parse(args, default=default)
        else:
            parsed = args[0].__handler__(*args[1:], default=default)  # parser specified explicitly

        return parsed

    return get_config
