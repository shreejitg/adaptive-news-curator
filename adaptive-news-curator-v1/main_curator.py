# file: main_curator.py
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools.tavily_search import TavilySearchResults
from custom_tools import read_past_feedback, get_previously_recommended_urls, save_feedback_to_db

# 1. Setup
load_dotenv()

# 2. Initialize LLM and Tools
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
search_tool = TavilySearchResults(max_results=5)
custom_tools = [read_past_feedback, get_previously_recommended_urls]
tools = [search_tool] + custom_tools

# 3. Create the Agent Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a world-class Personalized News Curator. Your goal is to find a single, highly relevant news article for the user that they have NOT seen before.

Your Process:
1.  First, understand the user's interests by using the `read_past_feedback` tool. This is your primary source of truth for their preferences.
2.  Based on their preferences, formulate a search query for the `tavily_search_results_json` tool.
3.  Analyze the search results. Check which URLs have already been recommended using the `get_previously_recommended_urls` tool.
4.  From the new, unrecommended articles, select the ONE that best matches the user's inferred interests.
5.  Provide a structured response with the article's title, a concise 2-3 sentence summary, and the URL. Do not make up information.

Your final output must be only the title, summary, and URL.
"""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Create the Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. The Main Application Loop
def run_curator():
    print("--- Adaptive News Curator ---")
    while True:
        # The input here is simple, the agent's real context comes from its tools
        user_input = "Find a new, interesting article for me."
        
        response = agent_executor.invoke({"input": user_input})
        
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

        print("\nSearching for the next article in 15 seconds...")
        time.sleep(15)


if __name__ == "__main__":
    run_curator()