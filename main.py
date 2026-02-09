import requests
import pandas as pd
import logging
from datetime import datetime

from config import *
from filters import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEADERS = {
    "User-Agent": "flat-finder-bot/1.0"
}

def fetch_subreddit(sub):
    url = f"https://www.reddit.com/r/{sub}/new.json?limit={POST_LIMIT}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["data"]["children"]


results = []

for sub in SUBREDDITS:
    logging.info(f"Scanning r/{sub}")

    try:
        posts = fetch_subreddit(sub)
    except Exception as e:
        logging.error(f"Error: {sub} {e}")
        continue

    for p in posts:
        d = p["data"]

        text = normalize(
            (d.get("title") or "") + " " + (d.get("selftext") or "")
        )

        if not keyword_match(text, KEYWORDS_REQUIRED):
            continue

        if not location_match(text, LOCATIONS):
            continue

        if not rent_match(text, MIN_RENT, MAX_RENT):
            continue

        results.append({
            "title": d["title"],
            "subreddit": sub,
            "url": "https://reddit.com" + d["permalink"],
            "score": d["score"],
            "created": datetime.utcfromtimestamp(d["created_utc"])
        })


df = pd.DataFrame(results).drop_duplicates(subset=["url"])
df.to_csv(OUTPUT_FILE, index=False)
logging.info(f"Saved {len(df)} matches → {OUTPUT_FILE}")
