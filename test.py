from clients.musicbrainz_client import MusicBrainzClient

client = MusicBrainzClient()
artist_id = client.get_artist_id("girls generation")
print(f"Artist ID: {artist_id}")

recordings = client.get_recordings(artist_id)
print(f"Found {len(recordings)} unique recordings")

for i, r in enumerate(recordings, 1):
    print(f"{i}. {r['title']} ")