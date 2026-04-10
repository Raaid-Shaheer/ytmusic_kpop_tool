from ytmusicapi import YTMusic
from flask import session
import json

from auth.exceptions import NotAuthenticatedError;


def get_ytmusic() -> YTMusic:
    headers = session.get("headers")

    if not headers:
        raise NotAuthenticatedError()

    client = YTMusic(auth=json.dumps(headers))
    print(" Authenticated with YouTube Music")
    return client