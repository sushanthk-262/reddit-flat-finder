import re
from config import KEYWORDS_REQUIRED, LOCATIONS, MIN_RENT, MAX_RENT

def normalize(text):
    return text.lower().replace(",", " ")


def extract_numbers(text):
    nums = re.findall(r"\d{4,6}", text)
    return [int(n) for n in nums]


def rent_match(text, min_rent, max_rent):
    for n in extract_numbers(text):
        if min_rent <= n <= max_rent:
            return True
    return False


def keyword_match(text, words):
    return any(re.search(r'\b' + w + r'\b', text) for w in words)


def location_match(text, locations):
    return any(loc in text for loc in locations)


def matches_filters(text):
    """Check if text matches all filter criteria"""
    text = normalize(text)
    return (
        keyword_match(text, KEYWORDS_REQUIRED) and
        location_match(text, LOCATIONS) and
        rent_match(text, MIN_RENT, MAX_RENT)
    )
