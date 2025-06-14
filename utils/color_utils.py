from skimage.exposure import match_histograms
import numpy as np
from PIL import Image

def harmonize_colors(fg, bg):
    # Extract alpha and RGB
    fg_rgb = fg.convert("RGB")
    bg_rgb = bg.convert("RGB")
    alpha = fg.split()[-1]  # original transparency

    # Histogram match RGB channels
    fg_np = np.array(fg_rgb)
    bg_np = np.array(bg_rgb.resize(fg.size))
    matched_rgb = match_histograms(fg_np, bg_np, channel_axis=-1)

    # Convert back and reapply alpha
    matched_img = Image.fromarray(matched_rgb.astype('uint8')).convert("RGBA")
    matched_img.putalpha(alpha)  # restore full opacity
    return matched_img
