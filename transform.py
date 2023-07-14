from pathlib import Path
import os
import json
from functools import cached_property


def curdir():
    return os.path.dirname(os.path.realpath(__file__))


class Transform():

    @cached_property
    def openAI_embeddings(self):
        from langchain.embeddings import OpenAIEmbeddings
        return OpenAIEmbeddings()

    @cached_property
    def pinecone_index(self):
        import pinecone
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="us-west4-gcp-free")
        return pinecone.Index("verra-index")

    def get_dest_filepath(self, file, folder, ext):
        filename = Path(file.name).name
        return f"{curdir()}/var/{folder}/{filename}.{ext}"

    def get_dest_file(self, file, folder, ext):
        dest_filepath = self.get_dest_filepath(file, folder, ext)
        dest_file = open(dest_filepath, "w")
        exists = os.path.isfile(dest_filepath)

        return dest_file, exists

    def pdf2text(self, file):
        import pdftotext
        dest_file_path = self.get_dest_filepath(file, "texts", "txt")
        # Transform to text
        text = " ".join(pdftotext.PDF(file))

        # Find paragraphs
        text = text.split("\n\n")

        # Remove very small paragraphs
        text = [t for t in text if len(t.split("\n")) > 1]
        for i, t in enumerate(text):
            dest_file_i = open(f"{dest_file_path}.{i}", "w")
            dest_file_i.write(t)

    def text2embedding(self, file):
        dest_file, exists = self.get_dest_file(file, "embeddings", "emb")
        if not exists:
            text = file.read().decode("utf-8")
            query_result = self.openAI_embeddings.embed_query(text)
            dest_file.write(json.dumps({"values": query_result}))

    def embedding2pinecone(self, file):
        vector_name = os.path.basename(file.name)
        print(vector_name)
        vector = json.loads(file.read())
        vector.update({
            "id": vector_name
        })
        index = self.pinecone_index
        index.upsert(
            vectors=[vector]
            )

    def query(self, text):
        embedding = json.load(open("./a", "r"))
        embedding = self.openAI_embeddings.embed_query(text)
        index = self.pinecone_index
        res = index.query(
            top_k=7,
            vector=embedding
        )
        print(res)
