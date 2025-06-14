# main.py

from PIL import Image, ImageFilter
from utils.shadow_utils import generate_shadow
from utils.lighting_utils import estimate_light_direction
from utils.color_utils import harmonize_colors
from models.segmentation.mediapipe_segmenter import remove_background_mediapipe
import os

# ---- Step 1: Remove background automatically ----
raw_path = "assets/person/raw_person.jpg"
no_bg_path = "assets/person/person_no_bg.png"
remove_background_mediapipe(raw_path, no_bg_path)

# ---- Step 2: Load background and extracted person image ----
position = (250, 100)  # Adjust as needed
bg = Image.open("assets/background/street_scene.jpg")
person = Image.open(no_bg_path)

# ---- Step 3: Estimate light direction ----
light_dir = estimate_light_direction(bg)

# ---- Step 4: Generate shadow ----
shadow = generate_shadow(person, light_dir)

# ---- Step 5: Match color tone + feather edges ----
def feather_edges(img, feather_radius=1):  # Reduce from 2 to 1
    alpha = img.split()[-1]
    soft_alpha = alpha.filter(ImageFilter.GaussianBlur(radius=feather_radius))
    img.putalpha(soft_alpha)
    return img
person_with_shadow = generate_shadow(person, light_dir)
harmonized_person = harmonize_colors(person, bg)  # Use original person image

# ---- Step 6: Composite onto background ----
bg_with_shadow = bg.copy()
bg_with_shadow.paste(shadow, position, shadow)
bg_with_shadow.paste(harmonized_person, position, harmonized_person)
# Paste shadow first
bg_with_shadow.paste(person_with_shadow, position, person_with_shadow)  # This includes shadow + silhouette

# Paste harmonized person on top
bg_with_shadow.paste(harmonized_person, position, harmonized_person)  # Full color person

harmonized_person = feather_edges(harmonized_person, feather_radius=1)

# Debugging images
harmonized_person.save("outputs/debug_harmonized_person.png")
person_with_shadow.save("outputs/debug_person_with_shadow.png")
print("Alpha max value:", harmonized_person.split()[-1].getextrema())

# ---- Step 7: Save final image ----
output_path = "outputs/final_composite.png"
bg_with_shadow.save(output_path)
print(f"✅ Final photorealistic image saved to: {output_path}")