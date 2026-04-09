"""
import torch
from torchvision import models, transforms
from PIL import Image

# Load model architecture and weights

model = models.resnet18()
model.fc = torch.nn.Linear(model.fc.in_features, 2)

model.load_state_dict(torch.load("human_detector.pth"))
model.eval()

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ]
)

img = Image.open("test.jpg")

img = transform(img).unsqueeze(0)

output = model(img)

pred = torch.argmax(output)

classes = ["human", "other"]

print("Prediction:", classes[pred])
"""

import torch
from torchvision import transforms, models
from PIL import Image

# Load model
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("best_human_detector.pth"))
model.eval()

classes = ["human", "other"]

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ]
)

# Load image
# test1.jpg is predicted as other.
# test2.jpg is predicted as other.
# test3.jpg is predicted as other.
# test4.jpg is predicted as other.
# test5.jpg is predicted as other.

img_path = "test2.jpg"  # change this
image = Image.open(img_path).convert("RGB")
image = transform(image).unsqueeze(0)

# Prediction
with torch.no_grad():
    output = model(image)
    _, pred = torch.max(output, 1)

print("Prediction:", classes[pred.item()])
