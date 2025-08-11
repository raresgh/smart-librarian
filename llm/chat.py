from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

TITLE_ONLY_PROMPT = PromptTemplate.from_template("""
Ești un sistem care recomandă cărți pe baza unui context. 

Contextul este următorul:
{context}

Întrebarea utilizatorului este:
"{question}"

Instrucțiuni:
- Răspunde doar cu titlul exact al unei cărți din context.
- Nu adăuga explicații, fraze sau alte cuvinte.
- Dacă nu poți răspunde pe baza contextului, scrie exact: "Not found".
""")


def build_chat_chain(retriever):
    llm = ChatOpenAI(temperature=0.3)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": TITLE_ONLY_PROMPT}
    )
