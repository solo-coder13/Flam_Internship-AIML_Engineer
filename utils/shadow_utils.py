from PIL import Image, ImageFilter
from PIL import ImageOps

def generate_shadow(person_img, light_dir=(1, -1), blur=10, opacity=80):
    # Convert person image to grayscale alpha mask
    alpha = person_img.split()[-1]
    
    # Create the shadow from alpha
    shadow = Image.new("RGBA", person_img.size, (0, 0, 0, 0))
    black_shadow = Image.new("RGBA", person_img.size, (0, 0, 0, opacity))
    shadow.paste(black_shadow, mask=alpha)
    
    # Offset shadow based on light direction
    offset_x = int(light_dir[0] * 20)
    offset_y = int(light_dir[1] * 20)
    shadow = shadow.transform(
        shadow.size,
        Image.AFFINE,
        (1, 0, offset_x, 0, 1, offset_y),
        resample=Image.BILINEAR,
    )
    
    # Blur to create soft shadow
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur))
    
    return shadow
