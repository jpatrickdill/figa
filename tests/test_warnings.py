from pathlib import Path

import pytest
import figa

config_root = Path(r"C:\Users\Patrick\PycharmProjects\figa\tests")


@figa.config
class Config:
    ignored = str(config_root / "ignored.conf")
    not_ignored = str(config_root / "config.conf")


def test_ignored():
    # checks that a non-ignored file raises a warning

    with pytest.warns(UserWarning):
        cfg = Config("not_ignored")


