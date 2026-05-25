def choose_channel(channel_names):
    """
    Display available channels
    and let user choose one.
    """

    print("\nAvailable channels:")

    # Print numbered channel list
    for index, channel in channel_names.items():
        print(f"{index}: {channel}")

    while True:
        try:
            # Ask user for selection
            choice = int(input("\nChoose channel number: "))

            # Validate selection
            if choice in channel_names:
                return channel_names[choice]

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")