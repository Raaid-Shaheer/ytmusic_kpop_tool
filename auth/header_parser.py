

from ytmusicapi import setup

def parse_headers(raw_text: str) -> str:  # now returns a JSON string
    converted = convert_headers(raw_text)
    return setup(filepath=None, headers_raw=converted)

def convert_headers(raw: str) -> str:
    lines = raw.strip().split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Check if this line is a key (single lowercase word)
        if line.islower() and " " not in line:
            key = line
            # Next line is the value
            value = lines[i + 1].strip() if i + 1 < len(lines) else ""
            result.append(f"{key}: {value}")
            i += 2
        else:
            i += 1

    return "\n".join(result)