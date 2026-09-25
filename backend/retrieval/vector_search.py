import ollama
from db.qdrant import client, COLLECTION_NAME

MODEL = "nomic-embed-text"

def vector_search(query: str, limit: int = 5):
    try:
        collections = client.get_collections().collections
        if not any(c.name == COLLECTION_NAME for c in collections):
            return []
    except Exception:
        return []

    response = ollama.embed(
        model=MODEL, 
        input=query
    )
    
    query_embedding = response["embeddings"][0]
    
    try:
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=limit
        )
    except Exception:
        return []
    
    points_list = results.points if hasattr(results, "points") else results
    
    chunks = []
    for point in points_list:
        payload = point.payload or {}
        chunks.append({
            "text": payload.get("text", ""),
            "filename": payload.get("filename", "Unknown"),
            "document_id": payload.get("document_id", ""),
            "chunk_index": payload.get("chunk_index", "")
        })
    return chunks