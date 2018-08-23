import pytest

from click.testing import CliRunner
from gaia import gaia


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(gaia.cli)
    assert result.output == 'Hello World!\n'
