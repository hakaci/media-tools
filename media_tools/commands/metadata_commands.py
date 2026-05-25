import argparse
from media_tools.youtube.append_metadata import (
    append_single_video_metadata,
    append_playlist_metadata
)


def run(args):
    # CLI parser setup
    parser = argparse.ArgumentParser(
        prog="media-tools metadata",
        description="Append YouTube metadata into CSV"
    )

    parser.add_argument("--url", action="append")
    parser.add_argument("--playlist")

    p = parser.parse_args(args)

    # Interactive mode (no args)
    if not p.url and not p.playlist:

        print("\n1: Single video URLs")
        print("2: Playlist / channel URL")

        choice = input("\nSelect: ").strip()

        # Single video mode
        if choice == "1":
            urls = []

            while True:
                u = input("URL (0 to stop): ").strip()

                if u == "0":
                    break

                urls.append(u)

            append_single_video_metadata(urls)

        # Playlist mode
        elif choice == "2":
            u = input("\nPlaylist URL: ").strip()
            append_playlist_metadata(u)

        else:
            print("Invalid choice")

        return

    # CLI mode (args provided)
    if p.url:
        append_single_video_metadata(p.url)

    if p.playlist:
        append_playlist_metadata(p.playlist)