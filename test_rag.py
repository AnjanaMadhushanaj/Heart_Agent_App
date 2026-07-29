from rag_setup import retrieve_medical_guidelines_func

def run_rag_evaluation():
    print("==================================================")
    print("RUNNING RAG RETRIEVAL EVALUATION (5 SAMPLE QUERIES)")
    print("==================================================")
    
    queries = [
        "cholesterol risk level",
        "exercise heart rate",
        "high cholesterol diet",
        "low exercise heart rate",
        "dietary sodium"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n[Query {i}] '{query}'")
        result = retrieve_medical_guidelines_func(query)
        print(result)
        print("-" * 50)

if __name__ == "__main__":
    run_rag_evaluation()
