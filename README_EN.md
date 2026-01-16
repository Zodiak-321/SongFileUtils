# Music File Batch Processing Toolkit 🎵

[中文版本](README.md)

A collection of Python scripts for batch processing music file renaming, randomization, and deduplication. Now featuring enhanced V2 versions with advanced randomization capabilities.

## 📂 Script Overview

### 🎲 Random Prefix Tools (Single Letter Version)
For basic randomization needs, providing simple single-letter random prefixes.

#### 1. Add_Randomize_songs.py
**Function**: Adds random **single-letter** prefixes to music files for basic pseudo-random ordering  
**Purpose**: Creates a shuffle effect by adding random letter prefixes like `A_SongName.mp3`  
**Features**: 
- Supports multiple audio formats (MP3, FLAC, WMA, M4A, etc.)
- Automatically skips files that already have prefixes
- Generates 26 different uppercase letter prefix combinations

#### 2. Remove_Randomize_songs.py
**Function**: Removes random **single-letter** prefixes added by Add_Randomize  
**Purpose**: Restores original music filenames by removing "Letter_" prefixes  
**Features**: 
- Intelligently identifies single-letter prefix format
- Prevents filename conflicts
- Safe restoration without affecting non-prefixed files

### 🔢 Random Prefix Tools (Three-Character V2 Version)
**New!** Provides enhanced randomization with 46,656 prefix combinations.

#### 3. Add_Randomize_songs_V2.py
**Function**: Adds random **three-character** prefixes to music files for advanced pseudo-random ordering  
**Purpose**: Provides more thorough randomization with prefixes like `ABC_SongName.mp3` (e.g., `X7K_SongName.mp3`)  
**Features**: 
- **46,656 combinations**: First character A-Z, second and third characters A-Z or 0-9
- Enhanced randomness: Compared to V1 (26 combinations), V2 offers 46,656 combinations
- Supports additional audio formats (including .opus)
- True randomization: Shuffles file order before adding prefixes
- Intelligently identifies existing prefixes to avoid duplicate additions

#### 4. Remove_Randomize_songs_V2.py
**Function**: Removes **three-character** prefixes added by V2 and is compatible with V1 single-letter prefixes  
**Purpose**: Intelligently removes various prefix formats to restore original filenames  
**Features**: 
- **Dual compatibility**: Supports removing both `ABC_` (three-character) and `A_` (single-letter) prefixes
- Smart conflict detection: Automatically handles filename conflicts
- Detailed statistics report: Shows counts of restored, skipped, and no-prefix files

### 🔍 Duplicate Song Finder Tool

#### 5. Find_Duplicate_songs.py
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

## 📊 Version Comparison

| Feature | V1 (Single Letter) | V2 (Three Characters) |
|---------|-------------------|----------------------|
| Prefix Format | `A_SongName.mp3` | `ABC_SongName.mp3` |
| Combinations | 26 combinations | 46,656 combinations |
| Character Range | A-Z | First char A-Z, second/third chars A-Z/0-9 |
| Randomness | Basic | Enhanced |
| Compatibility | V1 format only | Compatible with both V1 and V2 formats |
| File Shuffling | No | Yes (shuffles before prefixing) |

## 🚀 Use Cases

1. **Basic Random Playback**: Use `Add_Randomize` for simple shuffle (26 combinations)
2. **Advanced Random Playback**: Use `Add_Randomize_V2` for thorough randomization (46,656 combinations)
3. **Restore Organization**: 
   - Use `Remove_Randomize` for V1 prefixed files
   - Use `Remove_Randomize_V2` for both V1 and V2 prefixed files
4. **Clean Duplicates**: Use `Find_Duplicate` to clean duplicate songs from music library, saving storage space

## ⚠️ Important Notes

- **Always backup important music files before using these scripts**
- V2 version provides stronger randomization, suitable for large music libraries
- V2 removal tool is compatible with both V1 and V2 formats
- `Find_Duplicate_songs.py` relies on standard filename formats; non-standard formats may not be recognized correctly
- Always use dry run mode to preview operations before performing deletions

## 📦 Requirements

- Python 3.x
- No additional dependencies required (uses standard libraries)

## 🛠️ Usage Instructions

1. Place the scripts in your music file directory
2. Run the desired script based on your needs:
   ```bash
   # V1 Version - Basic Randomization (26 combinations)
   python Add_Randomize_songs.py
   python Remove_Randomize_songs.py
   
   # V2 Version - Advanced Randomization (46,656 combinations)
   python Add_Randomize_songs_V2.py
   python Remove_Randomize_songs_V2.py
   
   # Duplicate Song Cleanup
   python Find_Duplicate_songs.py
   ```

## 🎯 Selection Recommendations

- **Small Music Library** (<100 songs): V1 version is sufficient
- **Medium Music Library** (100-500 songs): V1 version recommended
- **Large Music Library** (>500 songs): V2 version recommended for better randomization
- **Uncertain Requirements**: Start with V1, upgrade to V2 when needed

## 🔄 Version Migration

Migrating from V1 to V2:
1. First use `Remove_Randomize_songs.py` to remove V1 prefixes
2. Then use `Add_Randomize_songs_V2.py` to add V2 prefixes

Perfect for music enthusiasts who need to batch organize music libraries, clean duplicate files, or implement pseudo-random playback. The V2 version provides powerful randomization features for large music collections.

---

*For Chinese version, please see [README.md](README.md)*
