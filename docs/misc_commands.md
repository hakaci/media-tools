## split-video
Split a media file into segments using timestamps.

### Usage
```bash
media-tools misc split-video <video_path> [options]
```

| Option        | Description                           | Default                                                            |
| ------------- | ------------------------------------- | ------------------------------------------------------------------ |
| --timestamps  | Path to timestamps file               | `C:\Users\hakaci-desktop\Videos\video_split_output\timestamps.txt` |
| --output      | Output folder                         | `C:\Users\hakaci-desktop\Videos\video_split_output`                |
| --no-original | Disable original filename in outputs  | Off                                                                |

### Example
```bash
media-tools misc split-video "video.mp4"

media-tools misc split-video "video.mp4" --output "C:\output"

media-tools misc split-video "video.mp4" --timestamps "C:\data\timestamps.txt"

media-tools misc split-video "video.mp4" --no-original
```