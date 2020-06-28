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

    >>> config.key == config["key"]  # config can be accessed using dots or indexing
    True

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

    >>> config = Config()  # if no environment is passed, get_env() will be called.

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

    >>> dev_cfg = MyConfig("dev")
    >>> prod_cfg = MyConfig("prod")
    >>> dev_cfg.name == prod_cfg.name  # "name" config item is included in both
    True

Required Values and Type Checking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In your Config class you can set required values and types that will be checked when the
config is loaded. This helps ensure that your code doesn't run with missing information.

.. code-block:: python

    @figa.config
    class Config:
        # two required config values: `string` & `sub.number`
        __required__ = {
            "string": str,
            "sub": {
                "number": int
            }
        }

If any values are missing, an error will be raised:

.. code-block:: python

    @figa.config
    class Config:
        # two required config values: `string` & `sub.number`
        __required__ = {
            "string": str,
            "sub": {
                "number": int
            }
        }

        missing_vals = {  # this config is missing sub.number
            "string": "hello, world",
            "sub": {}
        }

    >>> cfg = Config("missing_vals")
    ValueError: Missing required item 'sub.number'

Figa will automatically convert strings and numbers for you where possible.

.. code-block:: python

    @figa.config
    class Config:
        __required__ = {
            "stringval": str,
            "numberval": int
        }

        values = {
            "stringval": 100,
            "numberval": "42"
        }

    >>> cfg = Config("values")
    >>> cfg.stringval
    '100'
    >>> cfg.numberval
    42


This project is published under the MIT License. See ``LICENSE.md``.
