from typing import List
from models.track import Track
from auth.auth_manager import AuthManager
from urllib.parse import urlparse,parse_qs


class PlaylistScanner:

    def __init__(self, auth_manager: AuthManager):
        self._client = auth_manager.get_client()


    def scan(self, playlist_url: str) -> List[Track]:
        playlist_id =self._extract_playlist_id(url=playlist_url)
        tracks =self._fetch_raw_tracks(playlist_id=playlist_id)
        parsed_track = [self._parse_track(raw=track) for track in tracks]
        return parsed_track

    def _extract_playlist_id(self, url: str) -> str:
        # sample youtubeMusicURL : https://music.youtube.com/playlist?list=RDCLAK5uy_n9Fbdw7e6ap-98_A-8JYBmPv64v-Uaq1g
        if "://" not in url:
            return url
        parsed = urlparse(url)
        playlist_id = parse_qs(parsed.query).get("list",[None])[0]
        return playlist_id

    def _fetch_raw_tracks(self, playlist_id: str) -> List[dict]:
        playlist = self._client.get_playlist(playlist_id,limit=None)
        tracks = playlist.get("tracks",[])
        return tracks


    def _parse_track(self, raw: dict) -> Track:
        artists = raw.get("artists", [])
        artist = ", ".join(a["name"] for a in artists) if artists else "Unknown"

        return Track(
            title=raw["title"],
            artist=artist,
            album=raw["album"]["name"] if raw.get("album") else None,
            year=None,
            video_id= raw.get("videoId"),
            musicbrainz_id = None,
            duration_seconds=raw.get("duration_seconds"),
            source="ytmusic"
        )
