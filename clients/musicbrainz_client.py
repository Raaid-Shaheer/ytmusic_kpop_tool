import re
import time
import json
from typing import Optional
import musicbrainzngs


# Required by MusicBrainz to identify this app
musicbrainzngs.set_useragent("ytmusic-kpop-tool", "0.1", "sahlraaid52@gmail.com")


class MusicBrainzClient:
    def get_artist_id(self, artist_name: str) -> Optional[str]:
        search_result = musicbrainzngs.search_artists(query=artist_name, limit=1)
        artist_list = search_result.get("artist-list",[])
        if not artist_list:
            raise ValueError("No artist found for query")

        artist_id = artist_list[0]["id"]

        return artist_id
# Get recordings by artist ID
    def get_recordings(self,artist_id: str) -> list:
        all_recordings = []
        limit = 100
        offset = 0

        while True:
            result = musicbrainzngs.browse_recordings(
                artist=artist_id,
                limit=limit,
                offset=offset,
            )
            time.sleep(1)
            recordings = result.get("recording-list",[])
            total = int(result.get("recording-count",0))

            all_recordings.extend(recordings)
            print(f"  Fetched {len(all_recordings)}/{total} recordings...")
            # Stopping Condition
            if len(all_recordings) >= total:
                break
            offset += limit

        valid = [r for r in all_recordings if self._is_valid_recording(r)]
        return self._deduplicate(valid)

    def _is_valid_recording(self, recording: dict) -> bool:
        title = recording.get("title","")
        disambiguation= recording.get("disambiguation","")

        rem_keywords = ["edit","remix","inst.","-jp ver.-","instrumental","dance","behind the scenes","intro","bootleg","mix","interview","tour","acoustic","movie","version","performance","choreography","ver.","video","teaser","behind","film","movie","documentary","extended","trailer","clip","making","without","mc","opening"]

        if any(word in title.lower() for word in rem_keywords):
            return False
        if 'live' in disambiguation.lower() or 'japanese version' in disambiguation.lower():
           return False

        if not re.search(r'[a-zA-Z0-9가-힣]',title):
            return False
        if title.startswith("["):
            return False

        return True

    def _deduplicate(self, recordings: list) -> list:
        seen = set()
        unique = []

        for r in recordings:
            normalized = r.get("title","").lower().strip()
            normalized = normalized.replace("’", "'")
            if normalized not in seen:
                seen.add(normalized)
                unique.append(r)
        return unique


