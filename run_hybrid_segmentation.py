# run_hybrid_segmentation.py

from rembg import remove
from PIL import Image
import torch
from torchvision import transforms
import cv2
import numpy as np
from models.modnet.modnet import MODNet

def run_u2net_rembg(input_path, output_path):
    input_img = Image.open(input_path)
    output = remove(input_img)
    output.save(output_path)
    print(f"✅ U²-Net segmentation saved to: {output_path}")

def run_modnet_refinement(input_path, output_path, ckpt_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    modnet = MODNet(backbone='mobilenetv2')
    modnet.load_state_dict(torch.load(ckpt_path, map_location=device))
    modnet.to(device).eval()

    im = cv2.imread(input_path)
    im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im_rgb = cv2.resize(im_rgb, (512, 512))

    im_tensor = transforms.ToTensor()(im_rgb).unsqueeze(0).to(device)
    _, _, matte = modnet(im_tensor, True)

    matte_np = matte[0][0].data.cpu().numpy()
    matte_np = (matte_np * 255).astype(np.uint8)
    matte_np = cv2.resize(matte_np, (im.shape[1], im.shape[0]))

    rgba = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = matte_np

    cv2.imwrite(output_path, rgba)
    print(f"✅ MODNet-refined image saved to: {output_path}")

if __name__ == "__main__":
    raw_img = "assets/person/raw_person.jpg"
    u2_output = "assets/person/u2_output.png"
    final_output = "assets/person/person_no_bg.png"
    modnet_ckpt = "models/modnet/weights/modnet_photographic_portrait_matting.ckpt"

    run_u2net_rembg(raw_img, u2_output)
    run_modnet_refinement(u2_output, final_output, modnet_ckpt)
