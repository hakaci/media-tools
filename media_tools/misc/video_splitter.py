import ffmpeg
import os
from media_tools.utils.general_utils import (
    parse_timestamps,
    convert_time_to_seconds,
    sanitize_filename,
)


def split_video(video_path, timestamps_path, include_original_name, output_folder):
    """Splits video into individual videos based on timestamps."""
    os.makedirs(output_folder, exist_ok=True)  # Ensure output directory exists
    original_name = os.path.splitext(os.path.basename(video_path))[
        0
    ]  # Extract original_name from video_path

    # Return list of timestamps and segment names
    timestamps = parse_timestamps(timestamps_path)

    for i in range(len(timestamps)):
        start_time = timestamps[i][0]
        segment_name = timestamps[i][1]
        start_seconds = convert_time_to_seconds(start_time)

        if i < len(timestamps) - 1:
            end_seconds = convert_time_to_seconds(timestamps[i + 1][0])
            duration = end_seconds - start_seconds
        else:
            duration = None  # Until end of video

        # Generate output filename based on user choice
        if include_original_name:
            safe_video_name = sanitize_filename(f"{original_name} - {segment_name}")
        else:
            safe_video_name = sanitize_filename(segment_name)

        output_file = os.path.join(output_folder, f"{safe_video_name}.mp4")

        try:
            # Run FFmpeg command
            input_stream = ffmpeg.input(video_path)

            if duration:
                (
                    input_stream.output(
                        output_file, ss=start_seconds, t=duration, codec="copy"
                    ).run(overwrite_output=True)
                )
            else:
                (
                    input_stream.output(
                        output_file, ss=start_seconds, codec="copy"
                    ).run(overwrite_output=True)
                )

            print(f"Saved: {output_file}")
        except ffmpeg.Error as e:
            print(f"FFmpeg error while processing {segment_name}: {e}")
