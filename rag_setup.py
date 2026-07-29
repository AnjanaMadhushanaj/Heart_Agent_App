import os
import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from crewai.tools import tool

# Path to the persistent database
DB_PATH = os.path.join(os.path.dirname(__file__), ".chroma")
CORPUS_PATH = os.path.join(os.path.dirname(__file__), "medical_corpus.txt")

def init_vector_store():
    """Initializes ChromaDB and ingests guidelines if not already ingested."""
    # Initialize client
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Use ONNX embedding function
    embedding_function = ONNXMiniLM_L6_V2()
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="medical_guidelines",
        embedding_function=embedding_function
    )
    
    # Check if empty, then ingest
    if collection.count() == 0:
        if os.path.exists(CORPUS_PATH):
            with open(CORPUS_PATH, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            
            ids = [f"guideline_{i}" for i in range(len(lines))]
            metadatas = [{"source": "medical_corpus"} for _ in range(len(lines))]
            
            collection.add(
                documents=lines,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Ingested {len(lines)} guidelines into ChromaDB.")
        else:
            print("medical_corpus.txt not found!")
    else:
        print(f"ChromaDB collection already initialized with {collection.count()} items.")

# Initialize the vector store when this module is imported/run
init_vector_store()

def retrieve_medical_guidelines_func(query: str) -> str:
    """Helper function to search guidelines directly without tool decorator."""
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        embedding_function = ONNXMiniLM_L6_V2()
        collection = client.get_collection(
            name="medical_guidelines",
            embedding_function=embedding_function
        )
        
        # Query top 4 matching guidelines
        results = collection.query(
            query_texts=[query],
            n_results=4
        )
        
        documents = results.get("documents", [[]])[0]
        if not documents:
            return "No matching clinical guidelines found."
        
        formatted_results = "\n".join([f"- {doc}" for doc in documents])
        return f"Relevant Medical Guidelines for query '{query}':\n{formatted_results}"
    except Exception as e:
        return f"Error retrieving guidelines: {str(e)}"

@tool("Medical Guidelines Retriever")
def retrieve_medical_guidelines(query: str) -> str:
    """
    Search and retrieve clinical medical guidelines regarding cholesterol levels, 
    resting heart rate (thalach), exercise target heart rates, and cardiovascular risk.
    
    Parameters:
    - query: Semantic search query string.
    
    Returns:
    - A string containing relevant medical guidelines matching the query.
    """
    return retrieve_medical_guidelines_func(query)

def get_rag_tool():
    """Returns the CrewAI Custom Tool for RAG document retrieval."""
    return retrieve_medical_guidelines

if __name__ == "__main__":
    # Test query
    print("Testing retrieval...")
    print(retrieve_medical_guidelines_func("cholesterol risk level"))
