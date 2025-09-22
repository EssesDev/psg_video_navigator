import cv2
import numpy as np

# Créer une image vide (100x100 pixels, noire)
img = np.zeros((100, 100, 3), dtype=np.uint8)
height, width, channels = img.shape
print(f"OpenCV test: Image dimensions: {width}x{height}, {channels} channels")

# Optionnel : affiche l'image dans une fenêtre
cv2.imshow("Test OpenCV", img)
cv2.waitKey(3000)  # Attend 3 seconde
cv2.destroyAllWindows()
print("OpenCV window displayed successfully")