import pytest
import os
import shutil
from click.testing import CliRunner
from gaia import gaia


def setup_module(module):
    if os.path.isfile('gaia_conf.json'):
        os.rename('gaia_conf.json', 'gaia_conf.json.real')
    shutil.copyfile('tests/gaia_conf.json.test', 'gaia_conf.json')

def teardown_module(module):
    os.rename('gaia_conf.json.real', 'gaia_conf.json')


@pytest.mark.parametrize('bucket',(
                         ('s3'),
                         ('undefined')
 ))
def test_hello_world(bucket):
    os.system('rm -rf logs')

    runner = CliRunner()
    result = runner.invoke(gaia.cli, ['find', bucket])

    path = 'logs/'+bucket
    assert os.path.isdir(path) == True