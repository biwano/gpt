import click
from transform import Transform
from dotenv import load_dotenv

load_dotenv()


# Root group
@click.group()
def cli():
    pass


# PDF to Text
@cli.command(help="Creates text chunks from a pdf file")
@click.argument('file', type=click.File('rb'))
def pdf2text(file):
    Transform().pdf2text(file)


# Embeddings Group
@cli.group(help="Manage embeddings")
def embeddings():
    pass


# Create embeddings
@embeddings.command(help="Creates embeddings from text files")
@click.argument('files', type=click.File('rb'), nargs=-1)
def create(files):
    t = Transform()
    for file in files:
        t.text2embedding(file)


# Upload mbeddings
@embeddings.command(help="Saves embeddings to pinecone")
@click.argument('files', type=click.File('rb'), nargs=-1)
def save(files):
    t = Transform()
    for file in files:
        t.embedding2pinecone(file)


# Delete all mbeddings
@embeddings.command(help="Deletes encodings in pinecone")
def purge():
    Transform().embeddings_purge()


# Query mbeddings
@embeddings.command(help="query pinecone encodings")
@click.argument('query')
def query(query):
    Transform().query(query)


# PDF to Text
@cli.command(help="Sends a chat query to OpenAI with context")
@click.argument('query')
def chat(query):
    print(Transform().chat(query))


if __name__ == '__main__':
    cli()