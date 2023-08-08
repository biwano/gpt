import click
from framework.store import store
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

load_dotenv()


# Root group
@click.group()
def cli():
    pass


# EMBEDDINGS ###############################
@cli.group(help="Manage embeddings")
def embeddings():
    pass


# Delete all mbeddings
@embeddings.command(help="Deletes encodings in pinecone")
def purge():
    store.embeddings_purge()


# Query embeddings
@embeddings.command(help="query pinecone encodings")
@click.argument('query')
def query(query):
    print(store.query(query))


# PDFS ###############################
@cli.group(help="Manage pdfs")
def pdf():
    pass


@pdf.command(help="Transform PDF files into embeddings stored in pinecone")
@click.argument('files', type=click.File('rb'), nargs=-1)
def process(files):
    for file in files:
        print(f"Processing {file.name}")
        store.process_pdf(file)


@pdf.command(help="Returns a PDF into the pending state")
@click.argument('files', type=click.File('rb'), nargs=-1)
def restore(files):
    for file in files:
        print(f"Processing {file.name}")
        store.restore_pdf(file)


# PDF to Text
@cli.command(help="Sends a chat query to OpenAI with context")
@click.argument('query')
def chat(query):
    store.chat(query, [StreamingStdOutCallbackHandler()])


if __name__ == '__main__':
    cli()
