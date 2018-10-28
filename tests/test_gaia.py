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


@pytest.mark.parametrize('key, keyword, bucket_exist, time, dir_is_exist', (
        ('test1', 'keyword', True, '2018-09-19', True),
        ('test2', 'keyword', True, None, True),
        ('test3', 'keyword', True, None, True),
        ('test4', 'keyword', True, None, True),
        ('undefined', 'keyword', False, '2018-09-09', False),
        ('undefined', 'keyword', False, None, False),
))
@mock.patch('boto3.resource')
def test_find(mock_resource, key, keyword, bucket_exist, time, dir_is_exist):
    runner = CliRunner()
    runner.invoke(gaia.cli, ['find', '--time', time, key, keyword])
    path = 'logs/' + key

    assert os.path.isdir(path) == dir_is_exist
    if bucket_exist:
        assert mock_resource.called
    else:
        assert mock_resource.called == False


@pytest.mark.parametrize('keyword', (
        ('d2Rd8fpbRE2toz8KOPD_zA'),
        ('rTESTUJqQlKq55tjXdNoEA')
))
def test_log_finder(keyword):
    result = gaia._log_finder('tests/test_logs/', keyword)
    result = ast.literal_eval(result)
    assert result['uid'] == keyword


# test_gen은 test_find보다 늦게 실행되므로 gaia_conf.json을 삭제해도 영향을 미치지 않는다.
@pytest.mark.parametrize('key_option, key, path_option, path',(
        ('--key', 'testbucket', '--path', 'testbucket/test'),
        ('-k', 'testbucket', '-p', 'testbucket/test')
))
def test_gen(key_option, key, path_option, path):
    os.system('rm gaia_conf.json')
    runner = CliRunner()
    runner.invoke(gaia.cli, ['gen', key_option, key, path_option, path])
    assert os.path.isfile('gaia_conf.json') == True
    with open('gaia_conf.json') as f:
        data = json.load(f)
    assert data == {'BUCKET_PATH': {'testbucket': 'testbucket/test'}}


@pytest.mark.parametrize('time, bucket_path, path_result', (
        ('2018-09-11', "path/<YY>/<MM>/<DD>", "path/2018/09/11"),
        ('2017-11-02T15:12:24', "path/<YY>/<MM>/<DD>/<HH>/<MI>/<SC>", "path/2017/11/02/15/12/24")
))
def test_bucket_path(time, bucket_path, path_result):
    result = gaia._bucket_path(time, bucket_path)
    assert result == path_result
