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
    web_example = "http", "https://support.oneskyapp.com/hc/en-us/article_attachments/202761627/example_1.json"


tests = ["yaml", "ini", "json", "toml", "hocon"]


@pytest.mark.parametrize("environment", tests)
def test_configs(environment):
    config = MyConfig("{}_example".format(environment))

    assert (not DeepDiff(config.raw(), test_against[0])) or (not DeepDiff(config.raw(), test_against[1]))


def test_no_env():
    with pytest.raises(ValueError):
        config = MyConfig("nonexistant_env")
