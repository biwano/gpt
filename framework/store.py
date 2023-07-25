from pathlib import Path
import os
import json
from functools import cached_property
import re


def curdir():
    return os.path.dirname(os.path.realpath(__file__))


class Store():

    @cached_property
    def openAI_embeddings(self):
        from langchain.embeddings import OpenAIEmbeddings
        return OpenAIEmbeddings()

    def openAI_llmchain(self, callbacks):
        from langchain.llms import OpenAI
        from langchain import PromptTemplate, LLMChain

        template = """
        ### Context ###
        {context}

        Using the given context answer this quetion: {question}

        """

        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        llm = OpenAI(streaming=True, callbacks=callbacks)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        return llm_chain

    @cached_property
    def pinecone_index(self):
        import pinecone
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="us-west4-gcp-free")
        return pinecone.Index("verra-index")

    def get_dest_filepath(self, file, folder, ext):
        filename = Path(file.name).name
        return f"{curdir()}/../var/{folder}/{filename}.{ext}"

    def get_dest_file(self, file, folder, ext):
        dest_filepath = self.get_dest_filepath(file, folder, ext)
        dest_file = open(dest_filepath, "w")
        exists = os.path.isfile(dest_filepath)

        return dest_file, exists

    def pdf2text(self, file):
        import pdftotext
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        dest_file_path = self.get_dest_filepath(file, "texts", "txt")
        # Transform to text
        text = " ".join(pdftotext.PDF(file))

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=128
        )
        docs = text_splitter.create_documents([text])
#        print(docs)
        for i, t in enumerate(docs):
            dest_file_i = open(f"{dest_file_path}.{i}", "w")
            dest_file_i.write(t.page_content)
            
    def text2embedding(self, file):
        filename = Path(file.name).name
        sp = filename.split(".")
        orig_filename = ".".join(sp[0:-3])
        chunk = sp[-1]
        dest_file, exists = self.get_dest_file(file, "embeddings", "emb")
        content = file.read().decode("utf-8")
        query_result = self.openAI_embeddings.embed_query(content)
        dest_file.write(json.dumps({
            "values": query_result,
            "metadata": {
                "content": content,
                "filename": orig_filename,
                "chunk": chunk
            }
        }))

    def embedding2pinecone(self, file):
        vector_name = os.path.basename(file.name)
        vector = json.loads(file.read())
        vector.update({
            "id": vector_name
        })
        index = self.pinecone_index
        index.upsert(
            vectors=[vector]
            )

    def embeddings_purge(self):
        index = self.pinecone_index
        index.delete(deleteAll=True)

    def query(self, text):
        embedding = self.openAI_embeddings.embed_query(text)
        index = self.pinecone_index
        res = index.query(
            top_k=7,
            vector=embedding,
            include_metadata=True
        )
        return res

    def chat(self, question, callbacks):
        embeddings = self.query(question)
        context = ""
        for embedding in embeddings["matches"]:
            more_context = embedding["metadata"]["content"]
            context = f"{context}\n{more_context}"
        res = self.openAI_llmchain(callbacks).run({
            "context": context,
            "question": question
        })
        return res


store = Store()