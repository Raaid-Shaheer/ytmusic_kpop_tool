

def parse_headers(raw_text: str) -> dict:
    raw_lines = raw_text.strip().split("\n")

    if len(raw_lines) % 2 != 0:
        raise ValueError("Invalid headers format, copy all headers and values")

    # Loop 1 — filter invalid pairs
    cleaned = []
    for i in range(0, len(raw_lines), 2):
        name_line = raw_lines[i].strip()
        value_line = raw_lines[i + 1].strip()
        if _is_valid_header_name(name_line):
            cleaned.extend([name_line, value_line])

    # Loop 2 — parse cleaned lines into dict
    headers = {}
    for i in range(0, len(cleaned), 2):
        name = cleaned[i]
        value = cleaned[i + 1]
        if name.startswith(":"):
            continue
        headers[name] = value

    return headers

def _is_valid_header_name(name: str) -> bool:
    return name == name.lower() and " " not in name

def validate_headers(headers: dict) -> list[str]:
    required = ["cookie", "authorization", "user-agent", "x-goog-authuser", "x-origin"]
    missing = []

    for field in required:
        if field not in headers:
            missing.append(field)

    return missing