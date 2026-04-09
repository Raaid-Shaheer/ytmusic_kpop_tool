from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import atexit

from config import SOURCE_PLAYLIST_URL, TARGET_GROUPS
from config import SCHEDULE_ENABLED, SCHEDULE_DAY, SCHEDULE_HOUR
from auth.auth_manager import AuthManager
from core.playlist_scanner import PlaylistScanner
from core.discography_fetcher import DiscographyFetcher
from core.track_matcher import TrackMatcher
from core.playlist_manager import PlaylistManager
from clients.musicbrainz_client import MusicBrainzClient

app = Flask(__name__)

# Initialise components once at startup
auth = AuthManager()
scanner = PlaylistScanner(auth_manager=auth)
mb_client = MusicBrainzClient()
fetcher = DiscographyFetcher(mb_client=mb_client)
matcher = TrackMatcher(auth_manager=auth)
manager = PlaylistManager(auth_manager=auth)

# Track last run in memory
last_run = {"time": None, "results": None}


def process_playlist(playlist_url: str, selected_groups: list) -> dict:
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


def scheduled_job():
    print(f"\n⏰ Scheduled run starting at {datetime.now()}")
    data = process_playlist(SOURCE_PLAYLIST_URL, TARGET_GROUPS)
    last_run["time"] = datetime.now()
    last_run["results"] = data["results"]
    print(f"⏰ Scheduled run complete")


# Start scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=scheduled_job,
    trigger=CronTrigger(
        day=SCHEDULE_DAY,     # day of month
        hour=SCHEDULE_HOUR,
        minute=0
    ),
    id="monthly_run",
    name="Monthly playlist update",
    replace_existing=True
)
scheduler.start()
print(f"⏰ Scheduler active — runs on day {SCHEDULE_DAY} of each month at {SCHEDULE_HOUR}:00")

@app.route("/")
def home():
    return render_template("index.html", groups=TARGET_GROUPS)


@app.route("/run", methods=["POST"])
def run():
    playlist_url = request.form.get("playlist_url", "").strip()
    selected_groups = request.form.getlist("groups")
    data = process_playlist(playlist_url, selected_groups)
    return render_template(
        "results.html",
        results=data["results"],
        total_tracks=data["total_tracks"]
    )


@app.route("/status")
def status():
    next_run = None
    if SCHEDULE_ENABLED and scheduler.running:
        job = scheduler.get_job("weekly_run")
        if job:
            next_run = job.next_run_time

    return render_template(
        "status.html",
        schedule_enabled=SCHEDULE_ENABLED,
        schedule_day=SCHEDULE_DAY,
        schedule_hour=SCHEDULE_HOUR,
        next_run=next_run,
        last_run=last_run
    )


@app.route("/run-now")
def run_now():
    scheduled_job()
    return render_template(
        "results.html",
        results=last_run["results"],
        total_tracks=0
    )

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    message = None

    if request.method == "POST":
        day = int(request.form.get("day", 1))
        hour = int(request.form.get("hour", 9))
        playlist_url = request.form.get("playlist_url", SOURCE_PLAYLIST_URL).strip()

        # Update the running scheduler
        if scheduler.running:
            scheduler.reschedule_job(
                "monthly_run",
                trigger=CronTrigger(day=day, hour=hour, minute=0)
            )

        # Persist to config so it survives restarts
        _save_schedule(day, hour, playlist_url)
        message = f"✅ Schedule updated — runs on day {day} of each month at {hour:02d}:00"

    # Get next run time
    next_run = None
    if scheduler.running:
        job = scheduler.get_job("monthly_run")
        if job:
            next_run = job.next_run_time

    return render_template(
        "schedule.html",
        next_run=next_run,
        schedule_day=SCHEDULE_DAY,
        schedule_hour=SCHEDULE_HOUR,
        playlist_url=SOURCE_PLAYLIST_URL,
        message=message
    )


def _save_schedule(day: int, hour: int, playlist_url: str):
    """Persist schedule settings to config.py so they survive restarts."""
    config_content = f'''# config.py — auto-updated by scheduler
SOURCE_PLAYLIST_URL = "{playlist_url}"

TARGET_GROUPS = {TARGET_GROUPS}

SCHEDULE_ENABLED = True
SCHEDULE_DAY = {day}
SCHEDULE_HOUR = {hour}
'''
    with open("config.py", "w") as f:
        f.write(config_content)


if __name__ == "__main__":
    app.run(debug=True)