import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from collections import Counter
import re

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Load API key
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

#for storing the data
youtube_results = []

# Constants
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
QUERY = "riftbound"
MAX_RESULTS = 20 
DAYS_LIMIT = 7

def get_recent_video_ids():
    published_after = (datetime.utcnow() - timedelta(days=DAYS_LIMIT)).isoformat("T") + "Z"

    params = {
        "part": "snippet",
        "q": QUERY,
        "type": "video",
        "order": "date",
        "maxResults": MAX_RESULTS,
        "order": "viewCount",
        "publishedAfter": published_after,
        "key": API_KEY
    }

    res = requests.get(YOUTUBE_SEARCH_URL, params=params)
    res.raise_for_status()
    data = res.json()

    video_ids = [item["id"]["videoId"] for item in data.get("items", [])]
    return video_ids


def get_video_stats(video_ids):
    params = {
        "part": "snippet,statistics",
        "id": ",".join(video_ids),
        "key": API_KEY
    }

    res = requests.get(YOUTUBE_VIDEOS_URL, params=params)
    res.raise_for_status()
    data = res.json()

    videos = []
    cutoff_date = datetime.utcnow() - timedelta(days=DAYS_LIMIT)

    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        
        # Safely extract required fields
        title = snippet.get("title")
        channel = snippet.get("channelTitle")
        published_at = snippet.get("publishedAt")
        views = stats.get("viewCount")
        video_id = item.get("id")

        if not (title and views and published_at and video_id):
            continue  # Skip if data is incomplete

        # Parse the publishedAt timestamp
        published_dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
        if published_dt < cutoff_date:
            continue  # Skip if not recent

        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({
            "title": title,
            "channel": channel,
            "views": int(views),
            "url": url
        })

    # Sort by views descending
    return sorted(videos, key=lambda x: x["views"], reverse=True)


def extract_keywords(titles):
    words = []
    for title in titles:
        words += re.findall(r'\b\w+\b', title.lower())

    stopwords = {"the", "of", "and", "a", "to", "in", "is", "on", "for", "with", "by", "from", "at", "riftbound", "tcg", "league", "legends"}
    filtered = [word for word in words if word not in stopwords]
    return Counter(filtered).most_common(10)

def yt_main():
    video_ids = get_recent_video_ids()
    videos = get_video_stats(video_ids)

    youtube_results = videos[:5]
    keywords = extract_keywords([v["title"] for v in videos])

    return youtube_results, keywords

#yt_main()