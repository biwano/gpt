from pathlib import Path
import os
import json

def curdir():
    return os.path.dirname(os.path.realpath(__file__))


class Transform():
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
            from langchain.embeddings import OpenAIEmbeddings
            embeddings = OpenAIEmbeddings()
            text = file.read().decode("utf-8")
            query_result = embeddings.embed_query(text)
            dest_file.write(json.dumps(query_result))
