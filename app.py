from flask import Flask, render_template, request,redirect, url_for, session, Response,stream_with_context
from auth.auth_manager import get_ytmusic
from config import SOURCE_PLAYLIST_URL, TARGET_GROUPS
from core.playlist_scanner import PlaylistScanner
from core.discography_fetcher import DiscographyFetcher
from core.track_matcher import TrackMatcher
from core.playlist_manager import PlaylistManager
from clients.musicbrainz_client import MusicBrainzClient
from auth.exceptions import NotAuthenticatedError
from auth.header_parser import parse_headers
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Initialise components once at startup

mb_client = MusicBrainzClient()
fetcher = DiscographyFetcher(mb_client=mb_client)

# Track last run in memory
last_run = {"time": None, "results": None}

def format_sse(message: dict) -> str:
    return "data: " + json.dumps(message) + "\n\n"

def process_playlist(playlist_url, selected_groups, scanner, matcher, manager):
    yield format_sse({"step": "Scanning playlist..."})
    playlist_tracks = scanner.scan(playlist_url)
    total_tracks = len(playlist_tracks)
    yield format_sse({"step": f"Found {total_tracks} tracks"})

    results = []

    for group in selected_groups:
        try:
            yield format_sse({"step": f"Fetching discography for {group}..."})
            discography = fetcher.get_discography(group)

            yield format_sse({"step": f"Finding missing tracks for {group}..."})
            group_in_playlist = matcher.filter_by_artist(playlist_tracks, group)
            missing = matcher.find_missing(group_in_playlist, discography)
            resolved = matcher.resolve_video_ids(missing)

            yield format_sse({"step": f"Updating playlists for {group}..."})
            manager.update_group_playlist(group, group_in_playlist)
            manager.rebuild_new_playlist(group, resolved)

            results.append({
                "group": group,
                "success": True,
                "in_playlist": len(group_in_playlist),
                "missing": len(missing),
                "resolved": len(resolved)
            })
            yield format_sse({"step": f"Done with {group}!", "group_done": True})



        except Exception as e:
            results.append({
                "group": group,
                "success": False,
                "error": str(e)
            })
            yield format_sse({"step": f"Error with {group}: {str(e)}", "error": True})

    session["results"] = results
    session["total_tracks"] = total_tracks

    yield format_sse({"done": True, "results": results, "total_tracks": total_tracks})



def _save_config():
    config_content = f'''# config.py — auto-updated
SOURCE_PLAYLIST_URL = "{SOURCE_PLAYLIST_URL}"
TARGET_GROUPS = {TARGET_GROUPS}
'''
    with open("config.py", "w") as f:
        f.write(config_content)



@app.route("/")
def home():
    if session.get("headers") is  None:
        return redirect(url_for("setup"))
    return render_template("index.html", groups=TARGET_GROUPS)


@app.route("/run", methods=["POST"])
def run():
    playlist_url = request.form.get("playlist_url", "").strip()
    selected_groups = request.form.getlist("groups")

    # save to session
    session["playlist_url"] = playlist_url
    session["groups"] = selected_groups

    # redirect to loading page
    return redirect(url_for("loading"))


@app.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        raw = request.form.get("headers", "")
        try:
            headers = parse_headers(raw)
        except Exception as e:
            return render_template("setup.html", error=str(e))
        session["headers"] = headers
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("setup.html")

@app.route("/delete-group", methods=["POST"])
def delete_group():
    group = request.form.get("group")
    if group in TARGET_GROUPS:
        TARGET_GROUPS.remove(group)
        _save_config()
    return redirect(url_for("home"))

@app.route("/add-group", methods=["POST"])
def add_group():
    group = request.form.get("group")
    TARGET_GROUPS.append(group)
    _save_config()
    return redirect(url_for("home"))

@app.route("/loading")
def loading():
    return render_template("loading.html")


@app.route("/stream")
def stream():
    def generate():
        playlist_url = session.get("playlist_url")
        selected_groups = session.get("groups")

        if not playlist_url or not selected_groups:
            yield format_sse({"error": "no session", "redirect": "/"})
            return

        try:
            ytmusic = get_ytmusic()
            scanner = PlaylistScanner(ytmusic)
            matcher = TrackMatcher(ytmusic)
            manager = PlaylistManager(ytmusic)
        except NotAuthenticatedError:
            yield format_sse({"error": "not authenticated", "redirect": "/setup"})
            return

        for event in process_playlist(playlist_url, selected_groups, scanner, matcher, manager):
            yield event

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream"
    )

@app.route("/results")
def results():
    results = session.get("results")
    total_tracks = session.get("total_tracks")

    if not results or not total_tracks:
        return redirect(url_for("home"))

    return render_template("results.html", results=results, total_tracks=total_tracks)

if __name__ == "__main__":
    app.run(debug=True)