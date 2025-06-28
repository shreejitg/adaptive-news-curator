# file: intelligent_retriever.py
import chromadb
import datetime
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv

# -- SETUP --
load_dotenv()
# This is the heart of our new memory system.
# We will use a local, file-based ChromaDB instance.
client = chromadb.PersistentClient(path="./chroma_db")

# Use a standard, high-quality embedding model from OpenAI.
embedding_function = OpenAIEmbeddings()

# Initialize the Chroma vector store.
# It will use the embedding function to convert text to vectors.
vector_store = Chroma(
    client=client,
    collection_name="news_feedback",
    embedding_function=embedding_function,
)

# This is a key parameter for our time decay function.
# A smaller value means a slower decay (older items remain relevant longer).
# Decay formula is f(x) = a(b)^x where a is initial amount, b is **decay factor** and x is age. 
# Decay factor b = (1-r) where r is **decay rate**.
TIME_DECAY_RATE = 0.1

# --- FREQUENCY ANALYSIS ---

def get_topic_frequencies() -> str:
    """
    Analyzes the most recent 'liked' articles to find frequent topics,
    which will guide our new search.
    """
    # Get the 20 most recent documents to analyze for topics
    recent_docs = vector_store.get(include=["metadatas"], limit=20)
    
    liked_summaries = [
        meta['title'] for meta in recent_docs['metadatas'] 
        if meta.get('rating') == 1
    ]
    
    if not liked_summaries:
        return "general technology and AI breakthroughs"

    # Use an LLM to find the patterns in what the user likes
    topic_analysis_prompt = ChatPromptTemplate.from_template("""
    Based on the following list of liked article titles, identify the 2-3 most frequent and prominent topics or themes.
    Be concise and list the topics as a comma-separated string.

    Example: "AI in drug discovery, advancements in quantum computing, venture capital funding for tech startups"

    Article Titles:
    {titles}

    Prominent Topics:
    """)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    topic_chain = topic_analysis_prompt | llm | StrOutputParser()
    
    topics = topic_chain.invoke({"titles": "\n".join(liked_summaries)})
    print(f"🔎 Identified frequent topics: {topics}")
    return topics


# --- RETRIEVAL AND RE-RANKING ---

def retrieve_and_rerank_feedback(query: str, top_k: int = 10) -> str:
    """
    Performs semantic search and then re-ranks the results based on time decay.
    """
    # 1. Perform the initial semantic search
    docs_with_scores = vector_store.similarity_search_with_relevance_scores(query, k=top_k)
    
    if not docs_with_scores:
        return "No relevant feedback history found."

    reranked_results = []
    current_time = datetime.datetime.now()

    # 2. Apply time decay to scores
    for doc, score in docs_with_scores:
        metadata = doc.metadata
        doc_time = datetime.datetime.fromisoformat(metadata['timestamp'])
        age_in_days = (current_time - doc_time).total_seconds() / (60 * 60 * 24)
        
        # Exponential decay formula
        decay_factor = (1-TIME_DECAY_RATE) ** age_in_days
        
        # Combine semantic score with time decay
        # We also boost 'liked' articles slightly over 'disliked' ones in the ranking
        rating_boost = 1.0 if metadata['rating'] == 1 else 0.95
        final_score = score * decay_factor * rating_boost
        
        reranked_results.append((doc, final_score))

    # 3. Sort by the new, final score
    reranked_results.sort(key=lambda x: x[1], reverse=True)

    # 4. Format for the agent
    context = "Here is a summary of the user's most relevant past feedback, ranked by relevance and recency:\n\n"
    for doc, score in reranked_results[:5]: # Provide the top 5 after re-ranking
        rating = "Liked" if doc.metadata['rating'] == 1 else "Disliked"
        context += f"- {rating} article titled '{doc.metadata['title']}'\n"
        context += f"  Summary: {doc.page_content}\n\n"
        
    return context

def get_intelligent_context():
    """The main function that combines frequency analysis and retrieval."""
    # Frequency Weighting: Use frequent topics to create the search query
    frequent_topics = get_topic_frequencies()
    
    # Retrieval & Re-ranking: Use the topics to find and rank relevant memories
    context = retrieve_and_rerank_feedback(query=frequent_topics)
    return context