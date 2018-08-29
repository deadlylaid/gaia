import click
import json
import os


@click.group()
def cli():
    os.system('rm -rf logs')
    pass


@cli.command()
@click.argument('bucket_name')
def find(bucket_name):
    try:
        with open('gaia_conf.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("gaia_conf.json file doesn't exist, create gaia_conf.json in root directory")

    if not os.path.isdir('logs'):
        os.mkdir('logs')
    os.mkdir('logs/'+bucket_name)

    try:
        bucket_path = config['BUCKET_PATH'][bucket_name]
    except KeyError:
        raise KeyError(bucket_name + ' is not in gaia_conf.json')
