## split
Split a media file into segments using timestamps.

### Usage
```bash
media-tools split <video_path> [options]
```
| Option             | Description                           | Default                                                            |
| ------------------ | ------------------------------------- | ------------------------------------------------------------------ |
| --timestamps       | Path to timestamps file               | `C:\Users\hakaci-desktop\Videos\video_split_output\timestamps.txt` |
| --output           | Output folder                         | `C:\Users\hakaci-desktop\Videos\video_split_output`                |
| --include-original | Keep original filename in output name | Off                                                                |

### Example
```bash
media-tools split "video.mp4" --output "C:\output"
media-tools split "video.mp4" --timestamps "C:\data\timestamps.txt"
```