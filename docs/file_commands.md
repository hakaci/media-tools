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

## update-csv
Update metadata CSV by syncing filesystem changes.

### Usage
```bash
media-tools file update-csv
```

## rename-all
Rename all files using metadata CSV mapping.

### Usage
```bash
media-tools file rename-all
```

## convert
Convert supported video files to MP4 using ffmpeg.

### Usage
```bash
media-tools file convert
```

## rename
Rename newly added files and append them into metadata CSV.

### Usage
```bash
media-tools file rename
```

## clean
Remove metadata from media files using exiftool.

### Usage
```bash
media-tools file clean
```

## latest
Copy latest tracked files into temp folder.

### Usage
```bash
media-tools file latest
```

## replace
Replace strings inside filenames.

### Usage
```bash
media-tools file replace foo bar --with test
```

## organize
Organize and synchronize media archive.

### Usage
```bash
media-tools file organize
```

## remove-dash
Remove everything before and including the first "-" in filenames.

### Usage
```bash
media-tools file remove-dash <folder_path>
```

## Notes
- Need ffmpeg in CMD Path
- Need exiftool in CMD Path