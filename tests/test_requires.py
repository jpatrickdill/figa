import sys

sys.path.append(r"C:\Users\Patrick\PycharmProjects\figa")

import pytest
import figa
from contextlib import contextmanager


# testing utils
@contextmanager
def not_raises(expected):
    try:
        yield

    except expected as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


# tests

@figa.config
class WithRequired:
    __required__ = {
        "number": int,
        "string": str,
        "fruits": list,
        "person": {
            "name": str,
            "age": int
        }
    }

    with_types = {
        "number": 10,
        "string": "Hello world!",
        "fruits": ["apple", "pear"],
        "person": {
            "name": "Mark",
            "age": 64
        },
        "extra": "extra!"
    }
    without_types = {
        "number": "10",
        "string": "Hello world!",
        "fruits": ["apple", "pear"],
        "person": {
            "name": "Mark",
            "age": "64"
        },
        "extra": "extra!"
    }


@pytest.mark.parametrize("environment", ["with_types", "without_types"])
def test_requires(environment):
    # checks that creating a valid config using __required__ will not raise an error

    with not_raises(ValueError):
        config = WithRequired(environment)


@figa.config
class RequiredFails:
    __required__ = {
        "arg1": str,
        "arg2": str
    }

    missing_arg = {
        "arg1": "Hello world!"
    }
    fails_typecheck = {
        "arg1": [1, 2, 3],
        "arg2": "Hello, world!"
    }


@pytest.mark.parametrize("environment", ["missing_arg", "fails_typecheck"])
def test_requires_fails(environment):
    # checks that a config that doesn't include every required item will fail

    with pytest.raises(ValueError):
        config = RequiredFails(environment)


@figa.config
class ShouldConvert:
    __required__ = {
        "int": int,
        "string": str,
        "float1": float,
        "float2": float
    }

    test = {
        "int": "15",
        "string": 100,
        "float1": "42.42",
        "float2": 42
    }


def test_converts():
    # checks that values will be converted to __required__ types if possible

    config = ShouldConvert("test")

    assert config.int == 15
    assert config.string == "100"
