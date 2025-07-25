"""
File utility functions for the Audiobook Reader application.
"""

import sqlite3
from pathlib import Path
import os
import shutil
from typing import List, Dict, Optional

DB_PATH = Path(__file__).parent.parent / 'audiobook_progress.db'

def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS progress (
        audiobook_path TEXT PRIMARY KEY,
        position REAL
    )''')
    return conn

def save_position(audiobook_path, position):
    conn = _get_connection()
    with conn:
        conn.execute('''REPLACE INTO progress (audiobook_path, position) VALUES (?, ?)''', (str(audiobook_path), position))
    conn.close()

def get_position(audiobook_path):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT position FROM progress WHERE audiobook_path = ?''', (str(audiobook_path),))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0.0


def get_audio_files(directory: str) -> List[Path]:
    """Get all audio files from a directory.
    
    Args:
        directory: Path to the directory to scan
        
    Returns:
        List of Path objects for audio files
    """
    audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac'}
    audio_files = []
    
    dir_path = Path(directory)
    if not dir_path.exists():
        return audio_files
    
    for file_path in dir_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
            audio_files.append(file_path)
    
    return sorted(audio_files)


def validate_audio_file(file_path: str) -> bool:
    """Validate if a file is a supported audio file.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if the file is a valid audio file, False otherwise
    """
    audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac'}
    
    path = Path(file_path)
    if not path.exists():
        return False
    
    return path.suffix.lower() in audio_extensions


def get_file_info(file_path: str) -> Dict[str, any]:
    """Get information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary containing file information
    """
    path = Path(file_path)
    
    if not path.exists():
        return {}
    
    stat = path.stat()
    
    return {
        'name': path.name,
        'stem': path.stem,
        'suffix': path.suffix.lower(),
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'modified': stat.st_mtime,
        'exists': True
    }


def copy_audio_file(source_path: str, dest_directory: str) -> Optional[str]:
    """Copy an audio file to the destination directory.
    
    Args:
        source_path: Path to the source audio file
        dest_directory: Destination directory
        
    Returns:
        Path to the copied file, or None if failed
    """
    try:
        source = Path(source_path)
        dest_dir = Path(dest_directory)
        
        if not source.exists():
            return None
        
        # Create destination directory if it doesn't exist
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        dest_path = dest_dir / source.name
        shutil.copy2(source, dest_path)
        
        return str(dest_path)
        
    except Exception as e:
        print(f"Error copying file: {e}")
        return None


def delete_audio_file(file_path: str) -> bool:
    """Delete an audio file.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        True if deletion was successful, False otherwise
    """
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def ensure_directory_exists(directory: str) -> bool:
    """Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")
        return False


def get_directory_size(directory: str) -> int:
    """Get the total size of all files in a directory.
    
    Args:
        directory: Path to the directory
        
    Returns:
        Total size in bytes
    """
    total_size = 0
    dir_path = Path(directory)
    
    if not dir_path.exists():
        return 0
    
    for file_path in dir_path.rglob("*"):
        if file_path.is_file():
            total_size += file_path.stat().st_size
    
    return total_size


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB" 