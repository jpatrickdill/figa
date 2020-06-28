import os
import sys
from pathlib import Path

sys.path.append(r"C:\Users\Patrick\PycharmProjects\figa")

import pytest
from deepdiff import DeepDiff  # required to run tests
import figa

# example files should match one of the following in their respective syntax:
test_against = ({
                    "number": 12,
                    "string": "Hello, world!",
                    "fruits": ["apple", "pear"],
                    "person": {
                        "name": "Zach",
                        "age": 20
                    }
                }, {
                    "number": "12",
                    "string": "Hello, world!",
                    "fruits": ["apple", "pear"],
                    "person": {
                        "name": "Zach",
                        "age": "20"
                    }
                })

config_root = Path(r"C:\Users\Patrick\PycharmProjects\figa\tests")


class MyConfig(figa.Config):
    # default = "./config.yml"

    yaml_example = str(config_root / "config.yml")
    ini_example = str(config_root / "config.ini")
    json_example = str(config_root / "config.json")
    toml_example = str(config_root / "config.toml")
    hocon_example = str(config_root / "config.conf")

    env_example = "env", "cfg_"  # environment variables with cfg_ prefix
    web_example = "http", "https://gist.githubusercontent.com/jpatrickdill/" \
                          "7941fc1b531e69dfd4fe96c3628c497b/raw/8c49dba146f533614bee2b85ac0aa379de79ca99/config.json"


tests = ["yaml", "ini", "json", "toml", "hocon", "web"]


@pytest.mark.parametrize("environment", tests)
def test_configs(environment):
    config = MyConfig("{}_example".format(environment))

    assert (not DeepDiff(config.raw(), test_against[0])) or (not DeepDiff(config.raw(), test_against[1]))


# noinspection PyTypeChecker
def test_env_vars():
    # environment variables to test
    env_vals = {
        "key": "env_value",
        "creds": {
            "user": "usernamehere",
            "pass": "supersecret"
        }
    }

    # set environment variables using _ prefix for sub-dicts
    def set_env(d, prefix=""):
        for k, v in d.items():
            if isinstance(v, dict):
                set_env(v, prefix=prefix + k + "_")
            else:
                os.environ[prefix + k] = str(v)

    # check using sub-dicts of original variables
    def env_eq(cfg, d):
        for k, v in d.items():
            if isinstance(v, dict):
                if not env_eq(cfg[k], d[k]):
                    return False

            elif str(v) != cfg[k]:
                return False

        return True

    set_env(env_vals, "cfg_")

    config = MyConfig("env_example")

    assert env_eq(config, env_vals)


def test_nonexistant_env():
    with pytest.raises(ValueError):
        config = MyConfig("nonexistant_env")
