import pytest
import figa


class MyConfig(figa.Config):
    # default = "./config.yml"

    yaml_example = "./config.yml"
    ini_example = "./config.ini"
    json_example = "./config.json"
    toml_example = "./config.toml"
    hocon_example = "./config.conf"

    env_example = "env", "cfg_"  # environment variables with cfg_ prefix
    web_example = "http", "https://support.oneskyapp.com/hc/en-us/article_attachments/202761627/example_1.json"


config = MyConfig("hocon_example")
