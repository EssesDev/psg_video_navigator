"""Module for handling video loading and navigation in PSG Video Navigator.

This module contains the VideoModel class, responsible for video operations using
OpenCV, following the Single Responsibility Principle.
"""

import cv2
import math


class VideoModel:
    """Manages video loading and navigation operations.

    Attributes:
        cap (cv2.VideoCapture): OpenCV video capture object.
        duration (float): Video duration in seconds.
        current_time (float): Current time position in the video (seconds).
        slice_duration (float): Duration of each slice (seconds, default 30).
    """

    def __init__(self):
        """Initialize VideoModel with no video loaded."""
        self.cap = None
        self.duration = 0.0
        self.current_time = 0.0
        self.slice_duration = 30.0  # Default slice duration

    def load_video(self, file_path: str) -> None:
        """Load a video file using OpenCV.

        Args:
            file_path (str): Path to the video file (AVI or MP4).

        Raises:
            FileNotFoundError: If the video file does not exist.
            ValueError: If the video file cannot be opened.
        """
        if not file_path:
            raise FileNotFoundError("No video file selected")
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            raise ValueError("Could not open video")
        # Get video duration
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = frame_count / fps if fps > 0 else 0.0
        self.current_time = 0.0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def set_time(self, time: float) -> None:
        """Set the current time in the video.

        Args:
            time (float): Desired time in seconds.
        """
        if self.cap is None or not self.cap.isOpened():
            return
        # Clamp time between 0 and duration
        time = max(0.0, min(time, self.duration))
        self.current_time = time
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame = int(time * fps)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame)

    def get_frame(self) -> any:
        """Get the current video frame.

        Returns:
            numpy.ndarray: Current frame in RGB format, or None if no video is loaded.
        """
        if self.cap is None or not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        if ret:
            # Convert BGR to RGB for Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame_rgb
        return None

    def get_current_slice(self) -> int:
        """Get the current slice number (1-based).

        Returns:
            int: Current slice number based on slice_duration.
        """
        if self.duration == 0:
            return 1
        return math.floor(self.current_time / self.slice_duration) + 1

    def get_total_slices(self) -> int:
        """Get the total number of slices in the video.

        Returns:
            int: Total number of slices based on slice_duration.
        """
        if self.duration == 0:
            return 1
        return math.ceil(self.duration / self.slice_duration)

    def set_slice(self, slice_num: int) -> None:
        """Set the video to the start of a specific slice.

        Args:
            slice_num (int): Slice number (1-based).
        """
        if self.cap is None:
            return
        # Clamp slice number between 1 and total slices
        slice_num = max(1, min(slice_num, self.get_total_slices()))
        # Set time to start of the slice
        self.set_time((slice_num - 1) * self.slice_duration)
