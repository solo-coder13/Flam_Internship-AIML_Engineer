# main.py

from PIL import Image, ImageFilter
from utils.shadow_utils import generate_shadow
from utils.lighting_utils import estimate_light_direction
from utils.color_utils import harmonize_colors
import os

# Step 1: Load images
bg_path = "assets/background/street_scene.jpg"
person_path = "assets/person/person_no_bg.png"
bg = Image.open(bg_path).convert("RGBA")
person = Image.open(person_path).convert("RGBA")
position = (250, 150)

# Step 2: Estimate lighting direction
light_dir = estimate_light_direction(bg)

# Step 3: Generate shadow from person
shadow = generate_shadow(person, light_dir)

# Step 4: Color harmonization (preserve alpha manually)
def harmonize_colors_preserve_alpha(fg, bg):
    alpha = fg.split()[-1]
    fg_rgb = fg.convert("RGB")
    bg_rgb = bg.convert("RGB").resize(fg.size)
    
    from skimage.exposure import match_histograms
    import numpy as np
    fg_np = np.array(fg_rgb)
    bg_np = np.array(bg_rgb)
    matched = match_histograms(fg_np, bg_np, channel_axis=-1)
    
    from PIL import Image
    result = Image.fromarray(matched.astype('uint8')).convert("RGBA")
    result.putalpha(alpha)  # reapply alpha
    return result

# Step 5: Feather edges slightly
def feather_alpha(img, radius=1):
    alpha = img.split()[-1]
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(radius))
    enhanced_alpha = blurred_alpha.point(lambda p: min(255, int(p * 2)))  # reboost strength
    img.putalpha(enhanced_alpha)
    return img

# Apply harmonization and feathering
harmonized = harmonize_colors_preserve_alpha(person, bg)
harmonized = feather_alpha(harmonized)

# Step 6: Composite on background
composite = bg.copy()
composite.paste(shadow, position, shadow)
composite.paste(harmonized, position, harmonized)

# Step 7: Save output
output_path = "outputs/final_composite.png"
composite.save(output_path)
print(f"✅ Final photorealistic image saved at: {output_path}")
