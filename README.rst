Figa
====

Figa can read from multiple config sources including several file formats, environment variables,
and even the Internet, allowing you to configure your project however you want.

Figa supports many sources, including:

- Environment variables
- Dict objects
- JSON  (.json)
- HOCON  (.hocon, .conf)
- INI, CFG  (.ini, .cfg)
- YAML  (.yaml, .yml)
- TOML  (.toml)
- .properties  (.properties)
- Internet resources


.. code-block:: console

    $ pip install figa

Usage
-----

.. code-block:: py

    import figa

    @figa.config
    class MyConfig:
        development = "~/config.yml"  # use YAML file for config when developing
        production = "env", "cfg_"  # use environment variables with cfg_ prefix in production

    config = MyConfig("development")

    # config can be accessed using dots or indexing
    print(config.key == config["key"])  # True

Environment Detection
~~~~~~~~~~~~~~~~~~~~~

You can implement your own function that detects where to pull config values from.

.. code-block:: py

    @figa.config
    class Config:
        development = "~/config.yml"  # use YAML file for config when developing
        production = "env", "cfg_"  # use environment variables with cfg_ prefix in production

        def get_env(self):
            if "ON_HEROKU" in figa.env:  # figa.env is shortcut for os.environ
                return "production"
            else:
                return "development"

    config = Config()  # if no environment is passed, get_env() will be called.

File Types
~~~~~~~~~~

By default, the config file type will be guessed from the file extension.
This can also be set explicitly:

.. code-block:: python

    @figa.config
    class MyConfig:
        example = "ini", "./config.conf"
        # .conf would be detected as HOCON, but we set to INI

Default Values
~~~~~~~~~~~~~~

Default values can be set that will be included on every environment.

.. code-block:: python

    @figa.config
    class MyConfig:
        default = {"name": "My App"}

        dev = {"host": "localhost"}
        prod = {"host": "myapp.com"}

    dev_cfg = MyConfig("dev")
    prod_cfg = MyConfig("prod")

    assert dev_cfg.name == prod_cfg.name  # "name" config item is included in both

Required Values
~~~~~~~~~~~~~~~



This project is published under the MIT License. See ``LICENSE.md``.
