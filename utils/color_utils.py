from skimage.exposure import match_histograms
import numpy as np
from PIL import Image

def harmonize_colors(fg, bg):
    fg_rgb = fg.convert("RGB")
    bg_rgb = bg.convert("RGB")

    fg_np = np.array(fg_rgb)
    bg_np = np.array(bg_rgb.resize(fg.size))

    matched = match_histograms(fg_np, bg_np, channel_axis=-1)
    matched_img = Image.fromarray(matched.astype('uint8'))

    # Reapply alpha from original foreground
    alpha = fg.split()[-1]
    matched_img.putalpha(alpha)
    
    return matched_img
