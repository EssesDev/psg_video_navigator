from PIL import Image

# Créer une image rouge 100x100
img = Image.new("RGB", (100, 100), color="red")
img.save("test_pillow_image.png")
print("Pillow test: Red image saved as test_pillow_image.png")

# Vérifier que l'image existe
import os
if os.path.exists("test_pillow_image.png"):
    print("Pillow test: Image file created successfully")
else:
    print("Pillow test: Failed to create image file")