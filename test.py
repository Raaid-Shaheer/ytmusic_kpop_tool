from clients.musicbrainz_client import MusicBrainzClient
from core.discography_fetcher import DiscographyFetcher

mb_client = MusicBrainzClient()
fetcher = DiscographyFetcher(mb_client=mb_client)

tracks = fetcher.get_discography("BLACKPINK")

print(f"Found {len(tracks)} tracks\n")
for track in tracks[:5]:
    print(track)