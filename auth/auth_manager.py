from ytmusicapi import YTMusic
from flask import session


from auth.exceptions import NotAuthenticatedError;


def get_ytmusic() -> YTMusic:
    headers = session.get("headers")

    if not headers:
        raise NotAuthenticatedError()

    client = YTMusic(auth=headers)
    print(" Authenticated with YouTube Music")
    return client