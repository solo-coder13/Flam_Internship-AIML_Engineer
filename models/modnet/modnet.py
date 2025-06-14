import torch.nn as nn
from .mobilenetv2 import MobileNetV2Backbone

class MODNet(nn.Module):
    def __init__(self, backbone='mobilenetv2'):
        super(MODNet, self).__init__()

        assert backbone == 'mobilenetv2', 'Only MobileNetV2 backbone is supported.'
        self.backbone = MobileNetV2Backbone(pretrained=True)

        self.conv1 = nn.Conv2d(1280, 1, kernel_size=1)

    def forward(self, x, inference=False):
        features = self.backbone(x)
        matte = self.conv1(features)
        matte = nn.functional.interpolate(matte, size=x.shape[2:], mode='bilinear', align_corners=False)
        return None, None, matte
