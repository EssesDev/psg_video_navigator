"""Module for controlling interactions in PSG Video Navigator.

This module contains the AppController class, which connects the video and click
models with the Tkinter view, following the MVC pattern and Dependency Inversion.
"""

from tkinter import filedialog, messagebox
from models.video_model import VideoModel
from models.click_model import ClickConfig
import pyautogui


class AppController:
    """Coordinates interactions between models and view in PSG Video Navigator.

    Attributes:
        model_video (VideoModel): Manages video data and navigation.
        model_click (ClickConfig): Manages click configurations.
        view (AppView): Tkinter-based user interface.
    """

    def __init__(self, model_video: VideoModel, model_click: ClickConfig, view: any) -> None:
        """Initialize the controller with models and view.

        Args:
            model_video (VideoModel): Video model instance.
            model_click (ClickConfig): Click configuration model instance.
            view (AppView): Tkinter view instance.
        """
        self.model_video = model_video
        self.model_click = model_click
        self.view = view

    def simulate_click(self, key: str) -> None:
        """Simulate a mouse click at the configured coordinates for an action without moving the cursor permanently.

        Args:
            key (str): Action identifier (e.g., 'click1', 'forward').
        """
        x, y = self.model_click.get_position(key)
        # Save current mouse position
        current_x, current_y = pyautogui.position()
        # Move to target, click, and restore position quickly
        pyautogui.moveTo(x, y, duration=0)
        pyautogui.click()
        pyautogui.moveTo(current_x, current_y, duration=0)

    def set_click_position(self, key: str, x: int, y: int) -> None:
        """Set the (x, y) coordinates for a specific action and show confirmation.

        Args:
            key (str): Action identifier.
            x (int): X-coordinate for the click.
            y (int): Y-coordinate for the click.
        """
        self.model_click.set_position(key, x, y)
        messagebox.showinfo("Config", f"Position for {key} set to ({x}, {y})")

    def reset_clicks(self) -> None:
        """Reset click positions to defaults."""
        self.model_click.reset_positions()
        messagebox.showinfo("Reset", "Click positions reset to defaults")

    def load_video(self) -> None:
        """Open a file dialog to load a video and update the view.

        Displays an error message if the video cannot be loaded.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.avi *.mp4")])
        if file_path:
            try:
                self.model_video.load_video(file_path)
                self.update_view()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def navigate(self, action: str) -> None:
        """Navigate the video based on the action and trigger associated click.

        Args:
            action (str): Navigation action ('forward', 'backward', 'start', 'end').
        """
        if self.model_video.cap is None:
            return
        if action == "forward":
            self.model_video.set_time(self.model_video.current_time + 30)  # 30 seconds
        elif action == "backward":
            self.model_video.set_time(self.model_video.current_time - 30)
        elif action == "start":
            self.model_video.set_time(0)
        elif action == "end":
            self.model_video.set_time(self.model_video.duration)
        self.update_view()
        self.simulate_click(action)

    def update_view(self) -> None:
        """Update the view with the current video frame and slice info."""
        frame = self.model_video.get_frame()
        self.view.update_video_display(frame)
        self.view.update_slice_display()

    def go_to_slice(self, slice_str: str) -> None:
        """Navigate to a specific slice based on user input.

        Args:
            slice_str (str): Slice number as string from UI input.
        """
        try:
            slice_num = int(slice_str)
            self.model_video.set_slice(slice_num)
            self.update_view()
        except ValueError:
            messagebox.showerror("Error", "Invalid slice number")
            