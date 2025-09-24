"""Main entry point for PSG Video Navigator.

This script initializes the MVC components (VideoModel, ClickConfig, AppController,
AppView) and starts the Tkinter application.
"""

from models.video_model import VideoModel
from models.click_model import ClickConfig
from controllers.app_controller import AppController
from views.app_view import AppView


def main():
    """Initialize and run the PSG Video Navigator application."""
    # Create model instances
    video_model = VideoModel()
    click_model = ClickConfig()

    # Create controller with models
    controller = AppController(video_model, click_model, None)

    # Create view with controller
    view = AppView(controller)

    # Update controller with view reference
    controller.view = view

    # Start the Tkinter event loop
    view.mainloop()

    # Save click configurations on exit
    click_model.save_positions()


if __name__ == "__main__":
    main()
    