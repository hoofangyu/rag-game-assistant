from flask import Flask, request, jsonify
from src.embeddings import EmbeddingGenerator,VectorDB
from src.llm import RAGAgent
from src.utils import ChatMemory
import numpy as np

app = Flask(__name__)
vector_db = VectorDB()
vector_db.load_index()

embedding_generator = EmbeddingGenerator()
rag_agent = RAGAgent(retriever=vector_db)

chat_memory = ChatMemory()

@app.route('/answer_query', methods=['POST'])
def answer_query():
    """
    Endpoint to answer user query on the games description dataset.
    Expects a JSON payload with {"query": "text to search"}
    """
    data = request.get_json()
    query_text = data.get('query')
    session_id = data.get('session_id')

    if not session_id:
        return jsonify({"error": "Session id is required"}), 400
    if not query_text:
        return jsonify({"error": "Query text is required"}), 400
    
    if not chat_memory.check_memory(session_id):
        chat_memory.create_memory(session_id)

    conversation_history = chat_memory.get_memory(session_id)
    chat_history = "\n".join([f"User: {entry['user']}\nBot: {entry['bot']}" for entry in conversation_history])
        
    try:
        result = rag_agent.answer_query(query_text, history=chat_history)
        chat_memory.update_memory(session_id, query_text, result)
        return jsonify({"result":result, "chat_memory":chat_memory.get_memory(session_id)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)