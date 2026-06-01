from csv import reader
from media_tools.constants import HOARD_YOUTUBE_CSV_PATH

# CSV column structure
FIELDNAMES = [
    "id",
    "title",
    "channel",
    "timestamp",
    "download_status",
    "duration",
    "channel_id",
]


def get_metadata_csv_list(path):
    # Open metadata CSV file
    with open(path, newline="", encoding="utf-8") as metadataCSVfile:

        # get file reader object
        allMetadataRows = reader(metadataCSVfile, delimiter=",")

        return list(allMetadataRows)


def update_with_new_rows(new_rows):
    # Get rows
    updated_rows = get_metadata_csv_list(HOARD_YOUTUBE_CSV_PATH)
    # Collect existing video IDs
    existing_ids = {row[0] for row in updated_rows[1:]}

    # Add or update rows based on new_rows
    for new_row in new_rows:
        new_row = list(new_row.values())
        new_id = new_row[0]
        if new_id in existing_ids:
            for index, row in enumerate(updated_rows):
                if row[0] == new_id:
                    updated_rows[index] = new_row  # Update the existing row
        else:
            updated_rows.append(new_row)  # Add new row

    return updated_rows


def get_false_download_status_rows(rows, item_count_to_download):
    filtered_rows = []

    # Iterate over each row
    for row in rows:
        # Check if download_status is "False" (download_status is 5th column)
        if row[4] == "False":
            filtered_rows.append(row)

    # Calculate actual number of rows to process
    num_rows_to_process = min(item_count_to_download, len(filtered_rows))

    return filtered_rows[:num_rows_to_process]


def get_channels_list_from_csv(rows):
    # Collect unique channel names using a set to ensure uniqueness and by alphabetical
    channel_names = sorted({row[2] for row in rows[1:] if row[4] == "False"})

    # Create the dictionary with channel_names
    channel_names = {index + 1: channel for index, channel in enumerate(channel_names)}

    return channel_names


def get_relevant_video_infos(video_infos):
    # List to store metadata for each video
    all_video_metadata = []

    for video_info in video_infos:
        video_id = video_info.get("id")
        if not video_id:
            continue  # Skip if video ID is not available

        video_metadata = {
            "id": video_id,
            "title": video_info.get("title"),
            "channel": video_info.get("channel"),
            "timestamp": video_info.get("timestamp"),
            "download_status": False,
            "duration": video_info.get("duration"),
            "channel_id": video_info.get("channel_id"),
        }
        all_video_metadata.append(video_metadata)

    return all_video_metadata
