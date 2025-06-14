from PIL import Image, ImageFilter

def generate_shadow(person_img, light_dir):
    # Clone person
    shadow = person_img.convert('L').point(lambda x: min(x, 50))  # make darker
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=8))   # soft shadow
    # Add offset based on light direction (simplified)
    offset = (int(light_dir[0] * 20), int(light_dir[1] * 20))
    base = Image.new("RGBA", person_img.size, (0, 0, 0, 0))
    base.paste(shadow, offset, shadow)
    base.paste(person_img, (0, 0), person_img)
    return base