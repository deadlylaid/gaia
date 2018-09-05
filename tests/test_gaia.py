import pytest
import mock
import os
import shutil

from click.testing import CliRunner
from gaia import gaia


def setup_module(module):
    if os.path.isfile('gaia_conf.json'):
        os.rename('gaia_conf.json', 'gaia_conf.json.real')
    shutil.copyfile('tests/gaia_conf.json.test', 'gaia_conf.json')


def teardown_module(module):
    if os.path.isfile('gaia_conf.json.real'):
        os.rename('gaia_conf.json.real', 'gaia_conf.json')


@pytest.mark.parametrize('bucket, keyword, bucket_exist', (
        ('s3', 'keyword',True),
        ('undefined', 'keyword',False)
))
@mock.patch('boto3.resource')
def test_find(mock_resource, bucket, keyword, bucket_exist):
    os.system('rm -rf logs')

    runner = CliRunner()
    runner.invoke(gaia.cli, ['find', bucket, keyword])
    path = 'logs/' + bucket

    assert os.path.isdir(path) == True
    if bucket_exist:
        assert mock_resource.called