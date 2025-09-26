"""Module for managing mouse click configurations in PSG Video Navigator.

This module contains the ClickConfig class, responsible for storing and updating
click positions, following the Single Responsibility Principle.
"""

import json
import os


class ClickConfig:
    """Manages mouse click coordinates for various actions.

    Attributes:
        positions (dict): Dictionary mapping action keys to (x, y) coordinates.
        config_file (str): Path to the JSON configuration file.
    """

    def __init__(self, config_file: str = "click_config.json"):
        """Initialize ClickConfig with default or loaded click positions."""
        self.config_file = config_file
        self.reset_positions()
        self.load_positions()  # Load from file if exists

    def reset_positions(self) -> None:
        """Reset positions to default values."""
        # Default (x, y) coordinates for each action
        self.positions = {
            "click1": (100, 100),   # Button 1
            "click2": (200, 200),   # Button 2
            "click3": (300, 300),   # Button 3
            "rem": (400, 400),      # REM button
            "forward": (500, 500),  # +30s
            "backward": (600, 600), # -30s
            "start": (700, 700),    # Start
            "end": (800, 800),      # End
            "lock": (900, 900)      # Lock/Unlock button
        }
        self.save_positions()  # Save defaults to file

    def set_position(self, key: str, x: int, y: int) -> None:
        """Set the (x, y) coordinates for a specific action.

        Args:
            key (str): Action identifier (e.g., 'click1', 'forward').
            x (int): X-coordinate for the click.
            y (int): Y-coordinate for the click.
        """
        self.positions[key] = (x, y)
        self.save_positions()  # Save after setting position

    def get_position(self, key: str) -> tuple:
        """Get the (x, y) coordinates for a specific action.

        Args:
            key (str): Action identifier.

        Returns:
            tuple: (x, y) coordinates, defaults to (0, 0) if key is invalid.
        """
        return self.positions.get(key, (0, 0))

    def load_positions(self) -> None:
        """Load click positions from a JSON file if it exists."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    loaded_positions = json.load(f)
                # Convert lists to tuples for consistency
                self.positions.update({k: tuple(v) for k, v in loaded_positions.items()})
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_positions(self) -> None:
        """Save click positions to a JSON file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.positions, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
