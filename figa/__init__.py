import platform
from figa.loaders import detect_and_parse
from figa.loaders.default import BasicReader
from os import environ as env

# ease of use

system = platform.system().lower()
version = platform.python_version()


# class

class Config:
    def __new__(cls, env=None):
        # detect env
        env = env or cls.get_env(cls)

        if env is None:
            raise ValueError("No environment was provided or could be detected")

        # find config arguments
        args = getattr(cls, env, None)
        if args is None:
            raise ValueError("No environment named {!r}".format(env))
        if not isinstance(args, tuple):
            args = (args,)

        default = cls("default")._values if env != "default" and hasattr(cls, "default") else None

        if isinstance(args[0], dict):  # dict object
            return BasicReader(args[0], default=default)
        elif isinstance(args[0], str):  # string parser name
            parsed = detect_and_parse(args, default=default)
        else:
            parsed = args[0].__handler__(*args[1:], default=default)  # parser specified explicitly

        return parsed

    def get_env(self):
        raise NotImplementedError("Environment can't be detected because no get_env() method was defined.")
