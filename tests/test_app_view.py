import pytest
from unittest.mock import Mock, patch
import tkinter as tk
from views.app_view import AppView
import numpy as np
from PIL import Image


@pytest.fixture
def app_view():
    """Fixture to initialize AppView with mocked controller."""
    controller = Mock()
    root = AppView(controller)
    root.update()  # Process pending Tkinter events
    yield root
    root.destroy()  # Clean up after tests


def test_initialization(app_view):
    """Test UI initialization."""
    assert app_view.title() == "PSG Video Navigator"
    assert app_view.minsize() == (500, 400)
    assert app_view.attributes("-topmost") == 1
    assert isinstance(app_view.video_frame, tk.Frame)
    assert isinstance(app_view.video_label, tk.Label)
    assert isinstance(app_view.slice_label, tk.Label)


@patch("tkinter.Toplevel")
def test_open_click_config_window(mock_toplevel, app_view):
    """Test opening click configuration window."""
    mock_window = Mock()
    mock_toplevel.return_value = mock_window
    app_view.open_click_config_window()
    mock_toplevel.assert_called_with(app_view)
    mock_window.title.assert_called_with("Configure Click Positions")
    mock_window.geometry.assert_called_with("400x500")
    assert mock_window.attributes("-topmost") == 1


@patch("tkinter.messagebox.showinfo")
@patch("pyautogui.position")
def test_capture_position(mock_position, mock_showinfo, app_view):
    """Test capturing mouse position."""
    mock_position.return_value = (500, 600)
    mock_entry_x = Mock()
    mock_entry_y = Mock()
    app_view.capture_position("click1", mock_entry_x, mock_entry_y)
    mock_showinfo.assert_called_with("Capture Position", "Click on the screen where you want the click to occur. You have 5 seconds.")
    mock_entry_x.delete.assert_called_with(0, tk.END)
    mock_entry_x.insert.assert_called_with(0, "500")
    mock_entry_y.delete.assert_called_with(0, tk.END)
    mock_entry_y.insert.assert_called_with(0, "600")
    app_view.controller.set_click_position.assert_called_with("click1", 500, 600)


@patch("tkinter.messagebox.showerror")
def test_set_position_from_entry_invalid(mock_showerror, app_view):
    """Test setting position with invalid input."""
    app_view.set_position_from_entry("click1", "invalid", "600")
    mock_showerror.assert_called_with("Error", "Invalid x,y values")
    app_view.controller.set_click_position.assert_not_called()


@patch("PIL.Image.fromarray")
@patch("PIL.ImageTk.PhotoImage")
def test_update_video_display(mock_photoimage, mock_fromarray, app_view):
    """Test updating video display with a frame."""
    mock_image = Mock()
    mock_fromarray.return_value = mock_image
    mock_photo = Mock()
    mock_photoimage.return_value = mock_photo
    app_view.video_frame.winfo_width.return_value = 640
    app_view.video_frame.winfo_height.return_value = 480
    app_view.update_video_display(np.zeros((480, 640, 3), dtype=np.uint8))
    mock_fromarray.assert_called_once()
    mock_image.resize.assert_called_with((640, 480), Image.LANCZOS)
    mock_photoimage.assert_called_with(image=mock_image)
    assert app_view.video_label.imgtk == mock_photo
