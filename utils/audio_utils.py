"""
Audio utility functions for the Audiobook Reader application.
"""

from pathlib import Path
from typing import Optional


def format_duration(seconds: float) -> str:
    """Format duration in seconds to HH:MM:SS or MM:SS format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds <= 0:
        return "00:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


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


def get_audio_duration(file_path: str) -> Optional[float]:
    """Get the duration of an audio file in seconds.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Duration in seconds, or None if unable to determine
    """
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # Convert from milliseconds to seconds
    except ImportError:
        # Fallback if pydub is not available
        return None
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return None


def estimate_audio_duration(file_path: str, bitrate: int = 128) -> Optional[float]:
    """Estimate audio duration based on file size and bitrate.
    
    Args:
        file_path: Path to the audio file
        bitrate: Estimated bitrate in kbps
        
    Returns:
        Estimated duration in seconds, or None if unable to estimate
    """
    try:
        file_size = Path(file_path).stat().st_size
        # Duration = (file_size * 8) / (bitrate * 1000)
        duration = (file_size * 8) / (bitrate * 1000)
        return duration
    except Exception as e:
        print(f"Error estimating audio duration: {e}")
        return None


def get_audio_info(file_path: str) -> dict:
    """Get comprehensive information about an audio file.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Dictionary containing audio file information
    """
    info = {
        'file_path': str(file_path),
        'exists': False,
        'size': 0,
        'size_formatted': '0 B',
        'duration': 0,
        'duration_formatted': '00:00',
        'format': 'unknown'
    }
    
    try:
        path = Path(file_path)
        if not path.exists():
            return info
        
        # Basic file info
        stat = path.stat()
        info['exists'] = True
        info['size'] = stat.st_size
        info['size_formatted'] = format_file_size(stat.st_size)
        info['format'] = path.suffix.lower()
        
        # Get duration
        duration = get_audio_duration(file_path)
        if duration is None:
            # Try to estimate duration
            duration = estimate_audio_duration(file_path)
        
        if duration is not None:
            info['duration'] = duration
            info['duration_formatted'] = format_duration(duration)
        
    except Exception as e:
        print(f"Error getting audio info: {e}")
    
    return info


def is_supported_audio_format(file_path: str) -> bool:
    """Check if a file is a supported audio format.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a supported audio format
    """
    supported_formats = {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac'}
    return Path(file_path).suffix.lower() in supported_formats


def get_supported_formats() -> set:
    """Get the set of supported audio formats.
    
    Returns:
        Set of supported audio file extensions
    """
    return {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac'}


def format_bitrate(bitrate: int) -> str:
    """Format bitrate in human-readable format.
    
    Args:
        bitrate: Bitrate in kbps
        
    Returns:
        Formatted bitrate string
    """
    if bitrate >= 1000:
        return f"{bitrate/1000:.1f} Mbps"
    else:
        return f"{bitrate} kbps"


def calculate_playback_time(current_position: float, total_duration: float) -> str:
    """Calculate and format playback time information.
    
    Args:
        current_position: Current position in seconds
        total_duration: Total duration in seconds
        
    Returns:
        Formatted playback time string
    """
    if total_duration <= 0:
        return "00:00 / 00:00"
    
    current_formatted = format_duration(current_position)
    total_formatted = format_duration(total_duration)
    
    return f"{current_formatted} / {total_formatted}"


def calculate_progress_percentage(current_position: float, total_duration: float) -> float:
    """Calculate playback progress as a percentage.
    
    Args:
        current_position: Current position in seconds
        total_duration: Total duration in seconds
        
    Returns:
        Progress percentage (0.0 to 100.0)
    """
    if total_duration <= 0:
        return 0.0
    
    progress = (current_position / total_duration) * 100
    return max(0.0, min(100.0, progress)) 