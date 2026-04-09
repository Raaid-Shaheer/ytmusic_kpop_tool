from typing import List
from models.track import Track
from clients.musicbrainz_client import MusicBrainzClient
import json
from pathlib import Path
from datetime import datetime, timedelta



class DiscographyFetcher:
    CACHE_EXPIRY_DAYS = 30

    def __init__(self, mb_client: MusicBrainzClient,cache_dir:str = "cache"):
        self._client = mb_client
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(exist_ok=True)


    def get_discography(self, artist_name: str) -> List[Track]:
        cache_file = self._cache_dir / f"{artist_name.lower()}.json"
        # Load from cache if valid
        if cache_file.exists() and self._is_cache_valid(cache_file):
            print(f"  Loading {artist_name} from cache...")
            return self._load_from_cache(cache_file, artist_name)

        # Otherwise fetch fresh and save
        print(f"  Fetching {artist_name} from MusicBrainz...")
        artist_id = self._client.get_artist_id(artist_name)
        recordings = self._client.get_recordings(artist_id)
        self._save_to_cache(cache_file, recordings)

        return [self._to_track(r, artist_name) for r in recordings]

    def _is_cache_valid(self, cache_file: Path) -> bool:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        cached_at = datetime.fromisoformat(data["cached_at"])
        return datetime.now() - cached_at < timedelta(days=self.CACHE_EXPIRY_DAYS)

    def _save_to_cache(self, cache_file: Path, recordings: list):
        data = {
            "cached_at": datetime.now().isoformat(),
            "recordings": recordings
        }
        cache_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"  Saved to cache: {cache_file.name}")

    def _load_from_cache(self, cache_file: Path, artist_name: str) -> List[Track]:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        return [self._to_track(r, artist_name) for r in data["recordings"]]

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