# LivePhotos-2-GoogleMotion

A tool for creating Motion Photo v2 from HEIC or JPG files and videos. This project is a fork of the original MotionPhoto2 project, with added functionality through a `main.py` script for easier batch processing.

## Features

- Creates Motion Photo v2 compatible with Google Photos
- Preserves presentation timestamp for iPhone Live Photos
- Supports batch processing of directories

## Prerequisites

- [ExifTool](https://exiftool.org/)
- Python 3.x

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/bs10081/MotionPhoto2.git
   cd MotionPhoto2
   ```

2. Install ExifTool and ensure it's in the same directory as the script files.

## Usage

### Using the PowerShell script directly

To convert a single pair of image and video to Motion Photo v2:

```powershell
PS> .\MotionPhoto2.ps1 -imageFile ImageFile.HEIC -videoFile VideoFile.MOV -outputFile MotionPhoto.HEIC
```

### Using the Python script for batch processing

To process multiple files in a directory:

```bash
python main.py
```

When prompted, enter the source and output directory paths.

## Python Script Features

The `main.py` script provides the following functionality:

- Walks through the source directory recursively
- Processes Live Photos (HEIC + MOV pairs)
- Copies individual HEIC, MOV, and other file types
- Provides a detailed summary of processed files

## About

This fork builds upon the original MotionPhoto2 project, which was designed to mimic the Motion Photo v2 format used by Galaxy S20 FE phones. The added Python script enhances usability for batch processing of directories containing various file types.

## Contributing

Contributions to improve the script or add cross-platform compatibility are welcome. Please submit a pull request or open an issue for any bugs or feature requests.

## License

[Include the original license information here]

## Acknowledgements

- Original MotionPhoto2 project creator
- [@tribut](https://github.com/tribut) for providing a sample photo that made this project possible
