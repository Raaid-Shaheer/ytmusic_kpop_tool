

from ytmusicapi import setup

def parse_headers(raw_text: str) -> str:  # now returns a JSON string
    return setup(filepath=None, headers_raw=raw_text)

