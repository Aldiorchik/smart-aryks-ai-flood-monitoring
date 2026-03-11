import torch
import torchvision.transforms as transforms
from PIL import Image
import json
from pathlib import Path

"""
Smart Aryks Citizen Reporting

Computer vision module detecting aryk blockage
from citizen uploaded images.
"""

MODEL = torch.hub.load(
    'pytorch/vision:v0.10.0',
    'resnet18',
    pretrained=True
)

MODEL.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])


def detect_blockage(image_path):

    img = Image.open(image_path).convert("RGB")

    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = MODEL(img)

    prob = torch.softmax(output, dim=1)

    blockage_probability = prob.max().item()

    if blockage_probability > 0.7:
        label = "POSSIBLE_BLOCKAGE"
    else:
        label = "NO_BLOCKAGE"

    return {
        "label": label,
        "probability": round(blockage_probability,3)
    }