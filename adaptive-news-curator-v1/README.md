# adaptive-news-curator

## V1 - Simple storage based news feed recommender
1. Starts with base AI recommendation search query
1. Requests for feedback (y/n) and saves to sqlite db
1. Times out to prevent spamming Tavily search
1. Retrieves recommendations and forms new search query based on feedback, while ensuring no repeat articles are served.
1. Requests feedback to close loop

## Setup

1. Run
```bash
python database_setup.py
```
  at least once.

## Main Loop

Run 
```
python main_curator.py
```