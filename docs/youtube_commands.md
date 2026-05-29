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