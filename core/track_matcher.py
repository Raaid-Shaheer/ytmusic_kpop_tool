import time
from typing import List
import re
from models.track import Track
from auth.auth_manager import AuthManager


class TrackMatcher:

    def __init__(self, auth_manager: AuthManager):
        self._client = auth_manager.get_client()

    def _matches_artist(self, track: Track, artist_name: str) -> bool:
        pattern = rf'\b{re.escape(artist_name)}\b'
        return bool(re.search(pattern, track.artist, re.IGNORECASE))

    def filter_by_artist(self, tracks: List[Track], artist_name: str) -> List[Track]:

        return [track for track in tracks if self._matches_artist(track, artist_name)]

    def find_missing(self, playlist_tracks: List[Track], discography_tracks: List[Track]) -> List[Track]:

        playlist_titles = {track.title.strip().lower() for track in playlist_tracks}

        return [track for track in discography_tracks if track.title.strip().lower() not in playlist_titles]

    def resolve_video_ids(self, tracks: List[Track]) -> List[Track]:
        for track in tracks:
            results = self._client.search(f"{track.title} {track.artist}", filter="songs", limit=1)
            if results:
                track.video_id = results[0]["videoId"]
                time.sleep(0.5)
        return [track for track in tracks if track.video_id is not None]
