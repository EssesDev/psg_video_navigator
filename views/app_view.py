"""Module for the Tkinter-based user interface in PSG Video Navigator.

This module contains the AppView class, responsible for rendering the UI and
handling user inputs, following the Single Responsibility Principle.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import pyautogui
import time


class AppView(tk.Tk):
    """Tkinter-based user interface for PSG Video Navigator.

    Attributes:
        controller (AppController): Controller instance for handling user actions.
        video_frame (tk.Frame): Frame containing the video label with borders.
        video_label (tk.Label): Label for displaying video frames.
        entries (dict): Dictionary of (x, y) entry widgets for click configurations.
        original_frame (PIL.Image): Original video frame for resizing.
        slice_label (tk.Label): Label for displaying current slice number.
        slice_entry (tk.Entry): Entry for entering slice number.
    """

    def __init__(self, controller: any) -> None:
        """Initialize the Tkinter window and UI components.

        Args:
            controller (AppController): Controller to handle UI events.
        """
        super().__init__()
        self.title("PSG Video Navigator")
        self.geometry("800x600")
        self.minsize(500, 400)  # Increased minimum window size
        self.controller = controller
        self.attributes('-topmost', True)  # Keep window always on top

        # Create menu bar
        self.create_menu_bar()

        # Use grid layout for better control
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Video frame expands in row 1

        # Buttons for custom clicks and lock
        click_frame = tk.Frame(self)
        click_frame.grid(row=0, column=0, sticky="ew", pady=5)
        tk.Button(click_frame, text="Lock/Unlock", command=lambda: self.controller.simulate_click("lock"), font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(click_frame, text="1", command=lambda: self.controller.simulate_click("click1"), font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(click_frame, text="2", command=lambda: self.controller.simulate_click("click2"), font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(click_frame, text="3", command=lambda: self.controller.simulate_click("click3"), font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(click_frame, text="R", command=lambda: self.controller.simulate_click("rem"), font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(click_frame, text="Load Video", command=lambda: self.controller.load_video(), font=("Arial", 12)).pack(side=tk.RIGHT, padx=5)

        # Frame for video with borders
        self.video_frame = tk.Frame(self, borderwidth=2, relief="ridge")
        self.video_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Label inside the video frame
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(expand=True, fill=tk.BOTH)

        # Bind resize event to update video display
        self.bind("<Configure>", self.resize_image)

        # Navigation buttons with slice indicator
        nav_frame = tk.Frame(self)
        nav_frame.grid(row=2, column=0, sticky="ew", pady=10)
        tk.Button(nav_frame, text="Start", command=lambda: self.controller.navigate("start"), font=("Arial", 12)).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="-30s", command=lambda: self.controller.navigate("backward"), font=("Arial", 12)).grid(row=0, column=1, padx=5)

        # Slice indicator frame
        slice_frame = tk.Frame(nav_frame)
        slice_frame.grid(row=0, column=2, padx=5)
        self.slice_label = tk.Label(slice_frame, text="Slice: 1", font=("Arial", 12))
        self.slice_label.pack(side=tk.LEFT)
        self.slice_entry = tk.Entry(slice_frame, width=5, font=("Arial", 12))
        self.slice_entry.pack(side=tk.LEFT)
        tk.Button(slice_frame, text="Go", command=lambda: self.controller.go_to_slice(self.slice_entry.get()), font=("Arial", 12)).pack(side=tk.LEFT)

        tk.Button(nav_frame, text="+30s", command=lambda: self.controller.navigate("forward"), font=("Arial", 12)).grid(row=0, column=3, padx=5)
        tk.Button(nav_frame, text="End", command=lambda: self.controller.navigate("end"), font=("Arial", 12)).grid(row=0, column=4, padx=5)

        # Version label
        version_label = tk.Label(self, text="Version 1.0.0", font=("Arial", 10))
        version_label.grid(row=3, column=0, sticky="se", padx=10, pady=10)

        # Initialize original frame as None
        self.original_frame = None

    def create_menu_bar(self) -> None:
        """Create the menu bar with File, Settings, and Help menus."""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
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
        config_window.geometry("400x500")
        config_window.attributes('-topmost', True)  # Keep config window on top

        # Create input fields and capture buttons for click coordinates
        labels = ["Lock/Unlock", "1", "2", "3", "REM", "Forward", "Backward", "Start", "End"]
        keys = ["lock", "click1", "click2", "click3", "rem", "forward", "backward", "start", "end"]
        self.entries = {}
        for i, (label, key) in enumerate(zip(labels, keys)):
            tk.Label(config_window, text=f"{label} (x, y):").grid(row=i, column=0, padx=5, pady=5)
            x_entry = tk.Entry(config_window, width=5)
            y_entry = tk.Entry(config_window, width=5)
            x_entry.grid(row=i, column=1, padx=5)
            y_entry.grid(row=i, column=2, padx=5)
            tk.Button(config_window, text="Set", command=lambda k=key, xe=x_entry, ye=y_entry: self.set_position_from_entry(k, xe.get(), ye.get())).grid(row=i, column=3, padx=5)
            tk.Button(config_window, text="Capture", command=lambda k=key, xe=x_entry, ye=y_entry: self.capture_position(k, xe, ye)).grid(row=i, column=4, padx=5)
            self.entries[key] = (x_entry, y_entry)

        # Reset button
        tk.Button(config_window, text="Reset", command=self.controller.reset_clicks, font=("Arial", 12)).grid(row=len(labels), column=0, columnspan=5, pady=10)

    def capture_position(self, key: str, x_entry: tk.Entry, y_entry: tk.Entry) -> None:
        """Capture mouse click position after a short delay and set it for the action."""
        messagebox.showinfo("Capture Position", "Click on the screen where you want the click to occur. You have 5 seconds.")
        time.sleep(5)  # Wait for user to click
        x, y = pyautogui.position()
        x_entry.delete(0, tk.END)
        x_entry.insert(0, str(x))
        y_entry.delete(0, tk.END)
        y_entry.insert(0, str(y))
        self.controller.set_click_position(key, x, y)

    def set_position_from_entry(self, key: str, x_str: str, y_str: str) -> None:
        """Set position from manual entry."""
        try:
            x, y = int(x_str), int(y_str)
            self.controller.set_click_position(key, x, y)
        except ValueError:
            messagebox.showerror("Error", "Invalid x,y values")

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

    def update_slice_display(self) -> None:
        """Update the slice label with current slice number."""
        current_slice = self.controller.model_video.get_current_slice()
        self.slice_label.config(text=f"Slice: {current_slice}")
