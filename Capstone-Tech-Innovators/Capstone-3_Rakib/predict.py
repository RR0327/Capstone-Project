import torch
from torchvision import models, transforms
from PIL import Image

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
