import click
from transform import Transform
from dotenv import load_dotenv

load_dotenv()


# Root group
@click.group()
def cli():
    pass


# PDF to Text
@cli.command(help="create a text version of a pdf file")
@click.argument('file', type=click.File('rb'))
def pdf2text(file):
    Transform().pdf2text(file)


# Embeddings Group
@cli.group()
def embeddings():
    pass


# Create embeddings
@embeddings.command()
@click.argument('files', type=click.File('rb'), nargs=-1)
def create(files):
    t = Transform()
    for file in files:
        t.text2embedding(file)


# Upload mbeddings
@embeddings.command()
@click.argument('files', type=click.File('rb'), nargs=-1)
def save(files):
    t = Transform()
    for file in files:
        t.embedding2pinecone(file)


# Delete all mbeddings
@embeddings.command()
def purge():
    Transform().embeddings_purge()


# Query mbeddings
@embeddings.command()
@click.argument('query')
def query(query):
    Transform().query(query)


if __name__ == '__main__':
    cli()