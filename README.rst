Figa
====

Figa makes it easy to configure your app on multiple environments.

Figa can read from multiple sources including several file formats, environment variables,
and even the Internet, allowing you to configure your project however you want.

Installation
------------

Install from PyPA:

.. code-block:: console

    $ pip install figa

Example
-------



.. code-block:: py

    import figa


    class MyConfig(figa.Config):
        development = "~/config.yml"  # use YAML file for config when developing
        production = "env", "cfg_"  # use environment variables with cfg_ prefix in production

        def get_env(self):
            if "PRODUCTION" in figa.env:  # use environment variable we set as signal for prod. environment
                return "production"
            else:
                return "development"


    config = MyConfig()

    # config can be accessed using dots or indexing
    print(config.key == config["key"])  # True

    # configurations can be accessed explicitly
    dev_cfg = MyConfig("development")
    prod_cfg = MyConfig("production")


Figa supports many configuration sources, including:

- Environment variables
- Dict objects
- JSON  (.json)
- HOCON  (.hocon, .conf)
- INI, CFG  (.ini, .cfg)
- YAML  (.yaml, .yml)
- TOML  (.toml)
- .properties  (.properties)
- Internet resources

Data types can be set explicitly or guessed from the file extension.

.. code-block:: python

    class MyConfig(figa.Config):
        explicit_ex = "ini", "./config.conf"
        # .conf would be detected as HOCON, but we set to INI

