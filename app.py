import os
import streamlit as st

from src.config import DATA_PATH
from src.document_loader import load_documents
from src.text_splitter import split_documents
from src.embedding_model import get_embedding_model
from src.vector_store import create_vector_store, load_vector_store
from src.rag_pipeline import build_rag_chain


st.set_page_config(page_title="Education RAG System", layout="wide")
st.title("🎓 AI-Powered Curriculum & Course Content Retrieval System using RAG")

embedding_model = get_embedding_model()

# Create or load vector DB
if not os.path.exists("chroma_db"):
    with st.spinner("Indexing syllabus documents..."):
        documents = load_documents(DATA_PATH)
        chunks = split_documents(documents)
        vectorstore = create_vector_store(chunks, embedding_model)
else:
    vectorstore = load_vector_store(embedding_model)

# Dropdown for filtering
university_options = ["All Universities"] + [
    f.replace(".pdf", "") for f in os.listdir(DATA_PATH) if f.endswith(".pdf")
]

selected_university = st.selectbox(
    "Filter by University (Optional)",
    university_options
)

query = st.text_input("Enter your academic query:")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):

            rag_chain = build_rag_chain(
                vectorstore,
                None if selected_university == "All Universities" else selected_university
            )

            answer = rag_chain.invoke(query)

        st.subheader("📌 Answer")
        st.write(answer)