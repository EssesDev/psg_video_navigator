"""Module for the Tkinter-based user interface in PSG Video Navigator.

This module contains the AppView class, responsible for rendering the UI and
handling user inputs, following the Single Responsibility Principle.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np


class AppView(tk.Tk):
    """Tkinter-based user interface for PSG Video Navigator.

    Attributes:
        controller (AppController): Controller instance for handling user actions.
        video_frame (tk.Frame): Frame containing the video label with borders.
        video_label (tk.Label): Label for displaying video frames.
        entries (dict): Dictionary of (x, y) entry widgets for click configurations.
        original_frame (PIL.Image): Original video frame for resizing.
    """

    def __init__(self, controller: any) -> None:
        """Initialize the Tkinter window and UI components.

        Args:
            controller (AppController): Controller to handle UI events.
        """
        super().__init__()
        self.title("PSG Video Navigator")
        self.geometry("800x600")
        self.minsize(400, 300)  # Set minimum window size
        self.controller = controller

        # Create menu bar
        self.create_menu_bar()

        # Buttons for simple clicks
        click_frame = tk.Frame(self)
        click_frame.pack(pady=5)
        tk.Button(click_frame, text="Simulate Click 1", command=lambda: self.controller.simulate_click("click1")).pack(side=tk.LEFT, padx=5)
        tk.Button(click_frame, text="Simulate Click 2", command=lambda: self.controller.simulate_click("click2")).pack(side=tk.LEFT, padx=5)

        # Frame for video with borders
        self.video_frame = tk.Frame(self, borderwidth=2, relief="ridge")
        self.video_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Label inside the video frame
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(expand=True, fill=tk.BOTH)

        # Bind resize event to update video display
        self.bind("<Configure>", self.resize_image)

        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)
        tk.Button(nav_frame, text="Start", command=lambda: self.controller.navigate("start")).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="-30 min", command=lambda: self.controller.navigate("backward")).grid(row=0, column=1, padx=5)
        tk.Button(nav_frame, text="+30 min", command=lambda: self.controller.navigate("forward")).grid(row=0, column=2, padx=5)
        tk.Button(nav_frame, text="End", command=lambda: self.controller.navigate("end")).grid(row=0, column=3, padx=5)

        # Initialize original frame as None
        self.original_frame = None

    def create_menu_bar(self) -> None:
        """Create the menu bar with File, Settings, and Help menus."""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        # Use lambda to safely access controller method
        file_menu.add_command(label="Load Video", command=lambda: self.controller.load_video())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Settings menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Configure Clicks", command=self.open_click_config_window)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def open_click_config_window(self) -> None:
        """Open a new window to configure click coordinates."""
        config_window = tk.Toplevel(self)
        config_window.title("Configure Click Positions")
        config_window.geometry("300x400")

        # Create input fields for click coordinates
        labels = ["Click1", "Click2", "Forward", "Backward", "Start", "End"]
        self.entries = {}
        for i, key in enumerate(["click1", "click2", "forward", "backward", "start", "end"]):
            tk.Label(config_window, text=f"{labels[i]} x,y:").grid(row=i, column=0, padx=5, pady=5)
            x_entry = tk.Entry(config_window, width=5)
            y_entry = tk.Entry(config_window, width=5)
            x_entry.grid(row=i, column=1, padx=5)
            y_entry.grid(row=i, column=2, padx=5)
            tk.Button(config_window, text="Set", command=lambda k=key, xe=x_entry, ye=y_entry: self.controller.set_click_position(k, xe.get(), ye.get())).grid(row=i, column=3, padx=5)
            self.entries[key] = (x_entry, y_entry)

    def show_about(self) -> None:
        """Display an About dialog with application information."""
        messagebox.showinfo(
            "About PSG Video Navigator",
            "PSG Video Navigator\nVersion 1.0\nDeveloped by EssesDev\n"
            "A cross-platform tool for navigating videos and simulating mouse clicks.\n"
            "Built with Python, Tkinter, OpenCV, and PyAutoGUI."
        )

    def update_video_display(self, frame: np.ndarray) -> None:
        """Update the video display with a new frame and store the original for resizing.

        Args:
            frame (numpy.ndarray): Video frame in RGB format.
        """
        if frame is not None:
            self.original_frame = Image.fromarray(frame)
            self.resize_image()

    def resize_image(self, event=None) -> None:
        """Resize the video image to fit the current frame size."""
        if self.original_frame is not None:
            # Get current dimensions of the video frame
            width = self.video_frame.winfo_width()
            height = self.video_frame.winfo_height()
            # Ensure dimensions are valid
            if width > 0 and height > 0:
                # Resize the image with high-quality resampling
                resized_img = self.original_frame.resize((width, height), Image.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=resized_img)
                self.video_label.imgtk = imgtk  # Keep reference to avoid garbage collection
                self.video_label.configure(image=imgtk)
                