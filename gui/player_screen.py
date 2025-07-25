"""
Player screen for controlling audiobook playback (lightweight version with python-vlc).
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from pathlib import Path
from core.audio_player import AudioPlayer
from utils.file_utils import save_position, get_position

class PlayerScreen:
    """Screen for playing and controlling audiobook playback (lightweight with python-vlc)."""
    def __init__(self, root, app, audiobook_path):
        self.root = root
        self.app = app
        self.audiobook_path = Path(audiobook_path)
        self.frame = None
        self.audio_player = AudioPlayer()
        
        # UI state
        self.is_playing = False
        self.update_thread = None
        self.stop_update = False
        
        self.create_widgets()
        self.load_audiobook()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ttk.Label(
            self.frame,
            text="",
            font=("Arial", 40, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 10))

        # Main content frame
        content_frame = ttk.Frame(self.frame)
        content_frame.grid(row=2, column=0, sticky="nsew")
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Progress frame
        progress_frame = ttk.Frame(content_frame)
        progress_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        progress_frame.grid_columnconfigure(0, weight=1)
        # Time labels
        time_frame = ttk.Frame(progress_frame)
        time_frame.grid(row=0, column=0, sticky="ew")
        time_frame.grid_columnconfigure(1, weight=1)

        # Progress bar style for bigger height
        style = ttk.Style()
        style.configure("Big.Horizontal.TScale",
                        troughcolor="white",
                        sliderthickness=60,  # Aumentei para garantir que fique maior
                        thickness=40,
                        sliderlength=80,
                        length=100,
                        background="black",  # Cor de fundo base do slider
                        foreground="black")  # Cor de primeiro plano do slider (pode ser redundante com background em alguns temas)

        # Garante que a cor azul se mantém em outros estados (pode ser necessário dependendo do tema)
        style.map("Big.Horizontal.TScale",
                  background=[("active", "black"), ("!disabled", "black")],
                  foreground=[("active", "black"), ("!disabled", "black")])
        style.configure("Big.TButton", font=("Arial", 40, "bold"), background="white", foreground="black")

        # Time labels
        self.current_time_label = ttk.Label(time_frame, text="00:00", font=("Arial", 40, "bold"))
        self.current_time_label.grid(row=0, column=0, padx=(0, 10))
        self.total_time_label = ttk.Label(time_frame, text="00:00", font=("Arial", 40, "bold"))
        self.total_time_label.grid(row=0, column=2, padx=(10, 0))
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(
            progress_frame,
            from_=20, to=80,
            orient="horizontal",
            variable=self.progress_var,
            command=self.on_progress_change,
            style="Big.Horizontal.TScale"
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(5, 0))

        # Controls frame
        controls_frame = ttk.Frame(content_frame)
        controls_frame.grid(row=1, column=0, sticky="nsew", pady=(20, 0))
        controls_frame.grid_columnconfigure(0, weight=1)

        # Centered buttons frame
        centered_buttons_frame = ttk.Frame(controls_frame)
        centered_buttons_frame.grid(row=0, column=0, pady=(0, 10))
        for i in range(5):
            centered_buttons_frame.grid_columnconfigure(i, weight=1)

        # Previous button (skip back 30s)
        self.prev_button = ttk.Button(
            centered_buttons_frame,
            text=" Voltar 30s",
            command=self.skip_backward,
            style="Big.TButton"
        )
        self.prev_button.grid(row=0, column=0, padx=(10, 10))

        # Play/Pause button
        self.play_button = ttk.Button(
            centered_buttons_frame,
            text="OUVIR",
            command=self.toggle_play_pause,
            style="Big.TButton"
        )
        self.play_button.grid(row=0, column=1, padx=(10, 10))

        # Next button (skip forward 30s)
        self.next_button = ttk.Button(
            centered_buttons_frame,
            text="Avançar 30s",
            command=self.skip_forward,
            style="Big.TButton"
        )
        self.next_button.grid(row=0, column=2, padx=(10, 10))

        # Back to library button
        back_button = ttk.Button(
            controls_frame,
            text="VOLTAR PARA BIBLIOTECA",
            command=self.app.go_back_to_library,
            style="Big.TButton"
        )
        back_button.grid(row=1, column=0, pady=(20, 0))

        # Stop button (placed below back button)
        self.stop_button = ttk.Button(
            controls_frame,
            text="REINICIAR",
            command=self.stop_audio,
            style="Big.TButton"
        )
        self.stop_button.grid(row=2, column=0, pady=(200, 0))

    def load_audiobook(self):
        try:
            self.audio_player.load_file(str(self.audiobook_path))
            # Restore last position if available
            self.last_position = get_position(str(self.audiobook_path))
            title = self.audiobook_path.stem
            self.title_label.config(text=title)
            self.start_progress_update()
            # If there is a last position, auto-play and seek
            print("Last position: ", self.last_position)
            if self.last_position > 0:
                self.audio_player.play()
                self.is_playing = True
                self.root.after(500, lambda: [
                    self.audio_player.set_position(self.last_position),
                    self.audio_player.pause(),
                    setattr(self, 'is_playing', False),
                    self.play_button.config(text="OUVIR")
                ])
        except Exception as e:
            self.title_label.config(text="Error loading audiobook")


    def toggle_play_pause(self):
        if self.is_playing:
            self.pause_audio()
        else:
            self.play_audio()

    def play_audio(self):
        print("Last position: ", getattr(self, 'last_position', None))
        try:
            self.audio_player.play()
            self.is_playing = True
            self.play_button.config(text="PAUSAR")
        except Exception as e:
            print(f"Error playing audio: {e}")

    def pause_audio(self):
        try:
            self.audio_player.pause()
            self.is_playing = False
            self.play_button.config(text="OUVIR")
        except Exception as e:
            print(f"Error pausing audio: {e}")

    def stop_audio(self):
        try:
            self.audio_player.stop()
            self.is_playing = False
            self.play_button.config(text="OUVIR")
            self.progress_var.set(0)
        except Exception as e:
            print(f"Error stopping audio: {e}")

    def skip_forward(self):
        try:
            current_pos = self.audio_player.get_position()
            duration = self.audio_player.get_duration()
            if current_pos + 30 >= duration:
                new_pos = max(duration - 1, 0)
            else:
                new_pos = current_pos + 30
            self.audio_player.set_position(new_pos)
        except Exception as e:
            print(f"Error skipping forward: {e}")

    def skip_backward(self):
        try:
            current_pos = self.audio_player.get_position()
            new_pos = max(current_pos - 30, 0)
            self.audio_player.set_position(new_pos)
        except Exception as e:
            print(f"Error skipping backward: {e}")

    def on_progress_change(self, value):
        try:
            if self.audio_player.is_file_loaded():
                duration = self.audio_player.get_duration()
                new_position = (float(value) / 100) * duration
                self.audio_player.set_position(new_position)
        except Exception as e:
            print(f"Error changing progress: {e}")

    def on_volume_change(self, value):
        try:
            volume = int(float(value))
            self.audio_player.set_volume(volume)
            self.volume_label.config(text=f"{volume}%")
        except Exception as e:
            print(f"Error changing volume: {e}")

    def start_progress_update(self):
        self.stop_update = False
        self.update_thread = threading.Thread(target=self.update_progress, daemon=True)
        self.update_thread.start()

    def update_progress(self):
        while not self.stop_update:
            try:
                if self.audio_player.is_file_loaded():
                    current_pos = self.audio_player.get_position()
                    duration = self.audio_player.get_duration()
                    
                    if duration > 0:
                        progress = (current_pos / duration) * 100
                        self.root.after(0, self.update_progress_ui, current_pos, duration, progress)
                    
                    if self.is_playing and current_pos >= duration:
                        self.root.after(0, self.on_audio_finished)
                
                time.sleep(0.5)  # Update every 500ms (less frequent for better performance)
                
            except Exception as e:
                print(f"Error updating progress: {e}")
                time.sleep(1)

    def update_progress_ui(self, current_pos, duration, progress):
        try:
            self.progress_var.set(progress)
            current_time = self.format_time(current_pos)
            total_time = self.format_time(duration)
            self.current_time_label.config(text=current_time)
            self.total_time_label.config(text=total_time)
        except Exception as e:
            print(f"Error updating progress UI: {e}")

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:2}:{seconds:2}"

    def on_audio_finished(self):
        self.is_playing = False
        self.play_button.config(text="OUVIR")

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()
        self.stop_update = True
        if self.update_thread:
            self.update_thread.join(timeout=1)
        # Save current position to database
        if self.audio_player.is_file_loaded():
            pos = self.audio_player.get_position()
            save_position(str(self.audiobook_path), pos)
        self.audio_player.stop() 