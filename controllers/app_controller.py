"""Module for controlling interactions in PSG Video Navigator.

This module contains the AppController class, which connects the video and click
models with the Tkinter view, following the MVC pattern and Dependency Inversion.
"""

from tkinter import filedialog, messagebox
from models.video_model import VideoModel
from models.click_model import ClickConfig


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
        """Simulate a mouse click at the configured coordinates for an action.

        Args:
            key (str): Action identifier (e.g., 'click1', 'forward').
        """
        x, y = self.model_click.get_position(key)
        import pyautogui
        pyautogui.click(x, y)

    def set_click_position(self, key: str, x_str: str, y_str: str) -> None:
        """Set click coordinates for an action and show confirmation.

        Args:
            key (str): Action identifier.
            x_str (str): X-coordinate as string from UI input.
            y_str (str): Y-coordinate as string from UI input.

        Raises:
            ValueError: If coordinates cannot be converted to integers.
        """
        try:
            x, y = int(x_str), int(y_str)
            self.model_click.set_position(key, x, y)
            messagebox.showinfo("Config", f"Position for {key} set to ({x}, {y})")
        except ValueError:
            messagebox.showerror("Error", "Invalid x,y values")

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
            self.model_video.set_time(self.model_video.current_time + 1800)  # 30 min
        elif action == "backward":
            self.model_video.set_time(self.model_video.current_time - 1800)
        elif action == "start":
            self.model_video.set_time(0)
        elif action == "end":
            self.model_video.set_time(self.model_video.duration)
        self.update_view()
        self.simulate_click(action)

    def update_view(self) -> None:
        """Update the view with the current video frame."""
        frame = self.model_video.get_frame()
        self.view.update_video_display(frame)
        