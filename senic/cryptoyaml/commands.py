import click
from os import path

from . import api


def get_context(filepath, key, keyfile):
    try:
        return api.CryptoYAML(filepath, api.get_key(key, keyfile))
    except api.MissingKeyException as exc:
        click.echo(exc.msg)
        raise click.Abort()


@click.group(help='create, read and edit encrypted YAML files')
def main():
    pass


@click.command(help='generate a new private key on filesystem')
@click.argument('keyfile')
def generate_key(keyfile):
    created = api.generate_key(path.abspath(path.expanduser(keyfile)))
    click.echo('Created new private key at {}'.format(created))


@click.command(help='create a new encrypted YAML file from scratch')
@click.argument('filepath')
@click.option('--key', default=None, help='secret key')
@click.option('--keyfile', default=None, help='path to secret keyfile')
def create(filepath, key=None, keyfile=None):
    context = get_context(filepath, key, keyfile)
    context.write()
    click.echo('created new file at {}'.format(context.filepath))


@click.command(help='decrypt and print the contents of a settings file to stdout')
def cat():
    click.echo('decrypting file')


main.add_command(generate_key)
main.add_command(create)
main.add_command(cat)
