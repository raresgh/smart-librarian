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
known_titles = list(book_summaries_dict.keys())

vectorstore = create_vectorstore(book_summaries_dict)
retriever = vectorstore.as_retriever()
qa_chain = build_chat_chain(retriever)

def main():
    while True:
        query = input("Tu: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 La revedere!")
            break

        if "Spune-mi mai multe despre" in query:
            match = re.search(r'Spune-mi mai multe despre (.+)', query)
            if match:
                title = match.group(1).strip()
                summary = get_summary_by_title(title)
                print(f"\n🤖 REZUMAT: {summary}")
            else:
                print("⚠️ Nu am putut găsi un titlu în întrebarea ta.")
            continue

        response = qa_chain.run(query)

        if response == "Not found":
            print("🤖 Nu am o recomandare potrivită pentru această întrebare.")
        elif response in known_titles:
            print(f"\n🤖 RECOMANDARE: {response}")
            print("💡 Poți cere un rezumat tastând: „Spune-mi mai multe despre [titlu]”.")
        else:
            print(f"⚠️ LLM a returnat un titlu necunoscut: {response}")
            print("🔒 Ignorăm pentru a preveni halucinații.")

if __name__ == "__main__":
    main()
