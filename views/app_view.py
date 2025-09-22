"""Module for the Tkinter-based user interface in PSG Video Navigator.

This module contains the AppView class, responsible for rendering the UI and
handling user inputs, following the Single Responsibility Principle.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class AppView(tk.Tk):
    """Tkinter-based user interface for PSG Video Navigator.

    Attributes:
        controller (AppController): Controller instance for handling user actions.
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

        # Create menu bar
        self.create_menu_bar()

        # Buttons for simple clicks
        tk.Button(self, text="Simulate Click 1", command=lambda: self.controller.simulate_click("click1")).pack(pady=5)
        tk.Button(self, text="Simulate Click 2", command=lambda: self.controller.simulate_click("click2")).pack(pady=5)

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

    def create_menu_bar(self) -> None:
        """Create the menu bar with File, Settings, and Help menus."""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Video", command=self.controller.load_video)
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
            