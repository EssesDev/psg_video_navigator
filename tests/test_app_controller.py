import pytest
from unittest.mock import Mock, patch
from controllers.app_controller import AppController
from models.video_model import VideoModel
from models.click_model import ClickConfig


@pytest.fixture
def controller(tmp_path):
    """Fixture to initialize AppController with mocked dependencies."""
    video_model = Mock(spec=VideoModel)
    click_model = ClickConfig(config_file=str(tmp_path / "click_config.json"))
    view = Mock()
    return AppController(video_model, click_model, view)


@patch("pyautogui.position")
@patch("pyautogui.moveTo")
@patch("pyautogui.click")
def test_simulate_click_with_advance(mock_click, mock_move_to, mock_position, controller):
    """Test simulating a click with 30s advance for click1, click2, click3, rem."""
    controller.model_click.get_position.return_value = (500, 600)
    mock_position.return_value = (100, 100)
    controller.model_video.cap = Mock()  # Simulate loaded video
    controller.model_video.current_time = 10.0
    controller.model_video.set_time = Mock()
    controller.update_view = Mock()
    for key in ["click1", "click2", "click3", "rem"]:
        controller.simulate_click(key)
        mock_move_to.assert_any_call(500, 600, duration=0)
        mock_click.assert_called()
        mock_move_to.assert_any_call(100, 100, duration=0)
        controller.model_video.set_time.assert_called_with(40.0)
        controller.update_view.assert_called()
        mock_click.reset_mock()
        mock_move_to.reset_mock()
        controller.model_video.set_time.reset_mock()
        controller.update_view.reset_mock()


@patch("pyautogui.position")
@patch("pyautogui.moveTo")
@patch("pyautogui.click")
def test_simulate_click_no_advance(mock_click, mock_move_to, mock_position, controller):
    """Test simulating a click without advance for other actions."""
    controller.model_click.get_position.return_value = (500, 600)
    mock_position.return_value = (100, 100)
    controller.model_video.cap = Mock()  # Simulate loaded video
    controller.model_video.set_time = Mock()
    controller.update_view = Mock()
    for key in ["lock", "forward", "backward", "start", "end"]:
        controller.simulate_click(key)
        mock_move_to.assert_any_call(500, 600, duration=0)
        mock_click.assert_called()
        mock_move_to.assert_any_call(100, 100, duration=0)
        controller.model_video.set_time.assert_not_called()
        controller.update_view.assert_not_called()
        mock_click.reset_mock()
        mock_move_to.reset_mock()


@patch("tkinter.filedialog.askopenfilename")
def test_load_video_success(mock_askopenfilename, controller):
    """Test successful video loading."""
    mock_askopenfilename.return_value = "test.mp4"
    controller.model_video.load_video = Mock()
    controller.update_view = Mock()
    controller.load_video()
    controller.model_video.load_video.assert_called_with("test.mp4")
    controller.update_view.assert_called_once()


@patch("tkinter.filedialog.askopenfilename")
def test_load_video_no_file(mock_askopenfilename, controller):
    """Test loading when no file is selected."""
    mock_askopenfilename.return_value = ""
    controller.model_video.load_video = Mock()
    controller.update_view = Mock()
    controller.load_video()
    controller.model_video.load_video.assert_not_called()
    controller.update_view.assert_not_called()


def test_navigate_forward(controller):
    """Test forward navigation."""
    controller.model_video.cap = Mock()  # Simulate loaded video
    controller.model_video.current_time = 10.0
    controller.model_video.set_time = Mock()
    controller.update_view = Mock()
    controller.simulate_click = Mock()
    controller.navigate("forward")
    controller.model_video.set_time.assert_called_with(40.0)
    controller.update_view.assert_called_once()
    controller.simulate_click.assert_called_with("forward")


def test_navigate_end(controller):
    """Test end navigation to last slice."""
    controller.model_video.cap = Mock()  # Simulate loaded video
    controller.model_video.get_total_slices = Mock(return_value=5)
    controller.model_video.set_slice = Mock()
    controller.update_view = Mock()
    controller.simulate_click = Mock()
    controller.navigate("end")
    controller.model_video.set_slice.assert_called_with(5)
    controller.update_view.assert_called_once()
    controller.simulate_click.assert_called_with("end")


def test_go_to_slice_valid(controller):
    """Test navigating to a valid slice."""
    controller.model_video.set_slice = Mock()
    controller.update_view = Mock()
    controller.go_to_slice("2")
    controller.model_video.set_slice.assert_called_with(2)
    controller.update_view.assert_called_once()


@patch("tkinter.messagebox.showerror")
def test_go_to_slice_invalid(mock_showerror, controller):
    """Test navigating to an invalid slice."""
    controller.model_video.set_slice = Mock()
    controller.update_view = Mock()
    controller.go_to_slice("invalid")
    controller.model_video.set_slice.assert_not_called()
    controller.update_view.assert_not_called()
    mock_showerror.assert_called_with("Error", "Invalid slice number")
