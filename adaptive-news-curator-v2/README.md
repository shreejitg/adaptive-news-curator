# Adaptive News Curator V2 🌟

**Smarter news, powered by your evolving profile!**

V2 takes personalization to the next level by synthesizing your feedback into a dynamic user profile using ChatGPT, ensuring every news recommendation is tailored just for you.

---

## 🧠 How It Works

1. Starts with an AI-driven search query.
2. Presents news articles and collects your feedback (like/dislike).
3. Stores your feedback in a local SQLite database.
4. Prevents spamming Tavily search with built-in timeouts.
5. Uses your feedback to update your user profile with ChatGPT, then crafts smarter search queries based on your interests.
6. Continuously adapts and improves with every interaction!

---

## ⚡ Quick Setup

1. Run the database setup at least once:

    ```bash
    python database_setup.py
    ```

---

## ▶️ Run the Main Loop

Start your personalized news curation:

```bash
python main_curator.py
```

---

**Experience news that evolves with you—start V2 and see the difference!**