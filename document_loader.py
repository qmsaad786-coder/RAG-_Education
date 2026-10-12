import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def extract_university_from_filename(filename: str) -> str:
    return filename.replace(".pdf", "").strip()


def load_documents(data_path: str):
    documents = []

    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(data_path, file)
            university_name = extract_university_from_filename(file)

            loader = PyPDFLoader(file_path)
            pdf_docs = loader.load()

            for doc in pdf_docs:
                doc.metadata["university"] = university_name
                doc.metadata["source_file"] = file
                documents.append(doc)

    return documents