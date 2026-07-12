import time
from typing import List
import re
from models.track import Track
from ytmusicapi import YTMusic


class TrackMatcher:

    # Suffixes that don't change the underlying song: (Live), (Remix), feat. X, - Remastered 2021, etc.
    _NOISE_PATTERNS = [
        r'\(.*?\)',                 # anything in parentheses
        r'\[.*?\]',                 # anything in brackets
        r'\bfeat\.?.*$',            # "feat. X" / "featuring X" to end of string
        r'\bft\.?.*$',
        r'-\s*live$',
        r'-\s*remaster(ed)?(\s*\d{2,4})?$',
        r'-\s*\d{4}\s*remaster(ed)?$',
    ]

    def __init__(self, client: YTMusic):
        self._client = client

    @staticmethod
    def _normalize_title(title: str) -> str:
        t = title.strip().lower()
        for pattern in TrackMatcher._NOISE_PATTERNS:
            t = re.sub(pattern, '', t, flags=re.IGNORECASE)
        t = re.sub(r'[^\w\s]', '', t)   # drop remaining punctuation
        return re.sub(r'\s+', ' ', t).strip()

    @staticmethod
    def _normalize_artist(artist: str) -> str:
        a = artist.strip().lower()
        a = re.sub(r'[^\w\s]', '', a)
        return re.sub(r'\s+', ' ', a).strip()

    def _matches_artist(self, track: Track, artist_name: str) -> bool:
        pattern = rf'\b{re.escape(artist_name)}\b'
        return bool(re.search(pattern, track.artist, re.IGNORECASE))

    def filter_by_artist(self, tracks: List[Track], artist_name: str) -> List[Track]:
        return [track for track in tracks if self._matches_artist(track, artist_name)]

    def find_missing(self, playlist_tracks: List[Track], discography_tracks: List[Track]) -> List[Track]:
        playlist_titles = {self._normalize_title(t.title) for t in playlist_tracks}
        return [t for t in discography_tracks if self._normalize_title(t.title) not in playlist_titles]

    def exclude_blacklisted(self, tracks: List[Track], blacklist_tracks: List[Track]) -> List[Track]:
        """Removes tracks that match a blacklisted (title, artist) pair. Does not touch
        tracks already sitting in a group playlist — this only blocks new additions."""
        blacklist_keys = {
            (self._normalize_title(t.title), self._normalize_artist(t.artist))
            for t in blacklist_tracks
        }
        return [
            t for t in tracks
            if (self._normalize_title(t.title), self._normalize_artist(t.artist)) not in blacklist_keys
        ]