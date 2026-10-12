from .config import TOP_K


def get_retriever(vectorstore, university_filter=None):
    if university_filter and university_filter != "All Universities":
        return vectorstore.as_retriever(
            search_kwargs={
                "k": TOP_K,
                "filter": {"university": university_filter}
            }
        )
    else:
        return vectorstore.as_retriever(
            search_kwargs={"k": TOP_K}
        )