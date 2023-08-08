from pathlib import Path
import os
from functools import cached_property


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

    def pdf2text(self, file):
        import pdftotext
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        # Transform to text
        text = " ".join(pdftotext.PDF(file))

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=128
        )
        docs = text_splitter.create_documents([text])
        return list(map(lambda doc: doc.page_content, docs))

    def process_pdf(self, file):
        # Transform pdf to chunks
        docs = self.pdf2text(file)
        # Create embeddings
        embeddings = self.openAI_embeddings.embed_documents(docs)
        # Create vectors
        filepath = Path(file.name)
        filename = filepath.name
        vectors = []
        for i in range(len(docs)):
            vectors.append({
                "id": f"{filename}_{i}",
                "values": embeddings[i],
                "metadata": {
                    "content": docs[i],
                    "filename": filename,
                    "chunk": i
                }
            })
        # Save vectors to pinecone
        self.pinecone_index.upsert(
            vectors=vectors
        )
        # Mark the file as processed by moving it
        os.rename(filepath, filepath.parent.joinpath("..").joinpath("processed").joinpath(filepath.name))

    def restore_pdf(self, file):
        filepath = Path(file.name)
        os.rename(filepath, filepath.parent.joinpath("..").joinpath("pending").joinpath(filepath.name))

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
