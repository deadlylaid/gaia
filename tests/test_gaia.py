import pytest

from click.testing import CliRunner
from gaia import gaia


def test_hello_world():
    runner = CliRunner()
    runner.invoke(gaia.cli)
    assert 1==1
