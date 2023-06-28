import click
from transform import Transform
from dotenv import load_dotenv

load_dotenv()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file', type=click.File('rb'))
def pdf2text(file):
    Transform().pdf2text(file)


@cli.group()
def embedding():
    pass


@embedding.command()
@click.argument('file', type=click.File('rb'))
def create(file):
    Transform().text2embedding(file)


@embedding.command()
@click.argument('file', type=click.File('rb'))
def save(file):
    Transform().embedding2pinecone(file)


if __name__ == '__main__':
    cli()