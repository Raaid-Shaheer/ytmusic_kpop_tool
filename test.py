from auth.auth_manager import AuthManager
from core.playlist_scanner import PlaylistScanner
from core.discography_fetcher import DiscographyFetcher
from core.track_matcher import TrackMatcher
from clients.musicbrainz_client import MusicBrainzClient

# Setup
auth = AuthManager()
scanner = PlaylistScanner(auth_manager=auth)
mb_client = MusicBrainzClient()
fetcher = DiscographyFetcher(mb_client=mb_client)
matcher = TrackMatcher(auth_manager=auth)

# Step 1 — scan playlist
playlist_tracks = scanner.scan("https://music.youtube.com/playlist?list=RDCLAK5uy_l7wbVbkC-dG5fyEQQsBfjm_z3dLAhYyvo")
print(f"Scanned {len(playlist_tracks)} tracks")

# Step 2 — get discography
discography = fetcher.get_discography("BLACKPINK")
print(f"Discography has {len(discography)} tracks")

# Step 3 — filter playlist by artist
blackpink_in_playlist = matcher.filter_by_artist(playlist_tracks, "BLACKPINK")
print(f"BLACKPINK tracks in playlist: {len(blackpink_in_playlist)}")

# Step 4 — find missing
missing = matcher.find_missing(blackpink_in_playlist, discography)
print(f"Missing tracks: {len(missing)}")
for track in missing[:5]:
    print(f"  - {track.title}")

# Step 5 — resolve video ids
resolved = matcher.resolve_video_ids(missing)
print(f"Resolved {len(resolved)} video IDs")
for track in resolved[:5]:
    print(f"  - {track.title} | {track.video_id}")