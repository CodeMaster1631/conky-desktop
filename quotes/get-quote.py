#!/usr/bin/env python3

import json
import hashlib
import datetime
import textwrap

QUOTES_FILE = "/home/abby/.config/conky/quotes/quotes.json"

with open(QUOTES_FILE, "r", encoding="utf-8") as f:
    quotes = json.load(f)

# Keep only usable quotes
quotes = [
    q for q in quotes
    if q.get("text") and q.get("author")
]

# Remove duplicate quote text
unique = {}
for q in quotes:
    unique[q["text"].strip()] = q

quotes = list(unique.values())

# Create a deterministic but randomized order.
# The order stays the same, but looks random.
seed = "stellar-daily-quotes"
quotes.sort(
    key=lambda q: hashlib.sha256(
        (seed + q["text"]).encode("utf-8")
    ).hexdigest()
)

# Number of days since Unix epoch.
# This means we advance exactly one quote every day.
today = datetime.date.today()
days = (today - datetime.date(1970, 1, 1)).days

quote = quotes[days % len(quotes)]

text = quote["text"].strip()
author = quote["author"].strip()

# Keep the quote visually suitable for your Conky.
lines = textwrap.wrap(
    text,
    width=42,
    break_long_words=False,
    break_on_hyphens=False
)

for line in lines:
    print(line)

print(f"— {author}")
