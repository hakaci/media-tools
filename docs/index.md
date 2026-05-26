# Media Tools CLI

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

## download

Download YouTube videos from metadata CSV.

### Usage
```bash
media-tools youtube download [--channel NAME] [--limit N]
```

| Option    | Description                  | Default       |
| --------- | ---------------------------- | ------------- |
| --channel | Channel name from CSV        | (interactive) |
| --limit   | Number of videos to download | 10            |

### Behavior
- If --channel is missing → channel list is shown
- If --limit is missing → default is 10

### Example
```bash
media-tools youtube download --channel "Music"
media-tools youtube download --channel "Music" --limit 20
media-tools youtube download
```

## metadata

Append YouTube video metadata into CSV.

### Usage
```bash
media-tools youtube metadata [--url URL ...] [--playlist URL]
```

| Option     | Description             | Default |
| ---------- | ----------------------- | ------- |
| --url      | One or more video URLs  | None    |
| --playlist | Playlist or channel URL | None    |

### Example
```bash
media-tools youtube metadata --url https://youtube.com/watch?v=xxxx
media-tools youtube metadata --url url1 url2 url3
media-tools youtube metadata --playlist https://youtube.com/playlist?list=xxxx
```

## file

File management utilities.

### Usage
```bash
media-tools file <command>
```

## create-csv

Create metadata CSV from filesystem scan.

### Usage
```bash
media-tools file create-csv
```

## rename-all

Rename all files using metadata CSV mapping.

### Usage
```bash
media-tools file rename-all
```

## Notes

- Need ffmpeg and yt-dlp in CMD Path