# file: profile_manager.py
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def get_all_feedback() -> dict:
    """Gets all feedback from the database."""
    conn = sqlite3.connect('news_curator.db')
    cursor = conn.cursor()
    cursor.execute("SELECT summary FROM news_feedback WHERE rating = 1")
    liked = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT summary FROM news_feedback WHERE rating = -1")
    disliked = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"liked": liked, "disliked": disliked}

# The Profile Synthesizer Chain
prompt_template = ChatPromptTemplate.from_template("""
You are a brilliant profile analyst. Based on the following liked and disliked article summaries,
synthesize a dense, coherent paragraph describing this user's interests, preferences, and topics to avoid.
Focus on extracting thematic patterns.

Liked Articles:
{liked}

Disliked Articles:
{disliked}

Synthesized User Profile:
""")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0) # Cheaper model is fine for this

# LCEL Chain to create the profile
profile_synthesis_chain = (
    {"liked": (lambda x: x['liked']), "disliked": (lambda x: x['disliked'])}
    | prompt_template
    | llm
    | StrOutputParser()
)

def update_and_get_user_profile() -> str:
    """
    Fetches all feedback, synthesizes it into a profile, and returns the profile.
    In a real app, you'd save this to a file or a new DB table to avoid re-computing it every time.
    """
    print("Synthesizing user profile from feedback history...")
    feedback_data = get_all_feedback()
    if not feedback_data["liked"] and not feedback_data["disliked"]:
        return "No feedback history found. The user is interested in 'breakthroughs in artificial intelligence'."
    
    user_profile = profile_synthesis_chain.invoke(feedback_data)
    print("Profile synthesis complete.")
    return user_profile