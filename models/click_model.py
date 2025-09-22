"""Module for managing mouse click configurations in PSG Video Navigator.

This module contains the ClickConfig class, responsible for storing and updating
click positions, following the Single Responsibility Principle.
"""


class ClickConfig:
    """Manages mouse click coordinates for various actions.

    Attributes:
        positions (dict): Dictionary mapping action keys to (x, y) coordinates.
    """

    def __init__(self):
        """Initialize ClickConfig with default click positions."""
        # Default (x, y) coordinates for each action
        self.positions = {
            "click1": (100, 100),   # Simple click 1
            "click2": (200, 200),   # Simple click 2
            "forward": (300, 300),  # Forward 30 minutes
            "backward": (400, 400), # Backward 30 minutes
            "start": (500, 500),    # Start of video
            "end": (600, 600)       # End of video
        }

    def set_position(self, key: str, x: int, y: int) -> None:
        """Set the (x, y) coordinates for a specific action.

        Args:
            key (str): Action identifier (e.g., 'click1', 'forward').
            x (int): X-coordinate for the click.
            y (int): Y-coordinate for the click.
        """
        self.positions[key] = (x, y)

    def get_position(self, key: str) -> tuple:
        """Get the (x, y) coordinates for a specific action.

        Args:
            key (str): Action identifier.

        Returns:
            tuple: (x, y) coordinates, defaults to (0, 0) if key is invalid.
        """
        return self.positions.get(key, (0, 0))
    