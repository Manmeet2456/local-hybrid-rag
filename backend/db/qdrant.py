from pathlib import Path
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue

COLLECTION_NAME = "documents"

def get_qdrant_client():
    try:
        c = QdrantClient("http://localhost:6333", timeout=1.0, check_compatibility=False)
        c.get_collections()
        return c
    except Exception:
        # Fallback to local embedded storage in backend/qdrant_data
        db_path = Path(__file__).resolve().parent.parent / "qdrant_data"
        return QdrantClient(path=str(db_path), check_compatibility=False)

client = get_qdrant_client()

def create_collection(vector_size: int):
    try:
        collections = client.get_collections().collections
        if any(c.name == COLLECTION_NAME for c in collections):
            info = client.get_collection(COLLECTION_NAME)
            # Check if existing collection vector dimension matches
            vectors_config = getattr(info.config.params, "vectors", None)
            existing_size = getattr(vectors_config, "size", None) if vectors_config else None
            if existing_size == vector_size:
                return
            # Dimension mismatch (e.g. 4 vs 768) -> recreate collection
            client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

def store_embeddings(embeddings):
    points = []
    for item in embeddings:
        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=item["embedding"],
                payload={
                    "text": item["text"],
                    "document_id": item["document_id"],
                    "filename": item["filename"],
                    "chunk_index": item["chunk_index"]
                }
        ))
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def list_documents():
    documents = {}
    offset = None
    while True:
        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False,
            offset=offset
        )
        for point in points:
            payload = point.payload or {}

            document_id = payload.get("document_id")
            if not document_id:
                continue
            if document_id not in documents:
                documents[document_id] = {
                    "document_id": document_id,
                    "filename": payload.get("filename", "Unnamed"),
                    "chunks": 0
                }
            documents[document_id]["chunks"] += 1
            
        if offset is None:
            break

    return list(documents.values())

def delete_document(document_id: str):
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="document_id", 
                    match=MatchValue(
                        value=document_id
                    )
                )
            ]
        )
    )

def list_chunks():
    chunks = []
    offset = None
    while True:
        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False,
            offset=offset
        )
        for point in points:
            chunks.append({
                "text": point.payload.get("text"),
                "filename": point.payload.get("filename"),
                "document_id": point.payload.get("document_id"),
                "chunk_index": point.payload.get("chunk_index")
            })
        if offset is None:
            break
    return chunks