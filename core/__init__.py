"""
Core package for the Audiobook Reader application.
Contains the main business logic and audio processing components.
"""

from .audio_player import AudioPlayer
from .audiobook import Audiobook

__all__ = ['AudioPlayer', 'Audiobook'] 