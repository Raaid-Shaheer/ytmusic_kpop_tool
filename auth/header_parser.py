def parse_headers(raw_text: str) -> dict:
    lines = raw_text.strip().split("\n")
    headers = {}

    if len(lines)% 2 != 0 :
        raise ValueError("Invalid headers format, copy all headers and values")

    for i in range(0, len(lines), 2):
        name = lines[i].strip()
        value = lines[i+1].strip()

        if name.startswith(":"):
            continue

        headers[name] = value

    return headers


def validate_headers(headers: dict) -> list[str]:
    required = ["cookie", "authorization", "user-agent", "x-goog-authuser", "x-origin"]
    missing = []

    for field in required:
        if field not in headers :
            missing.append(field)

    return missing