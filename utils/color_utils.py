from skimage.exposure import match_histograms
import numpy as np
from PIL import Image

def harmonize_colors(fg, bg):
    fg_np = np.array(fg)
    bg_np = np.array(bg.resize(fg.size))
    matched = match_histograms(fg_np, bg_np, channel_axis=-1)
    return Image.fromarray(matched.astype('uint8'))