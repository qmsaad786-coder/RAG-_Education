from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from .retriever import get_retriever
from .llm import get_llm_runnable


def build_rag_chain(vectorstore, university_filter=None):

    retriever = get_retriever(vectorstore, university_filter)

    prompt_template = PromptTemplate.from_template(
        """
You are an academic assistant.

Answer ONLY using the provided context.
If the information is not available, respond with:
"Information not found in the provided syllabus documents."

Context:
{context}

Question:
{question}
"""
    )

    llm = get_llm_runnable()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
        | prompt_template
        | RunnableLambda(lambda x: x.to_string()) 
        | llm
    )

    return rag_chain