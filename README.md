# Adaptive News Curator 🚀📰

**Your Personalized, AI-Powered News Experience!**

Stay ahead of the curve with an intelligent news curator that adapts to your interests, learns from your feedback, and delivers the stories that matter most to you. Powered by advanced AI agents and seamless feedback integration, Adaptive News Curator evolves with every article you read.

---

## ✨ Versions at a Glance

- **V1: Smart Feedback Loop**
  - Simple SQLite database tracks your likes/dislikes.
  - AI agents use your feedback to refine future news recommendations.
  - Agents:
    - User Feedback Retrieval
    - Search Agent

- **V2: Profile-Driven Curation**
  - AI condenses your feedback into evolving user themes using ChatGPT.
  - Personalized profiles drive smarter, more relevant news results.
  - Agents:
    - User Profile Synthesizer
    - Search Agent

- **V3: Next-Gen Vector Intelligence**
  - Vector database powers deep theme analysis and age-weighted reranking.
  - Delivers the most relevant, timely articles based on your evolving interests.
  - Agents:
    - Feedback Theme Synthesizer
    - Age-Weighted Theme Reranker
    - Search Agent

---

## 🚦 Quick Start

### 1. API Keys

Each version requires a `.env` file with:

```
OPENAI_API_KEY="sk-..."
TAVILY_API_KEY="tvly-..."
```

Get your OpenAI API key [here](https://platform.openai.com/api-keys) and your Tavily API key [here](https://tavily.com).

### 2. Database Setup
For V1 and V2, run `python database_setup.py` before starting the main app with `python main_curator.py`.

---

**Ready to experience the future of news? Dive into any version folder and get started!**