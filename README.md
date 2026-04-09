# YouTube Music K-pop Playlist Manager

Automatically organises your YouTube Music library by K-pop group or any artist for that matter.

## What it does
- Scans any YouTube Music playlist
- Creates dedicated playlists per group/artist (BLACKPINK, aespa, IVE...)
- Finds songs missing from your library using MusicBrainz
- Adds missing songs to new_groupname playlists

## Technical highlights
- ytmusicapi for YouTube Music (no official API exists)
- MusicBrainz for authoritative discography data
- Regex whole-word matching for artist filtering
- Idempotent playlist management (safe to run repeatedly)
- 30-day local cache to minimise API calls

## Setup
pip install -r requirements.txt  
ytmusicapi browser  
python main.py