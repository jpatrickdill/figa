# readme basic

import figa


class MyConfig(figa.Config):
    # (optional) always included values. can be dict or any supported source
    default = {
        "test": "value"
    }

    development = "./config.yml"  # use YAML file for config when developing
    production = "env", "cfg_"  # use environment variables with cfg_ prefix in production

    def get_env(self):
        if figa.system == "windows":
            return "development"
        elif figa.system == "linux":
            return "production"


config = MyConfig()

# config can be accessed using dots or indexing
print(config.test == config["test"])  # True
