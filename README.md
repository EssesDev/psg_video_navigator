# PSG Video Navigator

A simple desktop application to navigate video files (AVI/MP4) frame-by-frame and simulate mouse clicks at configurable screen coordinates. Built with Python, Tkinter, OpenCV, and PyAutoGUI, it is designed for cross-platform use (Windows, Ubuntu, macOS) with a focus on Polysomnography (PSG) video analysis or similar use cases.

## Features
- **Video Navigation**: Load AVI/MP4 videos and navigate statically (no playback) with buttons to jump forward/backward by 30 minutes, or to the start/end of the video.
- **Mouse Click Simulation**: Trigger mouse clicks at user-defined (x, y) screen coordinates via buttons, with specific clicks tied to navigation actions.
- **Configurable**: Set custom (x, y) coordinates for each click action through a simple Tkinter interface.
- **Cross-Platform**: Runs natively on Windows, with easy extension to Ubuntu and macOS using PyInstaller for standalone executables.
- **Open-Source**: Built with MIT/Apache-licensed libraries, ensuring no licensing issues for deployment.

## Requirements
- Python 3.10+ (tested on 3.12)
- Libraries: `opencv-python`, `pillow`, `pyautogui`, `pyinstaller`
- OS: Developed on Ubuntu 22.04.4 LTS; deployable on Windows, Ubuntu, macOS

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
2. **Load a Video**: Click "Charger Vidéo" to select an AVI/MP4 file.
3. **Configure Clicks**: Enter (x, y) coordinates for each action (e.g., Clic1, Forward) and click "Set".
4. **Navigate and Click**:
   - Use "Simuler Clic 1/2" to trigger clicks at configured coordinates.
   - Use navigation buttons ("Début", "-30 min", "+30 min", "Fin") to jump through the video and trigger associated clicks.
5. The video frame updates statically in the UI, and clicks are simulated on the screen.

**Note**: PyAutoGUI performs real mouse clicks on your screen. Ensure coordinates are safe to avoid unintended interactions.

## Deployment
To create a standalone executable:
1. Run:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```
2. Find the executable in the `dist/` folder.
3. For Windows: Transfer and run the `.exe`. For Ubuntu/macOS: Rebuild on the target platform with PyInstaller.

## Project Structure
- `main.py`: Core application (MVC pattern: Model for video/click logic, View for Tkinter UI, Controller for event handling).
- Follows SOLID principles for maintainability and extensibility.

## Future Improvements
- Save click configurations to a JSON file.
- Add support for video playback (optional).
- Enhance UI with resizable video display and timestamp indicators.

## License
MIT License. All dependencies (Tkinter, OpenCV, PyAutoGUI, Pillow) are open-source with compatible licenses.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss.