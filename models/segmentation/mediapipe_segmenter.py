import cv2
import mediapipe as mp
from PIL import Image
import numpy as np
import os

def remove_background_mediapipe(input_path, output_path):
    if os.path.exists(output_path):
        print("✅ Segmented image already exists.")
        return

    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    image = cv2.imread(input_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as segmenter:
        result = segmenter.process(rgb_image)

        mask = result.segmentation_mask
        condition = mask > 0.5

        bg = np.zeros(image.shape, dtype=np.uint8)
        bg[:] = [0, 0, 0]  # Black background

        output_image = np.where(condition[..., None], image, bg)

        # Convert to RGBA and apply transparency
        rgba = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGBA)
        rgba[..., 3] = (condition * 255).astype(np.uint8)

        # Save as transparent PNG
        Image.fromarray(rgba).save(output_path)
        print(f"Background removed using MediaPipe. Saved: {output_path}")
