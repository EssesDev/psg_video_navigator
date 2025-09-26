import pytest
import os
import json
from unittest.mock import mock_open, patch
from models.click_model import ClickConfig


@pytest.fixture
def click_model(tmp_path):
    """Fixture to initialize ClickConfig with a temporary config file."""
    config_file = tmp_path / "click_config.json"
    return ClickConfig(config_file=str(config_file))


def test_reset_positions(click_model):
    """Test resetting positions to defaults."""
    click_model.positions["click1"] = (999, 999)
    click_model.reset_positions()
    assert click_model.positions["click1"] == (100, 100)
    assert click_model.positions["rem"] == (400, 400)
    assert click_model.positions["lock"] == (900, 900)
    assert os.path.exists(click_model.config_file)


def test_set_position(click_model):
    """Test setting a position for an action."""
    click_model.set_position("click1", 500, 600)
    assert click_model.get_position("click1") == (500, 600)
    with open(click_model.config_file, "r") as f:
        data = json.load(f)
    assert data["click1"] == [500, 600]


def test_get_position_invalid_key(click_model):
    """Test getting position for an invalid key."""
    assert click_model.get_position("invalid") == (0, 0)


@patch("builtins.open", new_callable=mock_open, read_data='{"click1": [1000, 1000], "rem": [2000, 2000]}')
def test_load_positions(mock_file, click_model):
    """Test loading positions from JSON file."""
    click_model.load_positions()
    assert click_model.positions["click1"] == (1000, 1000)
    assert click_model.positions["rem"] == (2000, 2000)
    assert click_model.positions["forward"] == (500, 500)  # Unchanged default


@patch("builtins.open", side_effect=FileNotFoundError)
def test_load_positions_file_not_found(mock_file, click_model):
    """Test loading when JSON file does not exist."""
    click_model.load_positions()
    assert click_model.positions["click1"] == (100, 100)  # Defaults unchanged
