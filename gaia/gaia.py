import boto3
import botocore
import click
import dateutil
import gzip
import json
import os

from datetime import datetime

from .errors import NoCredentialError


@click.group()
def cli():
    os.system('rm -rf logs')


@cli.command()
@click.option('--key', '-k')
@click.option('--path', '-p')
def gen(key, path):
    if not os.path.isfile('gaia_conf.json'):
        with open('gaia_conf.json', 'w') as f:
            json.dump({"BUCKET_PATH": {}}, f)
            click.echo('gaia_conf.json file generated')

    if key and path :
        with open('gaia_conf.json') as f:
            data = json.load(f)
        data['BUCKET_PATH'].update({key: path})
        with open('gaia_conf.json', 'w') as f:
            json.dump(data, f)


@cli.command()
@click.argument('key')
@click.argument('keyword')
@click.option('--time', '-t', default=datetime.utcnow(), help='UTC time like "1990-01-01T12:00:00"')
def find(key, keyword, time):
    try:
        with open('gaia_conf.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("gaia_conf.json file doesn't exist, run `gaia gen` ")

    if not os.path.isdir('logs'):
        os.mkdir('logs')

    try:
        bucket_path = config['BUCKET_PATH'][key]
    except KeyError:
        raise KeyError(key + ' is invalid key please check gaia_conf.json')

    if bucket_path[0] == '/':
        bucket_path = bucket_path[1:]
    if bucket_path[-1] == '/':
        bucket_path = bucket_path[:-1]

    bucket_name = bucket_path.split('/')[0]

    bucket_path = bucket_path.split('/')
    bucket_path = '/'.join(bucket_path[1:])

    bucket_path = _bucket_path(time, bucket_path)

    log_dir = 'logs/' + key + '/'
    os.mkdir(log_dir)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    try:
        for object in bucket.objects.filter(Prefix=bucket_path):
            is_file = object.key.split('/')[-1]
            if is_file:
                click.echo(is_file + ' downloading...')
                bucket.download_file(object.key, log_dir + object.key.split('/')[-1])
    except botocore.exceptions.NoCredentialsError:
        raise NoCredentialError

    log = _log_finder(log_dir, keyword)
    click.echo(log)


def _log_reader(log_dir):
    for file in os.listdir(log_dir):
        click.echo(file + ' reading...')
        extension = file.split('.')[-1]
        if extension in ['gz']:
            opend_file = gzip.open(log_dir + file)
        else:
            opend_file = open(log_dir + file)
        with opend_file as logs:
            for log in logs:
                yield log


def _log_finder(log_dir, keyword):
    for log in _log_reader(log_dir):
        if type(log) is not str:
            log = log.decode()
        if keyword in log:
            return log
    return "keyword does not exist"


def _bucket_path(time, bucket_path):
    if isinstance(time, str):
        time = dateutil.parser.parse(time)
    time = {
        '<YY>': '{:02d}'.format(time.year),
        '<MM>': '{:02d}'.format(time.month),
        '<DD>': '{:02d}'.format(time.day),
        '<HH>': '{:02d}'.format(time.hour),
        '<MI>': '{:02d}'.format(time.minute),
        '<SC>': '{:02d}'.format(time.second)
    }
    for k, v in time.items():
        bucket_path = bucket_path.replace(k, v)
    return bucket_path