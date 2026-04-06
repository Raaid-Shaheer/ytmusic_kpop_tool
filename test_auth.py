from auth.auth_manager import AuthManager

auth = AuthManager()
client = auth.get_client()

playlists = client.get_library_playlists(limit=20)
for p in playlists:
    print(f"{p['title']} -> {p['playlistId']}")


playlist = client.get_playlist("PLURfIY-yAalhne8d-OBemOtVMHo9BL2gO", limit=10)
import json
print(json.dumps(playlist['tracks'][0], indent=2))