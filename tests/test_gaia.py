import ast
import json
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
        ('s3', 'keyword', True),
        ('undefined', 'keyword', False)
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


@pytest.mark.parametrize('keyword', (
        ('d2Rd8fpbRE2toz8KOPD_zA'),
        ('rTESTUJqQlKq55tjXdNoEA')
))
def test_log_finder(keyword):
    result = gaia._log_finder('tests/test_logs/', keyword)
    result = ast.literal_eval(result)
    assert result['uid'] == keyword


# test_gen은 test_find보다 늦게 실행되므로 gaia_conf.json을 삭제해도 영향을 미치지 않는다.
def test_gen():
    os.system('rm gaia_conf.json')
    runner = CliRunner()
    runner.invoke(gaia.cli, ['gen', 'testbucket', 'testpath'])
    assert os.path.isfile('gaia_conf.json') == True
    with open('gaia_conf.json') as f:
        data = json.load(f)
    assert data == {'BUCKET_PATH': {'testbucket': 'testpath'}}