from media_tools.video_splitter import split_video
import os

from media_tools.constants import DEFAULT_SPLIT_VIDEO_TIMESTAMPS_PATH, DEFAULT_SPLIT_OUTPUT_FOLDER


def run(args):
    if len(args) < 1:
        print("""
        Usage:
        media-tools split <video_path> [timestamps_path] [output_folder] [include_original]

        Arguments:
        video_path         Required. Path to input video
        timestamps_path    Optional. Default: C:\\Users\\hakaci-desktop\\Videos\\video_split_output\\timestamps.txt
        output_folder      Optional. Default: C:\\Users\\hakaci-desktop\\Videos\\video_split_output
        include_original   Optional. yes / no (default: yes)
        """)
        return

    video_path = args[0]

    timestamps_path = args[1] if len(args) >= 2 else DEFAULT_SPLIT_VIDEO_TIMESTAMPS_PATH
    output_folder = args[2] if len(args) >= 3 else DEFAULT_SPLIT_OUTPUT_FOLDER
    include_original_name = args[3].strip().lower() == "yes" if len(args) >= 4 else True

    if not os.path.exists(video_path):
        print("Error: video not found")
        return

    if not os.path.exists(timestamps_path):
        print(f"Error: timestamps file not found -> {timestamps_path}")
        return

    if len(args) >= 4 and args[3].strip().lower() not in ["yes", "no"]:
        print("include_original must be 'yes' or 'no'")
        return

    split_video(
        video_path=video_path,
        timestamps_path=timestamps_path,
        include_original_name=include_original_name,
        output_folder=output_folder
    )