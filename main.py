from ytmusicapi import YTMusic
from core.playlist_scanner import PlaylistScanner
from core.discography_fetcher import DiscographyFetcher
from core.track_matcher import TrackMatcher
from core.playlist_manager import PlaylistManager
from clients.musicbrainz_client import MusicBrainzClient
from config import SOURCE_PLAYLIST_URL, TARGET_GROUPS


def main():
    # Setup
    auth = AuthManager()
    scanner = PlaylistScanner(auth_manager=auth)
    mb_client = MusicBrainzClient()
    fetcher = DiscographyFetcher(mb_client=mb_client)
    matcher = TrackMatcher(auth_manager=auth)
    manager = PlaylistManager(auth_manager=auth)

    # Step 1 — scan playlist
    playlist_tracks = scanner.scan(SOURCE_PLAYLIST_URL)
    print(f"Scanned {len(playlist_tracks)} tracks")

    for group in TARGET_GROUPS:
        try:
            print(f"\n{'=' * 40}")
            print(f"  Processing: {group}")
            print(f"{'=' * 40}")

            discography = fetcher.get_discography(group)
            print(f"  Discography: {len(discography)} tracks")

            group_in_playlist = matcher.filter_by_artist(playlist_tracks, group)
            print(f"  In your playlist: {len(group_in_playlist)} tracks")

            missing = matcher.find_missing(group_in_playlist, discography)
            print(f"  Missing tracks: {len(missing)}")

            resolved = matcher.resolve_video_ids(missing)
            print(f"  Resolved: {len(resolved)} video IDs")

            manager.update_group_playlist(group, group_in_playlist)
            manager.rebuild_new_playlist(group, resolved)

        except ValueError as e:
            print(f"  ❌ Artist not found: {e}")
            continue
        except ConnectionError as e:
            print(f"  ❌ Network error: {e}")
            continue
        except Exception as e:
            print(f"  ❌ Unexpected error processing {group}: {e}")
            continue

    print(f"\n  Processed {len(TARGET_GROUPS)} groups!")
if __name__ == "__main__":
    main()