import os
import shutil
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from config import CHROMA_DB_DIR, EMBEDDING_MODEL

def create_vectorstore(book_summaries: dict, rebuild=False):
    documents = [
        Document(page_content=summary, metadata={"title": title})
        for title, summary in book_summaries.items()
    ]
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    if rebuild and os.path.exists(CHROMA_DB_DIR):
        shutil.rmtree(CHROMA_DB_DIR)

    if not os.path.exists(CHROMA_DB_DIR):
        vs = Chroma.from_documents(
            documents,
            embedding_model,
            persist_directory=CHROMA_DB_DIR
        )
        vs.persist()  # saves to disk
    else:
        # Reuse existing persisted vector store
        vs = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=embedding_model
        )
    return vs
