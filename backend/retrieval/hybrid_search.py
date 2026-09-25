from retrieval.vector_search import vector_search
from retrieval.keyword_search import keyword_search
from retrieval.rerank import rerank

def hybrid_search(question: str, limit: int = 5):
    vector_results = vector_search(question, limit=limit * 4)
    keyword_results = keyword_search(question, limit=limit * 4)
    
    merged = {}
    for chunk in vector_results:
        key = (chunk.get("document_id", ""), chunk.get("chunk_index", ""))
        merged[key] = chunk
        
    for chunk in keyword_results:
        key = (chunk.get("document_id", ""), chunk.get("chunk_index", ""))
        if key not in merged: 
            merged[key] = chunk
            
    results = list(merged.values())
    if not results:
        return []

    ranked_results = rerank(question, results)
    return ranked_results[:limit]