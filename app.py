import re

from flask import Flask, render_template, request, jsonify
from data.loader import load_summaries
from embeddings.vectorstore import create_vectorstore
from llm.summary_tool import get_summary_by_title
from llm.chat import build_chat_chain

from langchain.chains import RetrievalQA
from langchain_core.messages import AIMessage


book_summaries_dict = load_summaries()
known_titles = list(book_summaries_dict.keys())

vectorstore = create_vectorstore(book_summaries_dict)
retriever = vectorstore.as_retriever()
qa_chain = build_chat_chain(retriever)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("question")
    if "Spune-mi mai multe despre" in query:
        match = re.search(r'Spune-mi mai multe despre (.+)', query)
        if match:
            title = match.group(1).strip()
            summary = get_summary_by_title(title)
            answer = f"\n🤖 REZUMAT: {summary}"
        else:
            answer = "⚠️ Nu am putut găsi un titlu în întrebarea ta."
    else:

        response = qa_chain.run(query)

        if response == "Not found":
            answer = "🤖 Nu am o recomandare potrivită pentru această întrebare."
        elif response in known_titles:
            answer = (f"\n🤖 RECOMANDARE: {response}\n"
                      "💡 Poți cere un rezumat tastând: „Spune-mi mai multe despre [titlu]”.")
        else:
            answer = (f"⚠️ LLM a returnat un titlu necunoscut: {response}\n"
                      f"🔒 Ignorăm pentru a preveni halucinații.")

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

