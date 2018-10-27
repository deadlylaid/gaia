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
@click.argument('bucket_name')
@click.argument('folder')
@click.argument('keyword')
@click.option('--time', '-t', default=datetime.utcnow(), help='UTC time like "1990-01-01T12:00:00"')
def find(bucket_name, folder, keyword, time):
    try:
        with open('gaia_conf.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("gaia_conf.json file doesn't exist, run `gaia gen` ")

    if not os.path.isdir('logs'):
        os.mkdir('logs')

    log_dir = 'logs/' + bucket_name + '/'
    os.mkdir(log_dir)

    try:
        bucket_path = config['BUCKET_PATH'][bucket_name][folder]
    except KeyError:
        raise KeyError(bucket_name + ' is invalid key please check gaia_conf.json')

    bucket_path = _bucket_path(time, bucket_path)

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