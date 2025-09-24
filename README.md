# PSG Video Navigator

A desktop application to navigate AVI/MP4 videos frame-by-frame and simulate mouse clicks at configurable screen coordinates. Built with Python, Tkinter, OpenCV, and PyAutoGUI, it is designed for cross-platform use (Windows, Ubuntu, macOS) with a focus on Polysomnography (PSG) video analysis or similar use cases. This project showcases backend development skills, MVC, and SOLID principles for a maintainable codebase.

## Features
- **Video Navigation**: Load AVI/MP4 videos and navigate statically (no playback) with buttons to jump forward/backward by 30 seconds, or to the start/end of the video.
- **Slice Navigation**: Display current slice number (30-second intervals) and jump to a specific slice via input.
- **Mouse Click Simulation**: Trigger mouse clicks at user-defined (x, y) screen coordinates via buttons ("1", "2", "3", "R" for reset), with specific clicks tied to navigation actions. Clicks are performed without moving the cursor permanently.
- **Configurable Clicks**: Set click coordinates by capturing a mouse click on the screen or manually entering (x, y) values through a Settings menu.
- **Lock/Unlock**: Toggle lock state with a button to enable/disable interactions (extendable).
- **Cross-Platform**: Runs natively on Windows, with easy extension to Ubuntu and macOS using PyInstaller for standalone executables.
- **Open-Source**: Built with MIT/Apache-licensed libraries, ensuring no licensing issues for deployment.
- **Menu Bar**: Includes File (Load Video, Exit), Settings (Configure Clicks), and Help (About) menus for improved usability.
- **Responsive Video Display**: Video frames adapt to window size, displayed in a bordered frame, with a minimum window size of 400x300 pixels.
- **Always On Top**: Application window remains in the foreground for user convenience.
- **Version Display**: Shows version 1.0.0 in the bottom-right corner.

## Requirements
- Python 3.10+ (tested on 3.11.7)
- Libraries: `opencv-python`, `pillow`, `pyautogui`, `pyinstaller`
- OS: Developed on Ubuntu 22.04.4 LTS; deployable on Windows, Ubuntu, macOS
- System dependencies (Ubuntu):
  ```bash
  sudo apt install python3-tk libx11-dev libxi-dev libxtst-dev scrot
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/EssesDev/psg-video-navigator.git
   cd psg-video-navigator
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install opencv-python pillow pyautogui pyinstaller
   ```

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. **Load a Video**: Use "File > Load Video" to select an AVI/MP4 file.
3. **Configure Clicks**:
   - Go to "Settings > Configure Clicks" to open the configuration window.
   - For each action (Click1, Click2, Click3, Forward, Backward, Start, End), either:
     - Click "Capture", then click on the screen within 5 seconds to set the coordinates.
     - Enter (x, y) coordinates manually and click "Set".
4. **Navigate and Click**:
   - Use buttons "1", "2", "3" to trigger clicks at configured coordinates.
   - Use "R" to reset click positions to defaults.
   - Use "Lock/Unlock" to toggle interaction state.
   - Use navigation buttons ("Start", "-30s", "+30s", "End") to jump through the video and trigger associated clicks.
   - Enter a slice number (30-second intervals) and click "Go" to jump to that slice.
5. The video frame updates statically in a bordered frame, and the window stays on top. Version 1.0.0 is displayed in the bottom-right.

**Note**: PyAutoGUI performs real mouse clicks on your screen. Ensure coordinates are safe to avoid unintended interactions.

## Deployment
To create a standalone executable:
1. Run:
   ```bash
   pyinstaller --onefile --windowed --name psg-video-navigator main.py
   ```
2. Find the executable in the `dist/` folder as `psg-video-navigator.exe` (Windows) or `psg-video-navigator` (Linux/macOS).
3. For Windows: Transfer and run the `.exe`. For Ubuntu/macOS: Rebuild on the target platform with PyInstaller.

## Project Structure
- `main.py`: Entry point to initialize and run the application.
- `models/`: Contains `VideoModel` (video handling) and `ClickConfig` (click coordinates).
- `controllers/`: Contains `AppController` for coordinating models and view.
- `views/`: Contains `AppView` for the Tkinter-based UI.
- Follows MVC and SOLID principles for maintainability and extensibility.
- Tests: All dependencies (`opencv-python`, `pillow`, `pyautogui`, `pyinstaller`) validated on Python 3.11.7.

## Development Workflow
- Changes are developed in the `dev` branch and merged into `main` after testing.

## Troubleshooting
- Fixed an `AttributeError` in MVC initialization by passing the controller to the view at creation, ensuring robust dependency injection.
- Resolved Tkinter/PyAutoGUI compatibility by using Python 3.11.7 with `python3-tk` on Ubuntu 22.04.
- Fixed `AttributeError` in menu bar by using lambda for safe controller method access.
- Fixed navigation buttons disappearing after video load by switching to grid layout for better widget management.
- Improved click simulation to avoid permanent cursor movement and simplified click configuration with screen capture.
- Updated navigation to 30-second slices, added slice indicator and direct jump input.
- Replaced simulate buttons with Lock/Unlock, 1, 2, 3, R for custom clicks and reset.

## Future Improvements
- Save click configurations to a JSON file.
- Add support for video playback (optional).
- Enhance UI with resizable video display and timestamp indicators.

## License
MIT License. All dependencies (Tkinter, OpenCV, PyAutoGUI, Pillow) are open-source with compatible licenses.

## Contributing
This is a portfolio project with limited maintenance. Pull requests are welcome! For major changes, please open an issue first to discuss.