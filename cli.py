import click
from framework.store import store
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

load_dotenv()


# Root group
@click.group()
def cli():
    pass


# PDF to Text
@cli.command(help="Creates text chunks from a pdf file")
@click.argument('file', type=click.File('rb'))
def pdf2text(file):
    store.pdf2text(file)


# Embeddings Group
@cli.group(help="Manage embeddings")
def embeddings():
    pass


# Create embeddings
@embeddings.command(help="Creates embeddings from text files")
@click.argument('files', type=click.File('rb'), nargs=-1)
def create(files):
    for file in files:
        store.text2embedding(file)


# Upload mbeddings
@embeddings.command(help="Saves embeddings to pinecone")
@click.argument('files', type=click.File('rb'), nargs=-1)
def save(files):
    t = Store()
    for file in files:
        t.embedding2pinecone(file)


# Delete all mbeddings
@embeddings.command(help="Deletes encodings in pinecone")
def purge():
    store.embeddings_purge()


# Query mbeddings
@embeddings.command(help="query pinecone encodings")
@click.argument('query')
def query(query):
    store.query(query)


# PDF to Text
@cli.command(help="Sends a chat query to OpenAI with context")
@click.argument('query')
def chat(query):
    store.chat(query, [StreamingStdOutCallbackHandler()])


if __name__ == '__main__':
    cli()