import os

_model = None

def get_reranker():
    global _model
    if _model is None:
        try:
            os.environ.setdefault("HF_HOME", "D:/cache/huggingface")
            os.environ.setdefault("TORCH_HOME", "D:/cache/torch")
            from sentence_transformers import CrossEncoder
            _model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        except Exception:
            _model = False
    return _model

def rerank(question, chunks):
    if not chunks:
        return []
    
    model = get_reranker()
    if not model:
        # Fallback if reranker model is not available
        return chunks

    pairs = [(question, chunk.get("text", "")) for chunk in chunks]
    try:
        scores = model.predict(pairs)
    except Exception:
        return chunks
    
    ranked = []

    for chunk, score in zip(chunks, scores):
        ranked.append(
            {
                **chunk,
                "rerank_score": float(score)
            }
        )

    ranked.sort(
        key = lambda item:item["rerank_score"],
        reverse=True
    )

    return ranked