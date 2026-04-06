from dataclasses import dataclass,field
from typing import Optional

@dataclass
class Track:
    #---Identity Fields-----------
    title: str
    artist: str
    album: Optional[str] = None
    year: Optional[int] = None

    video_id: Optional[str] = None
    musicbrainz_id: Optional[str] = None

    duration_seconds: Optional[int] = None
    source: str = "unknown"

    def __repr__(self):
        return f"Track('{self.title}' by {self.artist}"

    def is_fully_matched(self) -> bool:
        """Returns True if this track has both a video_id and musicbrainz_id."""
        return self.video_id is not None and self.musicbrainz_id is not None