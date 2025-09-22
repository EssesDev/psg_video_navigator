"""Module for the Tkinter-based user interface in PSG Video Navigator.

This module contains the AppView class, responsible for rendering the UI and
handling user inputs, following the Single Responsibility Principle.
"""

import tkinter as tk
from PIL import Image, ImageTk


class AppView(tk.Tk):
    """Tkinter-based user interface for PSG Video Navigator.

    Attributes:
        controller (AppController): Controller instance for handling user actions.
        config_frame (tk.Frame): Frame for click configuration inputs.
        video_label (tk.Label): Label for displaying video frames.
        entries (dict): Dictionary of (x, y) entry widgets for click configurations.
    """

    def __init__(self, controller: any) -> None:
        """Initialize the Tkinter window and UI components.

        Args:
            controller (AppController): Controller to handle UI events.
        """
        super().__init__()
        self.title("PSG Video Navigator")
        self.controller = controller
        self.geometry("800x600")

        # Section for click configuration inputs
        self.config_frame = tk.Frame(self)
        self.config_frame.pack(pady=10)
        self.create_config_entries()

        # Buttons for simple clicks
        tk.Button(self, text="Simulate Click 1", command=lambda: self.controller.simulate_click("click1")).pack(pady=5)
        tk.Button(self, text="Simulate Click 2", command=lambda: self.controller.simulate_click("click2")).pack(pady=5)

        # Button to load video
        tk.Button(self, text="Load Video", command=self.controller.load_video).pack(pady=10)

        # Label for displaying video frames
        self.video_label = tk.Label(self)
        self.video_label.pack()

        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)
        tk.Button(nav_frame, text="Start", command=lambda: self.controller.navigate("start")).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="-30 min", command=lambda: self.controller.navigate("backward")).grid(row=0, column=1, padx=5)
        tk.Button(nav_frame, text="+30 min", command=lambda: self.controller.navigate("forward")).grid(row=0, column=2, padx=5)
        tk.Button(nav_frame, text="End", command=lambda: self.controller.navigate("end")).grid(row=0, column=3, padx=5)

    def create_config_entries(self) -> None:
        """Create input fields for configuring click coordinates."""
        labels = ["Click1", "Click2", "Forward", "Backward", "Start", "End"]
        self.entries = {}
        for i, key in enumerate(["click1", "click2", "forward", "backward", "start", "end"]):
            tk.Label(self.config_frame, text=f"{labels[i]} x,y:").grid(row=i, column=0)
            x_entry = tk.Entry(self.config_frame, width=5)
            y_entry = tk.Entry(self.config_frame, width=5)
            x_entry.grid(row=i, column=1)
            y_entry.grid(row=i, column=2)
            tk.Button(self.config_frame, text="Set", command=lambda k=key, xe=x_entry, ye=y_entry: self.controller.set_click_position(k, xe.get(), ye.get())).grid(row=i, column=3)
            self.entries[key] = (x_entry, y_entry)

    def update_video_display(self, frame: any) -> None:
        """Update the video display with a new frame.

        Args:
            frame (numpy.ndarray): Video frame in RGB format.
        """
        if frame is not None:
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk  # Keep reference to avoid garbage collection
            self.video_label.configure(image=imgtk)
            