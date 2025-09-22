import pyautogui
import time

# Configurer PyAutoGUI pour éviter des clics accidentels
pyautogui.FAILSAFE = True  # Déplace le curseur en haut à gauche pour annuler
pyautogui.PAUSE = 0.5  # Pause entre actions

print("PyAutoGUI test: Clique à (100, 100) dans 3 secondes...")
time.sleep(3)  # Temps pour te préparer
pyautogui.click(100, 100)
print("PyAutoGUI test: Clic effectué")