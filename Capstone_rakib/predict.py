# predict.py

import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import cv2
from torchvision.models import resnet18, ResNet18_Weights

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
# model = models.resnet18(pretrained=False)
# model = models.resnet18(weights="DEFAULT")
model = resnet18(weights=ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("model/face_model.pth", map_location=device))
model = model.to(device)
model.eval()

# Transform
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ]
)

class_names = ["Face", "Other"]


def predict_image(img_path):
    image = Image.open(img_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    return class_names[predicted.item()]


# Test
img_path = "dataset/train/Face/95.png"
result = predict_image(img_path)
print("Prediction:", result)
