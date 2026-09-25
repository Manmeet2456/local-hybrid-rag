from memory.history import add_message, get_history
from retrieval.retriever import retrieve
from llm.chat import chat

def ask(question, session_id):
    # 1. Retrieve relevant chunks
    chunks = retrieve(question)
    
    # 2. Join the text from chunks into a single context string
    context = "\n\n".join([chunk["text"] for chunk in chunks])
    
    # 3. Get conversation history for this session
    history = get_history(session_id)
    
    # 4. Generate answer using the LLM
    answer = chat(question = question, context = context, history = history)
    
    # 5. Save the interaction to memory
    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)
    
    sources = [
        {
            "text": chunk.get("text", ""),
            "filename": chunk.get("filename", "Document")
        }
        for chunk in chunks
    ]
    return {
        "answer": answer,
        "sources": sources
    }