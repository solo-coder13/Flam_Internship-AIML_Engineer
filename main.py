# main.py

from PIL import Image
from utils.shadow_utils import generate_shadow
from utils.lighting_utils import estimate_light_direction
from utils.color_utils import harmonize_colors
from utils.background_remover import remove_background  # ✅ NEW
from utils.background_remover import remove_background
from PIL import ImageFilter
import os

# ---- Step 1: Remove background automatically ----
raw_path = "assets/person/raw_person.jpg"
no_bg_path = "assets/person/person_no_bg.png"

from models.segmentation.mediapipe_segmenter import remove_background_mediapipe

# Use ML-based MediaPipe segmentation
remove_background_mediapipe("assets/person/raw_person.jpg", "assets/person/person_no_bg.png")


# ---- Step 2: Load background and extracted person image ----
position = (250, 150)
bg = Image.open("assets/background/street_scene.jpg")
person = Image.open(no_bg_path)

# ---- Step 3: Estimate light direction ----
light_dir = estimate_light_direction(bg)

# ---- Step 4: Generate shadow ----
person_with_shadow = generate_shadow(person, light_dir)
shadow = generate_shadow(person, light_dir)
bg_with_shadow = bg.copy()
bg_with_shadow.paste(shadow, position, shadow)

# ---- Step 5: Match color tone ----
def feather_edges(img, feather_radius=2):
    alpha = img.split()[-1]
    soft_alpha = alpha.filter(ImageFilter.GaussianBlur(radius=feather_radius))
    img.putalpha(soft_alpha)
    return img
harmonized_person = harmonize_colors(person_with_shadow, bg)
harmonized_person = feather_edges(harmonized_person)  # Point 3: Feathering


# ---- Step 6: Composite onto background ----
bg_copy = bg.copy()
position = (250, 150)  # Adjust as needed
# bg_copy.paste(harmonized_person, position, harmonized_person)
# Paste shadow first
bg_with_shadow = bg.copy()
bg_with_shadow.paste(shadow, position, shadow)

# Then paste the harmonized + feathered person
bg_with_shadow.paste(harmonized_person, position, harmonized_person)

# Save final result
bg_with_shadow.save("outputs/final_composite.png")
print("✅ Final photorealistic image saved.")

# ---- Step 7: Save final image ----
output_path = "outputs/final_composite.png"
bg_copy.save(output_path)
print(f" Final image saved to: {output_path}")
