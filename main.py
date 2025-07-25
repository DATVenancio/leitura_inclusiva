#!/usr/bin/env python3
"""
Audiobook Reader - Main Application
A Python application for playing audiobooks using tkinter GUI.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import AudiobookReaderApp

def main():
    """Main function to start the audiobook reader application."""
    root = tk.Tk()
    app = AudiobookReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 