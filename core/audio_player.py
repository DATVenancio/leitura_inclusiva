"""
Audio player class for handling audiobook playback using python-vlc (lightweight).
"""

import vlc
import threading
import time
from pathlib import Path

class AudioPlayer:
    """Lightweight audio player using python-vlc."""
    def __init__(self):
        self.file_path = None
        self.is_loaded = False
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0
        self.duration = 0        
        # Initialize VLC instance
        self.vlc_instance = vlc.Instance('--no-xlib', '--quiet')
        self.media_player = self.vlc_instance.media_player_new()
        
        # Thread for monitoring playback
        self.monitor_thread = None
        self.stop_monitoring = False
    
    def load_file(self, file_path):
        """Load an audio file for playback."""
        try:
            self.file_path = Path(file_path)
            if not self.file_path.exists():
                raise FileNotFoundError(f"Audio file not found: {file_path}")
            
            # Create media and load it
            media = self.vlc_instance.media_new(str(self.file_path))
            self.media_player.set_media(media)
            
            # Parse media to get duration
            self.duration = self._get_duration(media)
            
            self.is_loaded = True
            self.current_position = 0
            
        except Exception as e:
            self.is_loaded = False
            raise Exception(f"Failed to load audio file: {e}")
    
    def _get_duration(self, media):
        """Get the duration of the loaded audio file, ensuring media is parsed."""
        try:
            # Parse the media (blocking)
            media.parse()
            duration_ms = media.get_duration()
            return duration_ms / 1000 if duration_ms > 0 else 0
        except Exception:
            return 0
    
    def play(self):
        """Start playing the loaded audio file."""
        if not self.is_loaded:
            raise Exception("No audio file loaded")
        
        try:
            self.media_player.play()
            self.is_playing = True
            self.is_paused = False
            
            # Start monitoring thread
            self._start_monitoring()
            
        except Exception as e:
            raise Exception(f"Failed to play audio: {e}")
    
    def pause(self):
        """Pause the currently playing audio."""
        if not self.is_loaded:
            return
        
        try:
            self.media_player.pause()
            self.is_playing = False
            self.is_paused = True
        except Exception as e:
            print(f"Error pausing audio: {e}")
    
    def unpause(self):
        """Resume playing the paused audio."""
        if not self.is_loaded:
            return
        
        try:
            self.media_player.pause()  # VLC pause() toggles pause/play
            self.is_playing = True
            self.is_paused = False
        except Exception as e:
            print(f"Error unpausing audio: {e}")
    
    def stop(self):
        """Stop playing and reset to beginning."""
        if not self.is_loaded:
            return
        
        try:
            self.media_player.stop()
            self.is_playing = False
            self.is_paused = False
            self.current_position = 0
            
            # Stop monitoring
            self._stop_monitoring()
            
        except Exception as e:
            print(f"Error stopping audio: {e}")
    
    def set_position(self, position):
        """Set the playback position in seconds."""
        if not self.is_loaded:
            return
        
        try:
            # Convert seconds to milliseconds
            position_ms = int(position *1000)
            self.media_player.set_time(position_ms)
            self.current_position = position
        except Exception as e:
            print(f"Error setting position: {e}")
    
    def get_position(self):
        """Get the current playback position in seconds."""
        if not self.is_loaded:
            return 0      
        try:
            position_ms = self.media_player.get_time()
            return position_ms / 1000 if position_ms > 0 else 0
        except Exception as e:
            print(f"Error getting position: {e}")
            return 0    
    def get_duration(self):
        """Get the total duration of the audio file in seconds."""
        return self.duration
    
    def set_volume(self, volume):
        """Set the playback volume (0-100)."""
        try:
            volume = max(0, min(100, volume))
            self.media_player.audio_set_volume(volume)
        except Exception as e:
            print(f"Error setting volume: {e}")
    
    def get_volume(self):
        """Get the current volume level."""
        try:
            return self.media_player.audio_get_volume()
        except Exception:
            return 50  
    def is_file_loaded(self):
        """Check if an audio file is loaded."""
        return self.is_loaded
    
    def is_audio_playing(self):
        """Check if audio is currently playing."""
        return self.is_playing
    
    def is_audio_paused(self):
        """Check if audio is currently paused."""
        return self.is_paused
    
    def _start_monitoring(self):
        """Start the monitoring thread for tracking playback position."""
        self.stop_monitoring = False
        self.monitor_thread = threading.Thread(target=self._monitor_playback, daemon=True)
        self.monitor_thread.start()
    
    def _stop_monitoring(self):
        """Stop the monitoring thread."""
        self.stop_monitoring = True
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
    
    def _monitor_playback(self):
        """Monitor playback and update position."""
        while not self.stop_monitoring and self.is_playing:
            try:
                # Update current position
                self.current_position = self.get_position()
                
                # Check if playback has ended
                if self.media_player.get_state() == vlc.State.Ended:
                    self.is_playing = False
                    break
                
                time.sleep(0.1)  # Update every 100ms
                
            except Exception as e:
                print(f"Error monitoring playback: {e}")
                break
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.stop()
            self.media_player.release()
            self.vlc_instance.release()
        except Exception as e:
            print(f"Error during cleanup: {e}")    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup() 