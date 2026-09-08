#!/usr/bin/env python3

import json
import hashlib
import datetime
from argparse import ArgumentParser
from pathlib import Path

QUOTES_FILE = Path(__file__).with_name("quotes.json")

parser = ArgumentParser(description="Print the quote of the day.")
parser.add_argument(
    "--conky",
    action="store_true",
    help="format the output with Conky alignment and color directives",
)
args = parser.parse_args()

# Keep every quote within approximately the same horizontal space as the
# original two-line quote. Smaller fonts allow longer lines without making the
# widget wider; longer quotes therefore gain lines instead of overflowing.
LAYOUTS = (
    (55, 14, 42, 33),
    (105, 12, 49, 39),
    (170, 10, 59, 47),
    (float("inf"), 8, 74, 59),
)


def quote_layout(text):
    """Return the font size and line widths appropriate for a quote."""
    for maximum_length, font_size, first_line_width, later_line_width in LAYOUTS:
        if len(text) <= maximum_length:
            return font_size, first_line_width, later_line_width


def wrap_trapezium(text, first_line_width, later_line_width):
    """Wrap text into a wide first line and deliberately narrower later lines."""
    words = text.split()
    lines = []
    index = 0

    while index < len(words):
        first_line = not lines
        maximum_words = 5 if first_line else 4
        maximum_width = first_line_width if first_line else later_line_width
        line_words = []

        while index < len(words) and len(line_words) < maximum_words:
            candidate = " ".join(line_words + [words[index]])
            if line_words and len(candidate) > maximum_width:
                break
            line_words.append(words[index])
            index += 1

        # A single unusually long word still needs a line of its own.
        if not line_words:
            line_words.append(words[index])
            index += 1

        lines.append(" ".join(line_words))

    return lines

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
font_size, first_line_width, later_line_width = quote_layout(text)

# The quote area is trapezium-shaped: a wider first line and narrower lines
# underneath keep text clear of the artwork around the widget.
lines = wrap_trapezium(text, first_line_width, later_line_width)

for line in lines:
    if args.conky:
        print(
            f"${{alignc}}${{font JetBrains Mono Nerd Font:size={font_size}}}"
            f"${{color #d8d8d8}}{line}"
        )
    else:
        print(line)

if args.conky:
    print("${voffset 1}")
    print(
        f"${{alignc}}${{font JetBrains Mono Nerd Font:size={font_size}}}"
        f"${{color #a8a8a8}}— {author}${{font}}"
    )
else:
    print(f"— {author}")
