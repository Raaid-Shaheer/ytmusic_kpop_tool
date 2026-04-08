from typing import List
from models.track import Track
from clients.musicbrainz_client import MusicBrainzClient


class DiscographyFetcher:

    def __init__(self, mb_client: MusicBrainzClient):
        self._client = mb_client


    def get_discography(self, artist_name: str) -> List[Track]:
        artist_id = self._client.get_artist_id(artist_name)
        tracks = self._client.get_recordings(artist_id)
        return [self._to_track(track,artist_name) for track in tracks]

    def _to_track(self, recording: dict, artist_name: str) -> Track:
        return Track(
            title=recording["title"],
            artist= artist_name,
            album=None,  # MusicBrainz recordings don't give us this
            year=None,  # same
            video_id=None,  # filled in later by the matcher
            musicbrainz_id= recording["id"],
            duration_seconds=None,
            source= "musicbrainz"

        )