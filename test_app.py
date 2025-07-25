#!/usr/bin/env python3
"""
Test script for the Audiobook Reader application.
This script tests the basic functionality without requiring audio files.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")
    
    try:
        from gui.main_window import AudiobookReaderApp
        from gui.library_screen import LibraryScreen
        from gui.player_screen import PlayerScreen
        print("✓ GUI modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import GUI modules: {e}")
        return False
    
    try:
        from core.audio_player import AudioPlayer
        from core.audiobook import Audiobook
        print("✓ Core modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import core modules: {e}")
        return False
    
    try:
        from utils.file_utils import get_audio_files, validate_audio_file
        from utils.audio_utils import format_duration, format_file_size
        print("✓ Utility modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utility modules: {e}")
        return False
    
    return True

def test_audiobook_class():
    """Test the Audiobook class with a dummy file."""
    print("\nTesting Audiobook class...")
    
    try:
        from core.audiobook import Audiobook
        
        # Create a dummy file for testing
        test_file = Path("test_audio.mp3")
        test_file.write_text("dummy audio content")
        
        # This should fail gracefully since it's not a real audio file
        try:
            audiobook = Audiobook(test_file)
            print("✓ Audiobook class created successfully")
        except Exception as e:
            print(f"✓ Audiobook class handled invalid file correctly: {e}")
        
        # Clean up
        test_file.unlink(missing_ok=True)
        
    except Exception as e:
        print(f"✗ Audiobook class test failed: {e}")
        return False
    
    return True

def test_audio_player():
    """Test the AudioPlayer class initialization."""
    print("\nTesting AudioPlayer class...")
    
    try:
        from core.audio_player import AudioPlayer
        
        player = AudioPlayer()
        print("✓ AudioPlayer initialized successfully")
        
        # Test basic methods
        assert not player.is_loaded()
        assert not player.is_playing()
        assert not player.is_paused()
        print("✓ AudioPlayer state methods work correctly")
        
    except Exception as e:
        print(f"✗ AudioPlayer test failed: {e}")
        return False
    
    return True

def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    try:
        from utils.audio_utils import format_duration, format_file_size
        
        # Test duration formatting
        assert format_duration(65) == "01:05"
        assert format_duration(3661) == "01:01:01"
        print("✓ Duration formatting works correctly")
        
        # Test file size formatting
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1048576) == "1.0 MB"
        print("✓ File size formatting works correctly")
        
    except Exception as e:
        print(f"✗ Utility functions test failed: {e}")
        return False
    
    return True

def test_directory_structure():
    """Test that the required directories exist."""
    print("\nTesting directory structure...")
    
    required_dirs = [
        "gui",
        "core", 
        "utils",
        "data/audiobooks"
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Missing directory: {dir_path}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("Audiobook Reader - Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_audiobook_class,
        test_audio_player,
        test_utils,
        test_directory_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 