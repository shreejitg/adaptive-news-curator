# Adaptive News Curator

AI-enhanced news curator that learns from feedback.

Navigate to one of the folders to learn more about each version and capabilties.

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