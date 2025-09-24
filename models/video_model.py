"""Module for handling video data and navigation in PSG Video Navigator.

This module contains the VideoModel class, responsible for loading and navigating
video files (AVI/MP4) using OpenCV, following the Single Responsibility Principle.
"""

import cv2
import os
import math


class VideoModel:
    """Manages video loading and frame navigation for PSG Video Navigator.

    Attributes:
        cap (cv2.VideoCapture): VideoCapture object for the loaded video.
        duration (float): Total duration of the video in seconds.
        current_time (float): Current position in the video in seconds.
        frame (numpy.ndarray): Current video frame as a numpy array (RGB).
        slice_duration (float): Duration of each slice in seconds (default: 30).
    """

    def __init__(self):
        """Initialize an empty VideoModel instance."""
        self.cap = None
        self.duration = 0
        self.current_time = 0
        self.frame = None
        self.slice_duration = 30  # Duration of each slice in seconds

    def load_video(self, file_path: str) -> None:
        """Load a video file and initialize its properties.

        Args:
            file_path (str): Path to the video file (AVI or MP4).

        Raises:
            FileNotFoundError: If the video file does not exist.
            ValueError: If the video file cannot be opened.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("Video file not found")
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            raise ValueError("Could not open video")
        # Calculate duration in seconds
        self.duration = self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.cap.get(cv2.CAP_PROP_FPS)
        self.set_time(0)  # Start at beginning

    def set_time(self, time_sec: float) -> None:
        """Set the video to a specific time and update the current frame.

        Args:
            time_sec (float): Target time in seconds.

        Returns:
            None: If no video is loaded or time is invalid.
        """
        if self.cap is None:
            return
        # Clamp time between 0 and duration
        self.current_time = max(0, min(time_sec, self.duration))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(self.current_time * fps))
        ret, frame = self.cap.read()
        if ret:
            # Convert BGR to RGB for display
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def get_frame(self) -> any:
        """Get the current video frame.

        Returns:
            numpy.ndarray or None: Current frame in RGB format, or None if not available.
        """
        return self.frame

    def get_current_slice(self) -> int:
        """Get the current slice number (1-based).

        Returns:
            int: Current slice number.
        """
        if self.duration == 0:
            return 1
        return math.floor(self.current_time / self.slice_duration) + 1

    def get_total_slices(self) -> int:
        """Get the total number of slices in the video.

        Returns:
            int: Total slices.
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
        time_sec = (slice_num - 1) * self.slice_duration
        self.set_time(time_sec)
        