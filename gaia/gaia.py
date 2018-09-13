import boto3
import botocore
import click
import gzip
import json
import os

from .errors import NoCredentialError


@click.group()
def cli():
    os.system('rm -rf logs')


@cli.command()
@click.argument('bucket_name', default='0')
@click.argument('path', default='0')
def gen(bucket_name, path):
    if not os.path.isfile('gaia_conf.json'):
        with open('gaia_conf.json', 'w') as f:
            json.dump({"BUCKET_PATH":{}}, f)
            click.echo('gaia_conf.json file generated')

    if bucket_name is not '0' and path is not '0':
        with open('gaia_conf.json') as f:
            data = json.load(f)
        data['BUCKET_PATH'].update({bucket_name:path})
        with open('gaia_conf.json', 'w') as f:
            json.dump(data,f)

@cli.command()
@click.argument('bucket_name')
@click.argument('keyword')
def find(bucket_name, keyword):
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
        bucket_path = config['BUCKET_PATH'][bucket_name]
    except KeyError:
        raise KeyError(bucket_name + ' is invalid key please check gaia_conf.json')

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

    log = (_log_finder(log_dir, keyword))
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
