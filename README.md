# K-pop Playlist Manager

A web tool that automatically organises your YouTube Music 
library by K-pop group using ytmusicapi and MusicBrainz.

## Features
- Scans any public YouTube Music playlist
- Creates dedicated playlists per group
- Finds missing songs using MusicBrainz discography data
- Monthly auto-scheduling via web UI
- 30-day local cache to minimise API calls

## Tech Stack
Python, Flask, ytmusicapi, MusicBrainz, APScheduler

## Setup
pip install -r requirements.txt
ytmusicapi browser
python app.py