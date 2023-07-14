import click
from transform import Transform
from dotenv import load_dotenv

load_dotenv()

# Root group
@click.group()
def cli():
    pass


# PDF to Text
@cli.command()
@click.argument('file', type=click.File('rb'))
def pdf2text(file):
    Transform().pdf2text(file)


# Embeddings Group
@cli.group()
def embedding():
    pass


# Create embeddings
@embedding.command()
@click.argument('file', type=click.File('rb'))
def create(file):
    Transform().text2embedding(file)


# Upload mbeddings
@embedding.command()
@click.argument('file', type=click.File('rb'))
def save(file):
    Transform().embedding2pinecone(file)


# Query mbeddings
@embedding.command()
@click.argument('query')
def query(query):
    Transform().query(query)


if __name__ == '__main__':
    cli()