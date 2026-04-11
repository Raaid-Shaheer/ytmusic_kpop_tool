def convert_headers(raw: str) -> str:
    lines = raw.strip().split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Check if this line is a key (single lowercase word)
        if line.isalpha() and line.islower():
            key = line
            # Next line is the value
            value = lines[i + 1].strip() if i + 1 < len(lines) else ""
            result.append(f"{key}:{value}")
            i += 2
        else:
            i += 1

    return "\n".join(result)


raw = """accept
*/*
accept-encoding
gzip, deflate, br, zstd
accept-language
en-GB,en-US;q=0.9,en;q=0.8
authorization
SAPISIDHASH 1775906833_ba1510ea492185c4e4360cfdabea0c9b7f85b057_u SAPISID1PHASH 1775906833_ba1510ea492185c4e4360cfdabea0c9b7f85b057_u SAPISID3PHASH 1775906833_ba1510ea492185c4e4360cfdabea0c9b7f85b057_u
content-encoding
gzip
content-length
2422
content-type
application/json
cookie
HSID=Ag09FVId5mplIzIFe; SSID=AbEGJKo75oWkjPp-P; APISID=VIyxGaOtc8xPTdXW/ALeixSixIbsHmS0Iw; SAPISID=A0DEvrwuifWjsIUg/A77b0f7Bky-DNZYbg; __Secure-1PAPISID=A0DEvrwuifWjsIUg/A77b0f7Bky-DNZYbg; __Secure-3PAPISID=A0DEvrwuifWjsIUg/A77b0f7Bky-DNZYbg; VISITOR_INFO1_LIVE=lMeXWkzmfuo; VISITOR_PRIVACY_METADATA=CgJJThIEGgAgZQ%3D%3D; LOGIN_INFO=AFmmF2swRAIgOS1Vvp0V1Ph-Vv1BYROSSL_3mag3VQcvA5BwiZ9Zh44CIA_H1CE9bB4kCSSIONO8T2wfeMH5sz7ItNqtvjeqvUkX:QUQ3MjNmejNaTUtObUM2MjdrZ1p0a18yNi1sTjZEY3htblZmQ3NfVkhqX1R3VW5XU1JXSHZxWFVrMjd6WmpvSjdNUjJQaF9tMVB4TmhTNGJHWE1ISkEtSERsSzRzZlpfcVptMkxNQWZldGlxNlBxQThCRlhnN0pyUGlPVWp6RnhLWTRfTmdrYWxkb29MUG9IRW9pcGpNYXl6aEpBVDRFSm1R; PREF=f4=4000000&tz=Asia.Colombo&f5=30000&f7=100; __Secure-1PSIDTS=sidts-CjUBBj1CYjS09P1fYa9ZOeMKthJKyat6qDTnOaFvK35ufo-PTpBmFfc-2iMJpoPh93aSFo-zghAA; __Secure-3PSIDTS=sidts-CjUBBj1CYjS09P1fYa9ZOeMKthJKyat6qDTnOaFvK35ufo-PTpBmFfc-2iMJpoPh93aSFo-zghAA; __Secure-BUCKET=CPIB; YSC=BSJnLZHS3eo; __Secure-ROLLOUT_TOKEN=COjXuMn4--illQEQ_c314NuljgMYzoff-9DlkwM%3D; _gcl_au=1.1.1439800326.1775904813; SID=g.a0008winmPHN3jwOyhUqWe_q5sRtyO_A3ll8kIksXy6JhMgcKFjIoS7JPseFK6bhb8K67eyOHgACgYKAQgSARASFQHGX2MiX9NEjn5m3cXzULDsWQNXWRoVAUF8yKrU6aaonOhmmjMxj2XLzEmt0076; __Secure-1PSID=g.a0008winmPHN3jwOyhUqWe_q5sRtyO_A3ll8kIksXy6JhMgcKFjIMmONyVNN-p_IMwoibDFgjQACgYKARUSARASFQHGX2Mics-ERcAbKBT9THAA4WX3fxoVAUF8yKqqMl4_9Mp9q6vOPYkRVkzB0076; __Secure-3PSID=g.a0008winmPHN3jwOyhUqWe_q5sRtyO_A3ll8kIksXy6JhMgcKFjIfuxyosRNRK1tPZD_IvWJ4AACgYKAVMSARASFQHGX2MiOdrKJDxNibBhATob1kWkoxoVAUF8yKosNTM1CwolqZh2HJZMAgHa0076; CONSISTENCY=AH5K9rZl7667digqTkj0sHKcW0h7F7xisDWvtMaQp6HU8eqI8iAxGhc8UoW2J7DUxXOz2JcQK2RjttSYabAJBVQFUb4g6Hb6pOgwlXpgmR0NALq2rE6kVwvF6apzTf2yRMbVRjH2zzr1dl6hOSjdFT1_eahdfO-xdlnSQrvctnlKzw; SIDCC=AKEyXzVP1S2eCr3ZSjGJsJ7zqStY4W9QOsyvNj0GjLm0lBx0kGSO9bkJ5v-YBzRut86nuBojjxE; __Secure-1PSIDCC=AKEyXzXx_xsQ8491jrXKvRBVtTrftU9I7WkNQ4VmNXPdnt3xJCrDGrmAJrIWmFKC0pU3AqKg0zI; __Secure-3PSIDCC=AKEyXzVW41k8KbPg4D9YnWqHbWVpq8Krwj03sVmshnv9U3n5xBuO8MLrRQ2UE-kKlgtJZehor5w
dnt
1
origin
https://music.youtube.com
priority
u=1, i
referer
https://music.youtube.com/library
sec-ch-ua
"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"
sec-ch-ua-arch
"x86"
sec-ch-ua-bitness
"64"
sec-ch-ua-form-factors
"Desktop"
sec-ch-ua-full-version
"145.0.7632.160"
sec-ch-ua-full-version-list
"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.160", "Chromium";v="145.0.7632.160"
sec-ch-ua-mobile
?0
sec-ch-ua-model
""
sec-ch-ua-platform
"Windows"
sec-ch-ua-platform-version
"19.0.0"
sec-ch-ua-wow64
?0
sec-fetch-dest
empty
sec-fetch-mode
same-origin
sec-fetch-site
same-origin
user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36
x-browser-channel
stable
x-browser-copyright
Copyright 2026 Google LLC. All Rights reserved.
x-browser-validation
mGtxj/IERUi4uQ9hLSvZZF4DQgA=
x-browser-year
2026
x-client-data
CI+2yQEIo7bJAQipncoBCM7aygEIlKHLAQiFoM0BCJqszwEI1a3PAQjGr88BCLOwzwEIhbTPAQi4tM8BGOyFzwEY7KPPAQ==
Decoded:
message ClientVariations {
  // Active Google-visible variation IDs on this client. These are reported for analysis, but do not directly affect any server-side behavior.
  repeated int32 variation_id = [3300111, 3300131, 3313321, 3321166, 3330196, 3362821, 3397146, 3397333, 3397574, 3397683, 3398149, 3398200];
  // Active Google-visible variation IDs on this client that trigger server-side behavior. These are reported for analysis *and* directly affect server-side behavior.
  repeated int32 trigger_variation_id = [3392236, 3396076];
}
x-goog-authuser
0
x-goog-visitor-id
CgtsTWVYV2t6bWZ1byir0OjOBjIKCgJJThIEGgAgZQ%3D%3D
x-origin
https://music.youtube.com
x-youtube-bootstrap-logged-in
true
x-youtube-client-name
67
x-youtube-client-version
1.20260407.02.00"""

print(convert_headers(raw))