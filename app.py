from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time
import random
from pipeline.pipeline import RAGPipeline

app = Flask(__name__)
CORS(app)

try:
  pipeline = RAGPipeline()
  print(f"[Debug] Pipeline loaded sucessfully.")
except Exception as e:
  raise RuntimeError(f"Pipeline loading failed :{e}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    
    data = request.json
    query = data.get("query", "")
    
    start = time.time()
	
    # answer = pipeline.test(query)
    # answer = pipeline.run(query)
    answer = pipeline.run_groq(query)
	
    print(f"[Debug] Pipeline connected Success: {answer}")
    
    latency = round(time.time() - start, 3)
	
    print(f"[Debug] retrieved_chunks : {answer["retrieved_chunks"]}")
	
    top_chunk = answer.get('retrieved_chunks', None)
    metadata = top_chunk[0].get('metadata') if  top_chunk else None
    # metadata = top_chunk.get('metadata',None)
    source = metadata.get('source', None) if metadata else None
    chunk_id = metadata.get('chunk_id', None) if metadata else None
	
    print(f"[Debug] Top Chunks: {metadata}")
	
    result = {"query": answer["query"], "answer": answer["answer"], "latency": answer["latency"]["total"], "confidence": answer["confidence"], "source": source, "chunk_id": chunk_id}
    
    return jsonify(result)

@app.route("/chat1", methods=["POST"])
def chat1():
    data = request.json
    query = data.get("query", "")
    
    start = time.time()
    
    test_data = [
        {
            "query": "What is Python?",
            "answer": "Python is a high-level programming language known for readability and versatility.",
            "confidence": "HIGH",
            "source": "tutorial_1.txt",
            "chunk_id": 3
        },
        {
            "query": "Explain Flask.",
            "answer": "Flask is a lightweight web framework for Python.",
            "confidence": "LOW",
            "source": "tutorial_2.txt",
            "chunk_id": 7
        },
        {
            "query": "What is Bootstrap?",
            "answer": "Bootstrap is a CSS framework for responsive web design.",
            "confidence": "MEDIM",
            "source": "tutorial_3.txt",
            "chunk_id": 5
        },
        {
            "query": "Define RAG system?",
            "answer": "A Retrieval-ugmentedGeneration(RAG) system combines with generative models to improve answers.",
            "confidence": "HIGH",
            "source": "tutorial_8.txt",
            "chunk_id": 12
        }
    ]
    
    entry = random.choice(test_data)
    
    latency = round(time.time() - start, 3)
    
    response = {
        "query": query,
        "answer": entry["answer"],
        "latency": latency,
        "confidence": entry["confidence"],
        "source": entry["source"],
        "chunk_id": entry["chunk_id"]
    }
    
    return jsonify(response)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok", "message":"Service is healthy"}), 200

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "message": "Test endpoint working",
        "example": {"foo": "bar", "number": 123},
    })

if __name__ == "__main__":
    app.run(debug = True)