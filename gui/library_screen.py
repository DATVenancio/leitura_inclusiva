"""
Library screen for browsing and selecting audiobooks.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path
from core.audiobook import Audiobook


class LibraryScreen:
    """Screen for displaying and selecting audiobooks from the library."""
    
    def __init__(self, root, app):
        """Initialize the library screen."""
        self.root = root
        self.app = app
        self.frame = None
        self.audiobooks = []
        self.selected_audiobook = None
        
        # Create the main frame
        self.create_widgets()
    
    def create_widgets(self):
        """Create and configure all widgets for the library screen."""
        # Main frame
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure grid weights
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            self.frame, 
            text="LIVROS DISPONÍVEIS", 
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create main content frame
        content_frame = ttk.Frame(self.frame)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Audiobooks listbox with scrollbar
        list_frame = ttk.Frame(content_frame)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Listbox for audiobooks
        self.audiobooks_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 50, "bold"),
            selectmode=tk.SINGLE,
            activestyle='none'
        )
        self.audiobooks_listbox.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.audiobooks_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.audiobooks_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event
        self.audiobooks_listbox.bind('<<ListboxSelect>>', self.on_audiobook_select)
        
        # Buttons frame
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.grid(row=0, column=1, sticky="n", padx=(10, 0))
        
        # Play button
        self.play_button = ttk.Button(
            buttons_frame,
            text="OUVIR",
            command=self.play_selected_audiobook,
            state="disabled",
            style="Big.TButton"
        )
        self.play_button.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        # Quit button
        quit_button = ttk.Button(
            buttons_frame,
            text="SAIR",
            command=self.app.quit_app,
            style="Big.TButton"
        )
        quit_button.grid(row=3, column=0, sticky="ew")

        # Style for even bigger buttons
        style = ttk.Style()
        style.configure("Big.TButton", font=("Arial", 40, "bold"), background="white", foreground="black")
        # Load audiobooks
        self.load_audiobooks()
    
    def load_audiobooks(self):
        """Load audiobooks from the data directory."""
        self.audiobooks = []
        self.audiobooks_listbox.delete(0, tk.END)
        
        audiobooks_dir = Path("data/audiobooks")
        if not audiobooks_dir.exists():
            audiobooks_dir.mkdir(parents=True, exist_ok=True)
            return
        
        # Scan for audio files
        audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a'}
        
        for file_path in audiobooks_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
                try:
                    audiobook = Audiobook(file_path)
                    self.audiobooks.append(audiobook)
                    self.audiobooks_listbox.insert(tk.END, audiobook.title)
                except Exception as e:
                    print(f"Error loading audiobook {file_path}: {e}")
        
        if not self.audiobooks:
            self.audiobooks_listbox.insert(tk.END, "No audiobooks found")
            self.audiobooks_listbox.itemconfig(0, fg="gray")
    
    def on_audiobook_select(self, event):
        """Handle audiobook selection from listbox."""
        selection = self.audiobooks_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.audiobooks):
                self.selected_audiobook = self.audiobooks[index]
                self.play_button.config(state="normal")
    
    def play_selected_audiobook(self):
        """Play the selected audiobook."""
        if self.selected_audiobook:
            self.app.show_player_screen(self.selected_audiobook.file_path)
    
    def refresh_library(self):
        """Refresh the audiobook library."""
        self.load_audiobooks()
        self.selected_audiobook = None
        self.play_button.config(state="disabled")
    
    def add_audiobook(self):
        """Add a new audiobook to the library."""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select Audiobook File",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.ogg *.flac *.m4a"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Copy file to audiobooks directory
                import shutil
                audiobooks_dir = Path("data/audiobooks")
                audiobooks_dir.mkdir(parents=True, exist_ok=True)
                
                dest_path = audiobooks_dir / Path(file_path).name
                shutil.copy2(file_path, dest_path)
                
                # Refresh library
                self.refresh_library()
                messagebox.showinfo("Success", "Audiobook added successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add audiobook: {e}")
    
    def show(self):
        """Show the library screen."""
        self.frame.grid()
        self.refresh_library()
    
    def hide(self):
        """Hide the library screen."""
        self.frame.grid_remove() 