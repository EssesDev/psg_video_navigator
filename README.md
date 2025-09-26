# PSG Video Navigator

A desktop application to navigate AVI/MP4 videos frame-by-frame and simulate mouse clicks at configurable screen coordinates. Built with Python, Tkinter, OpenCV, and PyAutoGUI, it is designed for cross-platform use (Windows, Ubuntu, macOS) with a focus on Polysomnography (PSG) video analysis or similar use cases. This project showcases backend development skills, MVC, and SOLID principles for a maintainable codebase.

## Features
- **Video Navigation**: Load AVI/MP4 videos and navigate statically (no playback) with buttons to jump forward/backward by 30 seconds, to the start, or to the last slice of the video.
- **Slice Navigation**: Display current slice number (30-second intervals) and jump to a specific slice via input.
- **Mouse Click Simulation**: Trigger mouse clicks at user-defined (x, y) screen coordinates via buttons ("1", "2", "3", "R" for sleep stages, "Lock/Unlock"). Buttons "1", "2", "3", and "R" also advance the video by 30 seconds. Navigation buttons ("Forward", "Backward", "Start", "End") trigger clicks, with "End" moving to the last slice.
- **Configurable Clicks**: Set click coordinates for all actions (including Lock/Unlock and R) by capturing a mouse click on the screen or manually entering (x, y) values through a Settings menu. Reset all positions to defaults via a Reset button. Configurations are saved to a JSON file.
- **Cross-Platform**: Runs natively on Windows, with easy extension to Ubuntu and macOS using PyInstaller for standalone executables.
- **Open-Source**: Built with MIT/Apache-licensed libraries, ensuring no licensing issues for deployment.
- **Menu Bar**: Includes File (Load Video, Exit), Settings (Configure Clicks), and Help (About) menus for improved usability.
- **Responsive Video Display**: Video frames adapt to window size, displayed in a bordered frame, with a minimum window size of 500x400 pixels.
- **Always On Top**: Application window remains in the foreground for user convenience.
- **Version Display**: Shows version 1.0.0 in the bottom-right corner.

## Requirements
- Python 3.10+ (tested on 3.11.7)
- Libraries: `opencv-python`, `pillow`, `pyautogui`, `pyinstaller`
- OS: Developed on Ubuntu 22.04.4 LTS; deployable on Windows, Ubuntu, macOS
- System dependencies (Ubuntu):
  ```bash
  sudo apt install python3-tk libx11-dev libxi-dev libxtst-dev scrot

## Testing
- Comprehensive unit tests for `video_model.py`, `click_model.py`, `app_controller.py`, and `app_view.py` using `pytest`.
- Tests cover video loading, navigation, click configuration, and UI initialization.
- Run tests with: `pytest tests/ -v`

## Troubleshooting
- Fixed issue where click positions were reset on application restart by adjusting ClickConfig initialization to prioritize loading saved positions.