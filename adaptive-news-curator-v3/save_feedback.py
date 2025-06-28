from intelligent_retriever import vector_store
import datetime
import uuid

def save_feedback_to_vector_store(summary: str, title: str, url: str, rating: int):
    """
    Embeds the article summary and saves it to the Chroma vector store
    with crucial metadata.
    """
    # We need a unique ID for each document
    doc_id = str(uuid.uuid4())
    
    # Metadata holds all the extra information we need for retrieval and decay
    metadata = {
        "title": title,
        "url": url,
        "rating": rating,
        "timestamp": datetime.datetime.now().isoformat() # ISO format is a standard way to store dates
    }
    
    # Add the document to the vector store.
    # Chroma automatically handles the embedding process.
    vector_store.add_texts(
        texts=[summary],
        metadatas=[metadata],
        ids=[doc_id]
    )
    print(f"✅ Feedback saved to vector store. (Rating: {rating})")