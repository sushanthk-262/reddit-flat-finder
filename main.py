import sys
import requests
import pandas as pd
import logging
from datetime import datetime

from config import *
from filters import *
from send_email import send_mail

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEADERS = {
    "User-Agent": "flat-finder-bot/1.0"
}

PROXIES = None


def fetch_subreddit(sub):
    url = f"https://www.reddit.com/r/{sub}/new.json?limit={POST_LIMIT}"

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=20,
        proxies=PROXIES
    )

    r.raise_for_status()
    return r.json()["data"]["children"]


results = []
success_count = 0


for sub in SUBREDDITS:
    try:
        logging.info(f"Scanning r/{sub}")
        posts = fetch_subreddit(sub)
        success_count += 1

        for p in posts:
            d = p["data"]

            title = d["title"]
            body = d.get("selftext", "")
            text = (title + " " + body).lower()

            if not matches_filters(text):
                continue

            results.append({
                "subreddit": sub,
                "title": title,
                "url": "https://reddit.com" + d["permalink"],
                "created": datetime.fromtimestamp(d["created_utc"])
            })

    except requests.exceptions.Timeout:
        logging.error(f"{sub} timeout")

    except requests.exceptions.ConnectionError:
        logging.error(f"{sub} connection error")

    except requests.exceptions.HTTPError as e:
        logging.error(f"{sub} http error: {e}")

    except Exception as e:
        logging.error(f"{sub} unexpected error: {e}")


# Fail if nothing succeeded (what you wanted)
if success_count == 0:
    logging.critical("All subreddit fetches failed — exiting")
    sys.exit(1)


df = pd.DataFrame(results).drop_duplicates(subset=["url"])
df.to_csv(OUTPUT_FILE, index=False)

logging.info(f"Saved {len(df)} matches → {OUTPUT_FILE}")


if len(df) > 0:
    try:
        send_mail(OUTPUT_FILE)
    except Exception as e:
        logging.critical(f"Email failed: {e}")
        sys.exit(1)
else:
    logging.info("No matches — no email sent")
