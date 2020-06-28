import os
import sys
from pathlib import Path

sys.path.append(r"C:\Users\Patrick\PycharmProjects\figa")

import pytest
from deepdiff import DeepDiff  # required to run tests
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


config_root = Path(r"C:\Users\Patrick\PycharmProjects\figa\tests")


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
        }
    }
    without_types = {
        "number": "10",
        "string": "Hello world!",
        "fruits": ["apple", "pear"],
        "person": {
            "name": "Mark",
            "age": "64"
        }
    }


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


@pytest.mark.parametrize("environment", ["with_types", "without_types"])
def test_requires(environment):
    # checks that creating a valid config using __required__ will not raise an error

    with not_raises(ValueError):
        config = WithRequired(environment)


@pytest.mark.parametrize("environment", ["missing_arg", "fails_typecheck"])
def test_requires_fails(environment):
    # checks that a config that doesn't include every required item will fail

    with pytest.raises(ValueError):
        config = RequiredFails(environment)
