import os
import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from crewai.tools import tool

DB_PATH = os.path.join(os.path.dirname(__file__), ".chroma")
CORPUS_PATH = os.path.join(os.path.dirname(__file__), "medical_corpus.txt")

def init_vector_store(force_reingest: bool = True):
    """Initializes ChromaDB persistent store and ingests reference ranges."""
    client = chromadb.PersistentClient(path=DB_PATH)
    embedding_function = ONNXMiniLM_L6_V2()
    
    if force_reingest:
        try:
            client.delete_collection("medical_guidelines")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name="medical_guidelines",
        embedding_function=embedding_function
    )
    
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
            print(f"Ingested {len(lines)} general lab reference guidelines into ChromaDB.")
        else:
            print("medical_corpus.txt not found!")
    else:
        print(f"ChromaDB collection initialized with {collection.count()} items.")

# Initialize store
init_vector_store(force_reingest=True)

def retrieve_medical_guidelines_func(query: str) -> str:
    """Helper function to search reference ranges directly."""
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        embedding_function = ONNXMiniLM_L6_V2()
        collection = client.get_collection(
            name="medical_guidelines",
            embedding_function=embedding_function
        )
        
        results = collection.query(
            query_texts=[query],
            n_results=4
        )
        
        documents = results.get("documents", [[]])[0]
        if not documents:
            return "No matching reference range guidelines found."
        
        formatted_results = "\n".join([f"- {doc}" for doc in documents])
        return f"Relevant Medical Reference Ranges for query '{query}':\n{formatted_results}"
    except Exception as e:
        return f"Error retrieving reference ranges: {str(e)}"

@tool("Medical Guidelines Retriever")
def retrieve_medical_guidelines(query: str) -> str:
    """
    Search and retrieve standard medical reference ranges for lab parameters (lipid panel, CBC, glucose, liver/kidney markers).
    """
    return retrieve_medical_guidelines_func(query)

def get_rag_tool():
    """Returns the CrewAI Custom Tool for RAG document retrieval."""
    return retrieve_medical_guidelines

if __name__ == "__main__":
    print("Testing retrieval...")
    print(retrieve_medical_guidelines_func("cholesterol reference range"))
