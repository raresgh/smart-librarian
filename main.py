import json
import os
import re

from data.loader import load_summaries
from embeddings.vectorstore import create_vectorstore
from llm.summary_tool import get_summary_by_title
from llm.chat import build_chat_chain

from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_core.messages import AIMessage


book_summaries_dict = load_summaries()
vectorstore = create_vectorstore(book_summaries_dict)
retriever = vectorstore.as_retriever()
qa_chain = build_chat_chain(retriever)

def main():
    print("📚 Smart Librarian - Chatbot RAG 🤖")
    print("Scrie 'exit' ca să ieși.\n")

    while True:
        query = input("Tu: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 La revedere!")
            break

        # Step 1: Retrieve top documents manually (RAG)
        results = retriever.get_relevant_documents(query, k=1)
        response = qa_chain.run(query)

        if not results:
            print("🤖 Nu am găsit cărți relevante.")
            continue

        best_doc = results[0]
        title = best_doc.metadata["title"]
        detailed_summary = get_summary_by_title(title)

        print(f"\n- RECOMANDARE: {response}")
        #print(f"\n📘 REZUMAT: {detailed_summary}")
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
