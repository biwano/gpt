from langchain.embeddings import OpenAIEmbeddings


def embed(text):
    embeddings = OpenAIEmbeddings()
    query_result = embeddings.embed_query(text)
    print(query_result)
    print(len(query_result))