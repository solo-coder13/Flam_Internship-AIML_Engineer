from utils.shadow_utils import generate_shadow
from utils.lighting_utils import estimate_light_direction
from utils.color_utils import harmonize_colors
from PIL import Image

# Load background and person
bg = Image.open('assets/background/street_scene.jpg')
person = Image.open('assets/person/person_no_bg.png')

# Estimate light direction
light_dir = estimate_light_direction(bg)

# Generate realistic shadow
person_with_shadow = generate_shadow(person, light_dir)

# Color match person to background
harmonized_person = harmonize_colors(person_with_shadow, bg)

# Composite final image
bg.paste(harmonized_person, (300, 150), harmonized_person)  # Adjust position
bg.save('outputs/final_composite.png')