from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

RAG_TEMPLATE = PromptTemplate.from_template("""
Ești un asistent AI care recomandă cărți doar din lista dată mai jos.

{context}

Întrebarea utilizatorului: {question}

Instrucțiuni:
- Răspunde doar cu titluri din context.
- Nu inventa titluri sau detalii care nu apar în context.
- Dacă nu există o potrivire clară, spune „Nu am o recomandare potrivită.”

Răspuns:
""")

def build_chat_chain(retriever):
    llm = ChatOpenAI(temperature=0.7)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
