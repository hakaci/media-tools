def get_convenient_formats(formats):
    # Initialize an empty dictionary to store convenient formats
    convenient_formats = {}

    # Iterate through video formats
    for fmt in formats:
        # Extract width, height, vbr, and extension (ext) from the format
        width = fmt.get("width")
        height = fmt.get("height")
        vbr = fmt.get("vbr")
        ext = fmt.get("ext")

        # Skip formats that are None or higher than 1920x1080 or not MP4
        if (
            width is None
            or height is None
            or vbr is None
            or width > 1920
            or height > 1080
            or ext != "mp4"
        ):
            continue

        # Create a resolution tuple
        resolution = (width, height)

        # Check if the resolution tuple is already a key in the dictionary
        if resolution in convenient_formats:
            # Check if this format has a lower bitrate (vbr)
            if convenient_formats[resolution]["vbr"] is None or (
                vbr is not None and vbr < convenient_formats[resolution]["vbr"]
            ):
                convenient_formats[resolution] = fmt
        else:
            # Add the format to the convenient_formats dictionary
            convenient_formats[resolution] = fmt

    # Sort convenient_formats by resolution (descending order)
    sorted_formats = dict(
        sorted(convenient_formats.items(), key=lambda item: item[0], reverse=True)
    )

    return sorted_formats


def get_lowest_bitrate_format(formats):
    lowest_bitrate = float("inf")  # Start with a very high value
    selected_format = None

    for fmt in formats:
        format_bitrate = fmt.get("abr") or fmt.get("vbr") or float("inf")
        if format_bitrate < lowest_bitrate:
            lowest_bitrate = format_bitrate
            selected_format = fmt

    return selected_format
