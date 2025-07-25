"""
Main window class for the Audiobook Reader application.
Manages the overall application window and screen transitions.
"""

import tkinter as tk
from tkinter import ttk
from .library_screen import LibraryScreen
from .player_screen import PlayerScreen


class AudiobookReaderApp:
    """Main application class that manages the window and screen transitions."""
    
    def __init__(self, root):
        """Initialize the main application window."""
        self.root = root
        self.root.title("Audiobook Reader")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.update()  # Ensure window is initialized
        try:
            # Windows
            self.root.state('zoomed')
        except tk.TclError:
            try:
                # Linux (many window managers)
                self.root.attributes('-zoomed', True)
            except tk.TclError:
                # Fallback: set to screen size
                self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        
        # Configure the main window
        self.setup_window()
        
        # Initialize screens
        self.current_screen = None
        self.library_screen = None
        self.player_screen = None
        
        # Start with the library screen
        self.show_library_screen()
    
    def setup_window(self):
        """Configure the main window appearance and behavior."""
        # Set window icon (if available)
        try:
            self.root.iconbitmap('data/icon.ico')
        except:
            pass
        
        # Configure grid weight for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme for better appearance
    
    def show_library_screen(self):
        """Show the audiobook library selection screen."""
        # Hide current screen if exists
        if self.current_screen:
            self.current_screen.hide()
        
        # Create and show library screen
        self.library_screen = LibraryScreen(self.root, self)
        self.current_screen = self.library_screen
        self.library_screen.show()
    
    def show_player_screen(self, audiobook_path):
        """Show the audio player screen for the selected audiobook."""
        # Hide current screen if exists
        if self.current_screen:
            self.current_screen.hide()
        
        # Create and show player screen
        self.player_screen = PlayerScreen(self.root, self, audiobook_path)
        self.current_screen = self.player_screen
        self.player_screen.show()
    
    def go_back_to_library(self):
        """Return to the library screen from the player screen."""
        if self.current_screen == self.player_screen:
            self.show_library_screen()
    
    def quit_app(self):
        """Safely quit the application."""
        # Stop any playing audio
        if self.player_screen:
            self.player_screen.stop_audio()
        
        self.root.quit() 