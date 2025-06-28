# file: main_curator.py
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search.tool import TavilySearchResults
import uuid
import datetime
from intelligent_retriever import get_intelligent_context, vector_store
from save_feedback import save_feedback_to_vector_store # Let's move save logic to its own file


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
# 3. UPDATED Agent Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a world-class Personalized News Curator. Your goal is to find ONE new, excellent article for the user.

You have been provided with a pre-analyzed summary of the user's preferences, ranked by relevance and recency.
Your job is to synthesize this information to find a fresh article the user will love.

<user_preferences>
{user_preferences}
</user_preferences>

Your Process:
1.  Deeply analyze the user's preferences provided above. Identify the core themes and topics they enjoy. Notice what they dislike.
2.  Formulate a creative and specific search query for the `tavily_search_results_json` tool. DO NOT search for topics identical to the titles you've just seen. Find a related but NEW angle.
3.  From the search results, select the ONE best article that is NOT on the list of previously recommended URLs.
4.  Provide a structured response with the article's title, a concise 2-3 sentence summary, and the URL.
"""),
    ("human", "Find a new article for me. Here are the URLs I have already seen, do not recommend them again: {seen_urls}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Create the Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. The Main Application Loop
def run_curator():
    print("--- Adaptive News Curator v2.0 (Vector Powered) ---")
    while True:
        # 1. GET CONTEXT: Use our intelligent retriever to get the best context
        user_preferences_context = get_intelligent_context()
        
        # 2. Get seen URLs to prevent duplication
        seen_docs = vector_store.get(include=["metadatas"])
        seen_urls = [meta['url'] for meta in seen_docs['metadatas']]

        # 3. INVOKE AGENT: Run the agent with the perfect, pre-processed context
        response = agent_executor.invoke({
            "user_preferences": user_preferences_context,
            "seen_urls": seen_urls
        })
        
        try:
            output_lines = response['output'].strip().split('\n')
            title = output_lines[0].replace("Title: ", "")
            summary = "\n".join(output_lines[1:-1]).replace("Summary: ", "")
            url = output_lines[-1].replace("URL: ", "")

            print("\n--- NEW RECOMMENDATION ---")
            print(f"📰 Title: {title}")
            print(f"📝 Summary: {summary}")
            print(f"🔗 URL: {url}")
            print("--------------------------")
            
            feedback = ""
            while feedback not in ['y', 'n']:
                feedback = input("Did you like this article? (y/n): ").lower()
            
            rating = 1 if feedback == 'y' else -1
            
            # 4. SAVE FEEDBACK: Save the new data to our vector store
            save_feedback_to_vector_store(summary, title, url, rating)

        except Exception as e:
            print(f"Sorry, there was an error processing the response: {e}")
            print(f"Agent raw output: {response.get('output', 'N/A')}")

        print(f"\nSearching for the next article in {timeout} seconds...")
        time.sleep(timeout)

if __name__ == "__main__":
    run_curator()