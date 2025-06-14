from skimage.exposure import match_histograms
import numpy as np
from PIL import Image

def harmonize_colors(fg, bg):
    # Separate alpha channel
    alpha = fg.split()[-1]

    # Convert both images to RGB
    fg_rgb = fg.convert("RGB")
    bg_rgb = bg.convert("RGB")

    # Match histograms
    fg_np = np.array(fg_rgb)
    bg_np = np.array(bg_rgb.resize(fg.size))
    matched = match_histograms(fg_np, bg_np, channel_axis=-1)
    matched_img = Image.fromarray(matched.astype('uint8'))

    # Reapply alpha to the result
    matched_img.putalpha(alpha)

    return matched_img

