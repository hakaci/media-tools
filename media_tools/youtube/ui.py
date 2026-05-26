from media_tools.youtube.csv_store import (
    get_metadata_csv_list,
    get_channels_list_from_csv
)

from media_tools.constants import HOARD_YOUTUBE_CSV_PATH


def choose_channel():
    """
    Display available channels
    and let user choose one.
    """
    rows = get_metadata_csv_list(HOARD_YOUTUBE_CSV_PATH)
    channels = get_channels_list_from_csv(rows)

    print("\nAvailable channels:")

    # Print numbered channel list
    for index, channel in channels.items():
        print(f"{index}: {channel}")

    while True:
        try:
            # Ask user for selection
            choice = int(input("\nChoose channel number: "))

            # Validate selection
            if choice in channels:
                return channels[choice]

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")