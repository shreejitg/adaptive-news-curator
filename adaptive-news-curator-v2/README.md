# adaptive-news-curator

## V2 - Storage and profile synthesis based news curator
1. Starts with base AI recommendation search query
1. Requests for feedback (y/n) and saves to sqlite db
1. Times out to prevent spamming Tavily search
1. Retrieves liked and disliked articles and forms an updated user profile using ChatGpt. Then uses the new user profile to formulate search query.
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