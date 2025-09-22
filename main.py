import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import pyautogui
import os

# Model: Gère la logique vidéo et configs clics (Single Responsibility)
class VideoModel:
    def __init__(self):
        self.cap = None  # VideoCapture object
        self.duration = 0  # in seconds
        self.current_time = 0  # in seconds
        self.frame = None  # Current frame as numpy array

    def load_video(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("Video file not found")
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            raise ValueError("Could not open video")
        self.duration = self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.cap.get(cv2.CAP_PROP_FPS)
        self.set_time(0)  # Start at beginning

    def set_time(self, time_sec):
        if self.cap is None:
            return
        self.current_time = max(0, min(time_sec, self.duration))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(self.current_time * fps))
        ret, frame = self.cap.read()
        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB

    def get_frame(self):
        return self.frame

class ClickConfig:
    def __init__(self):
        # Default positions (x, y) pour chaque action ; extensible
        self.positions = {
            "click1": (100, 100),  # Exemple pour clic simple 1
            "click2": (200, 200),  # Exemple pour clic simple 2
            "forward": (300, 300),  # Pour +30 min
            "backward": (400, 400),  # Pour -30 min
            "start": (500, 500),  # Pour début
            "end": (600, 600)     # Pour fin
        }

    def set_position(self, key, x, y):
        self.positions[key] = (x, y)

    def get_position(self, key):
        return self.positions.get(key, (0, 0))

# View: Interface Tkinter (Single Responsibility: Affichage)
class AppView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("PSG Video Navigator")
        self.controller = controller
        self.geometry("800x600")

        # Section configs clics
        self.config_frame = tk.Frame(self)
        self.config_frame.pack(pady=10)
        self.create_config_entries()

        # Boutons clics simples
        tk.Button(self, text="Simuler Clic 1", command=lambda: self.controller.simulate_click("click1")).pack(pady=5)
        tk.Button(self, text="Simuler Clic 2", command=lambda: self.controller.simulate_click("click2")).pack(pady=5)

        # Chargement vidéo
        tk.Button(self, text="Charger Vidéo", command=self.controller.load_video).pack(pady=10)

        # Affichage frame
        self.video_label = tk.Label(self)
        self.video_label.pack()

        # Boutons navigation (avec clics associés)
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)
        tk.Button(nav_frame, text="Début", command=lambda: self.controller.navigate("start")).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="-30 min", command=lambda: self.controller.navigate("backward")).grid(row=0, column=1, padx=5)
        tk.Button(nav_frame, text="+30 min", command=lambda: self.controller.navigate("forward")).grid(row=0, column=2, padx=5)
        tk.Button(nav_frame, text="Fin", command=lambda: self.controller.navigate("end")).grid(row=0, column=3, padx=5)

    def create_config_entries(self):
        # Champs pour configurer x,y par action
        labels = ["Clic1", "Clic2", "Forward", "Backward", "Start", "End"]
        self.entries = {}
        for i, key in enumerate(["click1", "click2", "forward", "backward", "start", "end"]):
            tk.Label(self.config_frame, text=f"{labels[i]} x,y:").grid(row=i, column=0)
            x_entry = tk.Entry(self.config_frame, width=5)
            y_entry = tk.Entry(self.config_frame, width=5)
            x_entry.grid(row=i, column=1)
            y_entry.grid(row=i, column=2)
            tk.Button(self.config_frame, text="Set", command=lambda k=key, xe=x_entry, ye=y_entry: self.controller.set_click_position(k, xe.get(), ye.get())).grid(row=i, column=3)
            self.entries[key] = (x_entry, y_entry)

    def update_video_display(self, frame):
        if frame is not None:
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk  # Keep reference
            self.video_label.configure(image=imgtk)

# Controller: Gère interactions (Dependency Inversion: Dépend des abstractions Model/View)
class AppController:
    def __init__(self, model_video, model_click, view):
        self.model_video = model_video
        self.model_click = model_click
        self.view = view

    def simulate_click(self, key):
        x, y = self.model_click.get_position(key)
        pyautogui.click(x, y)

    def set_click_position(self, key, x_str, y_str):
        try:
            x, y = int(x_str), int(y_str)
            self.model_click.set_position(key, x, y)
            messagebox.showinfo("Config", f"Position for {key} set to ({x}, {y})")
        except ValueError:
            messagebox.showerror("Erreur", "Invalid x,y values")

    def load_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.avi *.mp4")])
        if file_path:
            try:
                self.model_video.load_video(file_path)
                self.update_view()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def navigate(self, action):
        if self.model_video.cap is None:
            return
        if action == "forward":
            self.model_video.set_time(self.model_video.current_time + 1800)  # 30 min = 1800 sec
        elif action == "backward":
            self.model_video.set_time(self.model_video.current_time - 1800)
        elif action == "start":
            self.model_video.set_time(0)
        elif action == "end":
            self.model_video.set_time(self.model_video.duration)
        self.update_view()
        self.simulate_click(action)  # Simule clic associé

    def update_view(self):
        frame = self.model_video.get_frame()
        self.view.update_video_display(frame)

# Lancement (Open-Closed: Facile à étendre)
if __name__ == "__main__":
    video_model = VideoModel()
    click_model = ClickConfig()
    controller = AppController(video_model, click_model, None)  # Crée le controller d'abord
    view = AppView(controller)  # Passe le controller directement
    controller.view = view  # Met à jour la référence dans le controller
    view.mainloop()