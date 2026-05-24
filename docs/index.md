# Media Tools CLI

## Commands

### split
Splits a video into segments based on timestamps.

#### Usage
```bash
media-tools split <video_path> [timestamps_path] [output_folder] [include_original]

Arguments:
video_path         Required. Path to input video
timestamps_path    Optional. Default: C:\\Users\\hakaci-desktop\\Videos\\video_split_output\\timestamps.txt
output_folder      Optional. Default: C:\\Users\\hakaci-desktop\\Videos\\video_split_output
include_original   Optional. yes / no (default: yes)