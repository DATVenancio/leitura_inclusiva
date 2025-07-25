"""
Audiobook class for managing audiobook metadata and information.
"""

from pathlib import Path
import os
from datetime import datetime


class Audiobook:
    """Represents an audiobook with metadata and file information."""
    
    def __init__(self, file_path):
        """Initialize an Audiobook object.
        
        Args:
            file_path: Path to the audiobook file
        """
        self.file_path = Path(file_path)
        self._load_metadata()
    
    def _load_metadata(self):
        """Load metadata from the audiobook file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Audiobook file not found: {self.file_path}")
        
        # Basic file information
        self.title = self.file_path.stem
        self.filename = self.file_path.name
        self.file_size = self.file_path.stat().st_size
        self.file_extension = self.file_path.suffix.lower()
        
        # File modification time
        mtime = self.file_path.stat().st_mtime
        self.modified_date = datetime.fromtimestamp(mtime)
        
        # Validate file format
        self._validate_format()
    
    def _validate_format(self):
        """Validate that the file is a supported audio format."""
        supported_formats = {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac'}
        if self.file_extension not in supported_formats:
            raise ValueError(f"Unsupported audio format: {self.file_extension}")
    
    @property
    def duration(self):
        """Get the duration of the audiobook in seconds."""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(str(self.file_path))
            return len(audio) / 1000.0  # Convert from milliseconds to seconds
        except ImportError:
            # Fallback if pydub is not available
            return 0
        except Exception as e:
            print(f"Error getting duration: {e}")
            return 0
    
    @property
    def formatted_duration(self):
        """Get the duration formatted as HH:MM:SS."""
        duration = self.duration
        if duration == 0:
            return "Unknown"
        
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    @property
    def formatted_size(self):
        """Get the file size formatted as human-readable string."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def get_info(self):
        """Get a dictionary with all audiobook information."""
        return {
            'title': self.title,
            'filename': self.filename,
            'file_path': str(self.file_path),
            'file_size': self.formatted_size,
            'file_extension': self.file_extension,
            'duration': self.formatted_duration,
            'modified_date': self.modified_date.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __str__(self):
        """String representation of the audiobook."""
        return f"Audiobook: {self.title} ({self.formatted_duration})"
    
    def __repr__(self):
        """Detailed string representation of the audiobook."""
        return f"Audiobook(title='{self.title}', path='{self.file_path}', duration='{self.formatted_duration}')" 