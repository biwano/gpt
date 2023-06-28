from pathlib import Path
import os


def curdir():
    return os.path.dirname(os.path.realpath(__file__))


class Transform():
    def get_dest_filepath(self, file, folder):
        filename = Path(file.name).stem
        return f"{curdir()}/var/texts/{filename}.txt"

    def get_dest_file(self, file, folder):
        dest_filepath = self.get_dest_filepath(file, folder)
        dest_file = open(dest_filepath, "w")
        exists = os.path.isfile(dest_filepath)

        return dest_file, exists

    def pdf2text(self, file):
        import pdftotext
        dest_file_path = self.get_dest_filepath(file, "texts")
        # Transform to text
        text = " ".join(pdftotext.PDF(file))

        # Find paragraphs
        text = text.split("\n\n") 

        # Remove data
        #text = filter(lambda t: len(t.split("\n")) <= 1, text)
        text = [t for t in text if len(t.split("\n")) > 1]
        for i, t in enumerate(text):
            dest_file_i = open(f"{dest_file_path}.{i}", "w")
            dest_file_i.write(t)

    def text2embedding(self, file):
        from langchain.embeddings import OpenAIEmbeddings
        dest_file, exists = self.get_dest_file(file, "texts")
        if not exists:
            embeddings = OpenAIEmbeddings()
            text = file.read()
            query_result = embeddings.embed_query(text)
            dest_file.write(query_result)
