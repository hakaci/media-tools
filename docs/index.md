# Media Tools CLI

## Commands

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
media-tools download --channel <channel_name> [--limit N]
```

| Option    | Description                      | Default |
| --------- | -------------------------------- | ------- |
| --channel | Channel name from CSV (required) | None    |
| --limit   | Number of videos to download     | 10      |

### Example
```bash
media-tools download --channel "Music"
media-tools download --channel "Music" --limit 20
```

## metadata

Append YouTube video metadata into CSV.

### Usage
```bash
media-tools metadata [--url URL] [--playlist URL]
```

| Option     | Description             | Default |
| ---------- | ----------------------- | ------- |
| --url      | Single video URL(s)     | None    |
| --playlist | Playlist or channel URL | None    |

### Example
```bash
media-tools metadata --url https://youtube.com/watch?v=xxxx
media-tools metadata --url url1 --url url2
media-tools metadata --playlist https://youtube.com/playlist?list=xxxx
```


## Notes
All commands are fully CLI-based (no interactive mode)
CSV is used as central metadata storage
Default paths are defined in constants.py
Multiple --url values are supported in metadata command