# Adaptive News Curator

AI-enhanced news curator that learns from feedback using LangChain-chain based AI agents!

Navigate to one of the folders to try them out.

 - **V1**: Use a simple sqlite database to store all feedback on whether you liked or disliked an article. Use this history to ensure you get more relevant news results in the future.
    - Agents:
        - User feedback retrieval agent
        - Search agent
 - **V2**: Use a sqlite database based user profile condenser agent to generate themes using ChatGpt based on your recent feedback. Use these themes to get more relevant news results in the future.
    - Agents:
        - User profile synthesizer
        - Search agent
- **V3**: Use a vector database based user profile agent to identify themes in all of your feedback, while reranking and using the most relevant articles to get more relevant news results in the future
    - Agents:
        - User feedback theme synthesizer
        - Age weighted theme reranker
        - Search agent

# Setup

## 1. API keys

In each of the versions, you'll need a `.env` file with the following entries:

```
OPENAI_API_KEY="sk-..."
TAVILY_API_KEY="tvly-..."
```

Get an OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).

Get a Tavily API key from [tavily.com](https://tavily.com).

## 2. Database Setup
For V1 and V2, please run `python database_setup.py` before running the main loop using `python main_curator.py`.