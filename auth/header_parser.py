import json
from ytmusicapi import setup

def parse_headers(raw_text: str) -> str:
    if "fetch(" in raw_text:
        converted = parse_fetch_format(raw_text)
    else:
        converted = convert_headers(raw_text)
    return setup(filepath=None, headers_raw=converted)

def parse_fetch_format(raw: str) -> str:
    headers_start = raw.index('"headers"')
    brace_start = raw.index('{', headers_start)
    brace_end = raw.index('}', brace_start)
    headers_json = raw[brace_start:brace_end + 1]
    headers_dict = json.loads(headers_json)
    lines = [f"{k}: {v}" for k, v in headers_dict.items()]
    return "\n".join(lines)

def convert_headers(raw: str) -> str:
    lines = raw.strip().split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if line.islower() and " " not in line:
            key = line
            value = lines[i + 1].strip() if i + 1 < len(lines) else ""
            result.append(f"{key}: {value}")
            i += 2
        else:
            i += 1

    return "\n".join(result)