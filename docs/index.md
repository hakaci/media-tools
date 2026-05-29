# Media Tools CLI
CLI tool for organizing, converting, renaming and cleaning media files using ffmpeg and exiftool with metadata tracking.

## Setup

### 1. Create virtual environment
```bash
cd /path/to/media-tools
python -m venv .venv
```
Activate:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / Mac**
```bash
source .venv/bin/activate
```

### 2. Install project
```bash
pip install -e .
```

## External tools (PATH required)
- ffmpeg
- exiftool

## Run
```bash
media-tools <command>
```
or
```bash
python -m media_tools.main
```

## Commands
- file → file management (rename, convert, clean, organize)
- youtube → download & processing
- misc → utilities