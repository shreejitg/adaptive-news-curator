# file: main_curator.py
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from custom_tools import save_feedback_to_db
from profile_manager import update_and_get_user_profile
import sqlite3

# 1. Setup
load_dotenv()
timeout = 5 # seconds

# 2. Initialize LLM and Tools
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
# NEW, SIMPLER TOOLS FOR THE CURATOR
search_tool = TavilySearchResults(max_results=5)
# The old custom tools are no longer needed for this agent.
tools = [search_tool] 

# 3. Create the Agent Prompt
# UPDATED AGENT PROMPT
# It now takes a 'user_profile' as input instead of figuring it out itself.
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a world-class Personalized News Curator. Your goal is to find a single, highly relevant news article for the user based on their profile.

This is the user's profile, which describes their interests:
<user_profile>
{user_profile}
</user_profile>

Your Process:
1.  Analyze the user profile to understand their tastes.
2.  Formulate a highly specific search query for the `tavily_search_results_json` tool to find a new article that matches their profile.
3.  From the search results, select the ONE best article. You must not recommend an article they have already seen.
4.  Provide a structured response with the article's title, a concise 2-3 sentence summary, and the URL.
"""),
    ("human", "Find a new, interesting article for me. Here are the URLs I've already seen: {seen_urls}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Create the Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. The Main Application Loop
def run_curator():
    print("--- Adaptive News Curator ---")
    while True:
        # 1. Synthesize the profile from ALL historical data
        user_profile = update_and_get_user_profile()
        
        # 2. Get URLs to avoid duplication
        # (This part still needs a direct DB call, but it's very lightweight)
        conn = sqlite3.connect('news_curator.db')
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM news_feedback")
        seen_urls = [row[0] for row in cursor.fetchall()]
        conn.close()

        # 3. Invoke the curator agent with the synthesized profile
        response = agent_executor.invoke({
            "user_profile": user_profile,
            "seen_urls": seen_urls
        })
        # The agent's raw output might have extra text; we need to parse it.
        # For simplicity, we assume the LLM follows instructions and the last part is the article.
        # A more robust solution would use response parsing or structured output.
        try:
            # Let's assume response['output'] is a string with Title, Summary, URL
            output_lines = response['output'].strip().split('\n')
            title = output_lines[0].replace("Title: ", "")
            summary = "\n".join(output_lines[1:-1]).replace("Summary: ", "")
            url = output_lines[-1].replace("URL: ", "")

            print("\n--- NEW RECOMMENDATION ---")
            print(f"📰 Title: {title}")
            print(f"📝 Summary: {summary}")
            print(f"🔗 URL: {url}")
            print("--------------------------")
            
            # Gather feedback
            feedback = ""
            while feedback not in ['y', 'n']:
                feedback = input("Did you like this article? (y/n): ").lower()
            
            rating = 1 if feedback == 'y' else -1
            
            # Save feedback for next time
            save_feedback_to_db(title, url, summary, rating)
            print("✅ Feedback saved. I will use this to improve future recommendations.")

        except (IndexError, AttributeError) as e:
            print(f"Sorry, I couldn't format a recommendation properly. Agent output: {response.get('output', 'N/A')}")

        print(f"\nSearching for the next article in {timeout} seconds...")
        time.sleep(timeout)


if __name__ == "__main__":
    run_curator()