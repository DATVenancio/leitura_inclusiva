# Audiobook Reader

A Python-based audiobook reader application built with tkinter GUI. This application allows users to browse and play audiobooks with a simple and intuitive interface.

## Features

- **Audiobook Library**: Browse and select from your audiobook collection
- **Audio Player**: Full-featured audio player with play, pause, stop, and seek controls
- **Progress Tracking**: Visual progress bar showing current playback position
- **Volume Control**: Adjustable volume levels
- **Simple Interface**: Clean and intuitive user interface

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. The application will open with the audiobook selection screen
3. Click on an audiobook to start playing
4. Use the player controls to manage playback

## Project Structure

```
leitura_inclusiva/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── gui/                   # GUI components
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── library_screen.py  # Audiobook selection screen
│   └── player_screen.py   # Audio player screen
├── core/                  # Core functionality
│   ├── __init__.py
│   ├── audio_player.py    # Audio playback engine
│   └── audiobook.py       # Audiobook data model
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── file_utils.py      # File handling utilities
│   └── audio_utils.py     # Audio processing utilities
└── data/                  # Application data
    └── audiobooks/        # Directory for audiobook files
```

## Supported Audio Formats

- MP3
- WAV
- OGG
- FLAC (with additional codecs)

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- pygame (for audio playback)
- pydub (for audio file handling)

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## License

This project is open source and available under the MIT License. 