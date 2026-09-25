import ollama

DEFAULT_MODEL = "llama3.2:1b"

def get_model():
    try:
        models = ollama.list()
        model_names = [m.model for m in models.models] if hasattr(models, "models") else [m.get("name") for m in models.get("models", [])]
        # Check preferred models
        for preferred in ["llama3.2:1b", "llama3.1:8b", "llama3.2:latest", "llama3:latest", "mistral:latest"]:
            for name in model_names:
                if name and preferred in name:
                    return name
        if model_names:
            # Pick first non-embedding model
            for name in model_names:
                if name and "embed" not in name:
                    return name
    except Exception:
        pass
    return DEFAULT_MODEL

def chat(question: str, context: str, history: str):
    model = get_model()
    prompt = f"""
    You are a helpful assistant. Answer ONLY using the provided context.
    
    Context:
    {context}
    
    History:
    {history}
    
    Question:
    {question}
    """
    
    response = ollama.chat(model=model, messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']