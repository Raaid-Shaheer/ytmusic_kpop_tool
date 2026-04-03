from auth.auth_manager import AuthManager

auth = AuthManager()
client = auth.get_client()

# Fetch the library to confirm if the auth works
library = client.get_library_playlists(limit=5)
print(f"Total playlists found: {len(library)}")
print(library)

for playlist in library:
    print(f" Playlist: {playlist['title']}")