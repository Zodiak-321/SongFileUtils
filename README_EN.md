# Music File Batch Processing Toolkit 🎵

[中文版本](README.md)

A set of three Python scripts for batch processing music file renaming and deduplication.

## 📂 Script Overview

### 1. Add_Randomize_songs.py
**Function**: Adds random letter prefixes to music files for pseudo-random ordering  
**Purpose**: Creates a shuffle effect when players sort files alphabetically by adding prefixes like `A_SongName.mp3`, `K_SongName.mp3`  
**Features**: 
- Supports multiple audio formats (MP3, FLAC, WMA, M4A, etc.)
- Automatically skips files that already have prefixes
- Generates random uppercase letter prefixes

### 2. Remove_Randomize_songs.py
**Function**: Removes random letter prefixes added by Add_Randomize  
**Purpose**: Restores original music filenames by removing "Letter_" prefixes  
**Features**: 
- Intelligently identifies prefix format
- Prevents filename conflicts
- Safe restoration without affecting non-prefixed files

### 3. Find_Duplicate_songs.py
**Function**: Intelligently finds and handles duplicate song files  
**Purpose**: Automatically identifies duplicate songs with same title and artist, keeps high-quality versions, removes low-quality duplicates  
**Features**: 
- Standardized text comparison (ignores case, special characters)
- Intelligent quality detection (by file format, quality suffix, file size)
- Multiple safety modes:
  - Dry run (preview operations)
  - Safe mode (move to backup folder)
  - Direct delete mode
- Generates detailed operation logs
- Supports song format: `Song Title - Artist.ext` or `Song Title - Artist_Suffix.ext`

## 🚀 Use Cases

1. **Random Playback**: Use `Add_Randomize` to shuffle music playback order
2. **Restore Organization**: Use `Remove_Randomize` to restore original filenames
3. **Clean Duplicates**: Use `Find_Duplicate` to clean duplicate songs from music library, saving storage space

## ⚠️ Important Notes

- **Always backup important music files before using these scripts**
- `Find_Duplicate_songs.py` relies on standard filename formats; non-standard formats may not be recognized correctly
- Use dry run mode to preview operations before performing deletions

## 📦 Requirements

- Python 3.x
- No additional dependencies required (uses standard libraries)

## 🛠️ Usage Instructions

1. Place the scripts in your music file directory
2. Run the desired script:
   ```bash
   python Add_Randomize_songs.py
   python Remove_Randomize_songs.py
   python Find_Duplicate_songs.py
   ```

## 🔄 Script Functions Details

### Add_Randomize_songs.py
Adds a random uppercase letter prefix followed by an underscore to music filenames. This changes the alphabetical order when files are sorted by name, creating a pseudo-random shuffle effect. Files already having the format "Letter_SongName" are skipped.

### Remove_Randomize_songs.py
Reverses the process of Add_Randomize_songs.py by removing the "Letter_" prefix from filenames. It checks if a filename starts with a single uppercase letter followed by an underscore and restores the original name. Handles filename conflicts gracefully.

### Find_Duplicate_songs.py
A sophisticated duplicate finder that:
1. Normalizes song titles and artist names (removes special characters, converts to lowercase)
2. Groups songs with identical normalized titles and artists
3. Analyzes quality based on file format, quality suffixes (like `_320k`, `_flac`, `_hq`), and file size
4. Recommends which files to keep and which to delete
5. Offers multiple safety modes including backup creation

Perfect for music enthusiasts who need to batch organize music libraries, clean duplicate files, or implement pseudo-random playback.

---

*For Chinese version, please see [README.md](README.md)*
