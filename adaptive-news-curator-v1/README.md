# Adaptive News Curator V1 🚀

**Kickstart your personalized news journey!**

V1 is a simple yet powerful AI-driven news recommender that learns from your feedback to deliver ever-better articles—no repeats, no spam, just smarter news.

---

## 🧠 How It Works

1. Starts with a smart AI-powered search query.
2. Presents you with news articles and asks for your feedback (like/dislike).
3. Stores your feedback in a local SQLite database.
4. Prevents spamming Tavily search with built-in timeouts.
5. Refines future recommendations based on your feedback, ensuring you never see the same article twice.
6. Continuously improves with every interaction!

---

## ⚡ Quick Setup

1. Run the database setup at least once:

    ```bash
    python database_setup.py
    ```

---

## ▶️ Run the Main Loop

Start curating your news:

```bash
python main_curator.py
```

---

**Ready to get smarter news? Start now and let the AI learn what you love!**