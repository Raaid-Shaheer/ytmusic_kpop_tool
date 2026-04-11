from flask import Flask, render_template, request,redirect, url_for, session
from auth.auth_manager import get_ytmusic
from config import SOURCE_PLAYLIST_URL, TARGET_GROUPS
from core.playlist_scanner import PlaylistScanner
from core.discography_fetcher import DiscographyFetcher
from core.track_matcher import TrackMatcher
from core.playlist_manager import PlaylistManager
from clients.musicbrainz_client import MusicBrainzClient
from auth.exceptions import NotAuthenticatedError
from auth.header_parser import parse_headers,validate_headers
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-production")

# Initialise components once at startup

mb_client = MusicBrainzClient()
fetcher = DiscographyFetcher(mb_client=mb_client)

# Track last run in memory
last_run = {"time": None, "results": None}


def process_playlist(playlist_url: str, selected_groups: list,scanner,matcher,manager) -> dict:
    playlist_tracks = scanner.scan(playlist_url)
    total_tracks = len(playlist_tracks)
    results = []

    for group in selected_groups:
        try:
            discography = fetcher.get_discography(group)
            group_in_playlist = matcher.filter_by_artist(playlist_tracks, group)
            missing = matcher.find_missing(group_in_playlist, discography)
            resolved = matcher.resolve_video_ids(missing)

            manager.update_group_playlist(group, group_in_playlist)
            manager.rebuild_new_playlist(group, resolved)

            results.append({
                "group": group,
                "success": True,
                "in_playlist": len(group_in_playlist),
                "missing": len(missing),
                "resolved": len(resolved)
            })

        except ValueError as e:
            results.append({
                "group": group,
                "success": False,
                "error": str(e)
            })
        except Exception as e:
            results.append({
                "group": group,
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            })

    return {"total_tracks": total_tracks, "results": results}


@app.route("/")
def home():
    return render_template("index.html", groups=TARGET_GROUPS)


@app.route("/run", methods=["POST"])
def run():
    try:
        ytmusic = get_ytmusic()
        scanner = PlaylistScanner(ytmusic)
        matcher = TrackMatcher(ytmusic)
        manager = PlaylistManager(ytmusic)
        playlist_url = request.form.get("playlist_url", "").strip()
        selected_groups = request.form.getlist("groups")
        data = process_playlist(playlist_url, selected_groups,scanner, matcher, manager)
        return render_template(
            "results.html",
            results=data["results"],
            total_tracks=data["total_tracks"]
        )
    except NotAuthenticatedError:
        return redirect(url_for("setup"))


@app.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        raw = request.form.get("headers", "")
        try:
            headers = parse_headers(raw)
        except ValueError as e:
            return render_template("setup.html", error=str(e))
        missing_groups = validate_headers(headers)

        if missing_groups:
            return render_template("setup.html", missing=missing_groups)
        else:
            session["headers"] = headers
            return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)