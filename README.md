# Media Sorter

This Python program organizes and sorts photos, videos, and other media files based on their date of creation.

## Features
- **Sorts files by date**: Sorts photos, videos, and other files into year-month folders.
- **Duplicate detection**: Moves duplicate files (e.g., photo.jpg and photo_1.jpg) to a separate "duplicates" folder.
- **Supports multiple file formats**: Handles `.jpg`, `.jpeg`, `.png`, `.mp4`, `.mov`, `.aae`, and more.
- **EXIF support**: Uses EXIF metadata to determine the date a photo was taken. If EXIF data is not available, it uses the file modification date.
- **Recursive sorting**: Can recursively sort files in subfolders.
- **Multiple language support**: Currently, English and Turkish are supported.

## Installation
If you are using the `.exe` and `.app` for Windows and Mac respectively, just installing them is enough.
For other cases:

### Prerequisites
- Python 3.x
- Required Python libraries:
  - `Pillow` (for handling images and EXIF data)
  - `shutil` (for moving files)
  - `os` (for file operations)


> **Note**: This program was made specifically for my needs, I also may update it from time to time. However feel free to fork it and make modifications according to your needs! 
