import boto3
import botocore
import click
import json
import os


@click.group()
def cli():
    os.system('rm -rf logs')


@cli.command()
@click.argument('bucket_name')
@click.argument('keyword')
def find(bucket_name, keyworkd):
    try:
        with open('gaia_conf.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("gaia_conf.json file doesn't exist, create gaia_conf.json in root directory")

    if not os.path.isdir('logs'):
        os.mkdir('logs')

    log_dir = 'logs/' + bucket_name + '/'
    os.mkdir(log_dir)

    try:
        bucket_path = config['BUCKET_PATH'][bucket_name]
    except KeyError:
        raise KeyError(bucket_name + ' is not in gaia_conf.json')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    try:
        for object in bucket.objects.filter(Prefix=bucket_path):
            is_file = object.key.split('/')[-1]
            if is_file:
                bucket.download_file(object.key, log_dir + object.key.split('/')[-1])
    except botocore.exceptions.NoCredentialsError:
        raise NoCredentialError


def _finder(keyword):
    raise NotImplementedError


class NoCredentialError(botocore.exceptions.NoCredentialsError):
    fmt = "please create credential in `~/.aws/` Referer - https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html"
