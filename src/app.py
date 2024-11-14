from flask import Flask, request, jsonify
from src.embeddings import EmbeddingGenerator,VectorDB
from src.llm import RAGAgent
import numpy as np

app = Flask(__name__)

vector_db = VectorDB()
vector_db.load_index()

embedding_generator = EmbeddingGenerator()
rag_agent = RAGAgent(retriever=vector_db)

@app.route('/answer_query', methods=['POST'])
def answer_query():
    """
    Endpoint to search for similar texts based on a query.
    Expects a JSON payload with {"query": "text to search"}
    """
    data = request.get_json()
    query_text = data.get('query')

    if not query_text:
        return jsonify({"error": "Query text is required"}), 400
    try:
        result = rag_agent.answer_query(query_text)
        return jsonify({"result":result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

