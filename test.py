from auth.auth_manager import AuthManager
from core.playlist_scanner import PlaylistScanner

auth = AuthManager()
scanner = PlaylistScanner(auth_manager=auth)

# Paste a real public playlist URL here
tracks = scanner.scan("https://music.youtube.com/playlist?list=RDCLAK5uy_l7wbVbkC-dG5fyEQQsBfjm_z3dLAhYyvo")

print(f"Found {len(tracks)} tracks\n")
for track in tracks[:10]:
    print(track)
    print(f"{track.title} | video_id: {track.video_id}")