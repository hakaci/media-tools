import re


def parse_timestamps(file_path):
    timestamps = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # match: 00:00 or 00:00:00 followed by anything
            match = re.match(r"(\d{1,2}:\d{2}(?::\d{2})?)\s*[|\-]?\s*(.+)", line)

            if match:
                timestamps.append((match.group(1), match.group(2)))

    return timestamps

def convert_time_to_seconds(time_str):
    parts = list(map(int, time_str.split(":")))

    if len(parts) == 2:  # MM:SS
        minutes, seconds = parts
        return minutes * 60 + seconds

    elif len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds

    return 0

def sanitize_filename(name):
    """Removes invalid characters for filenames."""
    return re.sub(r'[<>:"/\\|?*]', '_', name)