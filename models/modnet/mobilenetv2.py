import torch.nn as nn
from torchvision.models import mobilenet_v2

def MobileNetV2Backbone(pretrained=True):
    model = mobilenet_v2(pretrained=pretrained).features
    return model
