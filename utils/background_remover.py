# utils/background_remover.py
from rembg import remove
from PIL import Image
import os

def remove_background(input_path, output_path):
    if not os.path.exists(output_path):
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        print(f"Saved: {output_path}")
    else:
        print("Background already removed.")
