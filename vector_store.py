import os
from langchain_community.vectorstores import Chroma
from .config import CHROMA_DB_DIR


def create_vector_store(documents, embedding_model):
    if not os.path.exists(CHROMA_DB_DIR):
        os.makedirs(CHROMA_DB_DIR)

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=CHROMA_DB_DIR
    )
    vectorstore.persist()
    return vectorstore


def load_vector_store(embedding_model):
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embedding_model
    )