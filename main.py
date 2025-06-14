# main.py

from PIL import Image, ImageFilter
from utils.shadow_utils import generate_shadow
from utils.lighting_utils import estimate_light_direction
from utils.color_utils import harmonize_colors
from models.segmentation.mediapipe_segmenter import remove_background_mediapipe
import os

# Step 1: Background removal
raw_path = "assets/person/raw_person.jpg"
no_bg_path = "assets/person/person_no_bg.png"
remove_background_mediapipe(raw_path, no_bg_path)

# Step 2: Load images
position = (250, 100)
bg = Image.open("assets/background/street_scene.jpg")
person = Image.open(no_bg_path)

# Step 3: Estimate lighting
light_dir = estimate_light_direction(bg)

# Step 4: Generate shadow only (separate from person)
shadow = generate_shadow(person, light_dir)

# Step 5: Color harmonization (apply to full-opacity person only)
def feather_edges(img, feather_radius=1):
    alpha = img.split()[-1]
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(radius=feather_radius))

    # Restore opacity around central regions
    boosted_alpha = blurred_alpha.point(lambda x: min(255, int(x * 2)))  # Sharper edges
    img.putalpha(boosted_alpha)
    return img


# Convert person to RGB before harmonization
harmonized_person = harmonize_colors(person, bg)
harmonized_person = feather_edges(harmonized_person)

# Step 6: Paste shadow and person
bg_composite = bg.copy()
bg_composite.paste(shadow, position, shadow)
bg_composite.paste(harmonized_person, position, harmonized_person)
# Step 7: Save debug + final outputs
output_path = "outputs/final_composite.png"
bg_composite.save(output_path)
print(f"✅ Final photorealistic image saved to: {output_path}")
print("Alpha extrema (person):", harmonized_person.split()[-1].getextrema())