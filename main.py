import os
import cv2
import numpy as np
from PIL import Image
import pyautogui
from dearpygui import dearpygui as dpg

# Model: Gère la logique vidéo et configs clics (Single Responsibility)
class VideoModel:
    def __init__(self):
        self.cap = None
        self.duration = 0
        self.current_time = 0
        self.frame = None

    def load_video(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("Video file not found")
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            raise ValueError("Could not open video")
        self.duration = self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.cap.get(cv2.CAP_PROP_FPS)
        self.set_time(0)

    def set_time(self, time_sec):
        if self.cap is None:
            return
        self.current_time = max(0, min(time_sec, self.duration))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(self.current_time * fps))
        ret, frame = self.cap.read()
        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def get_frame(self):
        return self.frame

class ClickConfig:
    def __init__(self):
        self.positions = {
            "click1": (100, 100),
            "click2": (200, 200),
            "forward": (300, 300),
            "backward": (400, 400),
            "start": (500, 500),
            "end": (600, 600)
        }

    def set_position(self, key, x, y):
        self.positions[key] = (x, y)

    def get_position(self, key):
        return self.positions.get(key, (0, 0))

# View: Interface Dear PyGui (Single Responsibility: Affichage)
class AppView:
    def __init__(self, controller):
        self.controller = controller
        dpg.create_context()
        dpg.create_viewport(title="PSG Video Navigator", width=800, height=600)
        
        # Texture pour afficher la vidéo
        with dpg.texture_registry():
            dpg.add_dynamic_texture(width=640, height=480, default_value=np.zeros((480, 640, 4), dtype=np.float32), tag="video_texture")

        # Fenêtre principale
        with dpg.window(label="PSG Video Navigator", width=800, height=600):
            # Configs clics
            with dpg.group():
                self.entries = {}
                labels = ["Clic1", "Clic2", "Forward", "Backward", "Start", "End"]
                for i, key in enumerate(["click1", "click2", "forward", "backward", "start", "end"]):
                    with dpg.group(horizontal=True):
                        dpg.add_text(f"{labels[i]} x,y:")
                        x_entry = dpg.add_input_int(width=60, default_value=100)
                        y_entry = dpg.add_input_int(width=60, default_value=100)
                        dpg.add_button(label="Set", callback=lambda s, d, u: self.controller.set_click_position(u[0], dpg.get_value(u[1]), dpg.get_value(u[2])), user_data=(key, x_entry, y_entry))
                        self.entries[key] = (x_entry, y_entry)
            
            # Boutons clics simples
            dpg.add_button(label="Simuler Clic 1", callback=lambda: self.controller.simulate_click("click1"))
            dpg.add_button(label="Simuler Clic 2", callback=lambda: self.controller.simulate_click("click2"))
            
            # Chargement vidéo
            dpg.add_button(label="Charger Vidéo", callback=self.controller.load_video)
            
            # Affichage vidéo
            dpg.add_image("video_texture")
            
            # Boutons navigation
            with dpg.group(horizontal=True):
                dpg.add_button(label="Début", callback=lambda: self.controller.navigate("start"))
                dpg.add_button(label="-30 min", callback=lambda: self.controller.navigate("backward"))
                dpg.add_button(label="+30 min", callback=lambda: self.controller.navigate("forward"))
                dpg.add_button(label="Fin", callback=lambda: self.controller.navigate("end"))

        dpg.setup_dearpygui()
        dpg.show_viewport()

    def update_video_display(self, frame):
        if frame is not None:
            # Convertir frame en RGBA pour Dear PyGui
            img = Image.fromarray(frame)
            img = img.convert("RGBA")
            data = np.array(img, dtype=np.float32) / 255.0
            dpg.set_value("video_texture", data.flatten())

    def run(self):
        dpg.start_dearpygui()
        dpg.destroy_context()

# Controller: Gère interactions (Dependency Inversion)
class AppController:
    def __init__(self, model_video, model_click, view):
        self.model_video = model_video
        self.model_click = model_click
        self.view = view

    def simulate_click(self, key):
        x, y = self.model_click.get_position(key)
        pyautogui.click(x, y)

    def set_click_position(self, key, x, y):
        try:
            x, y = int(x), int(y)
            self.model_click.set_position(key, x, y)
            dpg.show_item(dpg.add_popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="popup_success"))
            dpg.add_text(f"Position for {key} set to ({x}, {y})", parent="popup_success")
        except ValueError:
            dpg.show_item(dpg.add_popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="popup_error"))
            dpg.add_text("Invalid x,y values", parent="popup_error")

    def load_video(self, sender, app_data, user_data):
        # Dear PyGui utilise filedialog différemment; ici on simule avec tkinter pour simplicité
        from tkinter import filedialog, Tk
        Tk().withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.avi *.mp4")])
        if file_path:
            try:
                self.model_video.load_video(file_path)
                self.update_view()
            except Exception as e:
                dpg.show_item(dpg.add_popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="popup_error"))
                dpg.add_text(str(e), parent="popup_error")

    def navigate(self, action):
        if self.model_video.cap is None:
            return
        if action == "forward":
            self.model_video.set_time(self.model_video.current_time + 1800)
        elif action == "backward":
            self.model_video.set_time(self.model_video.current_time - 1800)
        elif action == "start":
            self.model_video.set_time(0)
        elif action == "end":
            self.model_video.set_time(self.model_video.duration)
        self.update_view()
        self.simulate_click(action)

    def update_view(self):
        frame = self.model_video.get_frame()
        self.view.update_video_display(frame)

# Lancement
if __name__ == "__main__":
    video_model = VideoModel()
    click_model = ClickConfig()
    view = AppView(None)
    controller = AppController(video_model, click_model, view)
    view.controller = controller
    view.run()