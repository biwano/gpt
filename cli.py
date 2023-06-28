import click
from transform import Transform


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file', type=click.File('rb'))
def pdf2text(file):
    Transform().pdf2text(file)


if __name__ == '__main__':
    cli()