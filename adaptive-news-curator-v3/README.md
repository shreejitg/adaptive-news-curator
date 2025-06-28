# adaptive-news-curator

## V3 - Vector DB based user profile
1. Starts with empty vector db of feedback and base search query
1. Search query is made to Tavily with base search query
1. User is asked for feedback, which is then saved into vector db.
1. Upon next loop, vector db is queried for 2-3 most frequently liked topics
1. These topics are then used to query the vector db to rerank and fetch the top 5 most relevant articles liked/disliked by the user
1. These articles are then fed into the ChatGpt prompt to serve as user context. All seen urls are also fed into seen urls to prevent duplication of results.

## Setup

None

## Main Loop

Run 
```
python main_curator.py
```