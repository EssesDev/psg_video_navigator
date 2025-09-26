import pytest
from unittest.mock import Mock, patch
import cv2
import numpy as np
from models.video_model import VideoModel


@pytest.fixture
def video_model():
    """Fixture to initialize VideoModel."""
    return VideoModel()


@patch("cv2.VideoCapture")
def test_load_video_success(mock_capture, video_model):
    """Test successful video loading."""
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.side_effect = [25.0, 100]  # FPS, frame_count
    mock_capture.return_value = mock_cap
    video_model.load_video("test.mp4")
    assert video_model.cap == mock_cap
    assert video_model.duration == 4.0  # 100 / 25 = 4 seconds
    assert video_model.current_time == 0
    mock_cap.set.assert_called_with(cv2.CAP_PROP_POS_FRAMES, 0)


@patch("cv2.VideoCapture")
def test_load_video_file_not_found(mock_capture, video_model):
    """Test loading a non-existent video file."""
    mock_capture.side_effect = FileNotFoundError("Video file not found")
    with pytest.raises(FileNotFoundError, match="Video file not found"):
        video_model.load_video("nonexistent.mp4")


@patch("cv2.VideoCapture")
def test_load_video_invalid(mock_capture, video_model):
    """Test loading an invalid video file."""
    mock_cap = Mock()
    mock_cap.isOpened.return_value = False
    mock_capture.return_value = mock_cap
    with pytest.raises(ValueError, match="Could not open video"):
        video_model.load_video("invalid.mp4")


@patch("cv2.VideoCapture")
def test_set_time_valid(mock_capture, video_model):
    """Test setting valid time within video duration."""
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.return_value = 25.0  # FPS
    mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
    video_model.cap = mock_cap
    video_model.duration = 4.0
    video_model.set_time(2.0)
    assert video_model.current_time == 2.0
    mock_cap.set.assert_called_with(cv2.CAP_PROP_POS_FRAMES, 50)  # 2 * 25


@patch("cv2.VideoCapture")
def test_set_time_clamp(mock_capture, video_model):
    """Test time clamping to 0 or duration."""
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.return_value = 25.0  # FPS
    mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
    video_model.cap = mock_cap
    video_model.duration = 4.0
    video_model.set_time(10.0)  # Beyond duration
    assert video_model.current_time == 4.0
    video_model.set_time(-1.0)  # Below 0
    assert video_model.current_time == 0


def test_get_current_slice(video_model):
    """Test getting current slice number."""
    video_model.duration = 90.0  # 90 seconds
    video_model.current_time = 45.0
    video_model.slice_duration = 30.0
    assert video_model.get_current_slice() == 2  # 45 / 30 + 1


def test_get_total_slices(video_model):
    """Test getting total number of slices."""
    video_model.duration = 90.0  # 90 seconds
    video_model.slice_duration = 30.0
    assert video_model.get_total_slices() == 3  # ceil(90 / 30)


@patch("cv2.VideoCapture")
def test_set_slice(mock_capture, video_model):
    """Test setting video to a specific slice."""
    mock_cap = Mock()
    mock_cap.isOpened.return_value = True
    mock_cap.get.return_value = 25.0  # FPS
    mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
    video_model.cap = mock_cap
    video_model.duration = 4.0
    video_model.slice_duration = 1.0
    video_model.set_slice(2)
    assert video_model.current_time == 1.0  # (2-1) * 1.0
    