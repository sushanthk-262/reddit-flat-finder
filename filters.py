import re

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
    return any(w in text for w in words)


def location_match(text, locations):
    return any(loc in text for loc in locations)
