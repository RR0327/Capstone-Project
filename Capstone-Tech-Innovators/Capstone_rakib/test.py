import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from utils import get_device, load_model, get_eval_transform

# paths
test_dir = "dataset/train"
model_path = "model/face_model.pth"

# device
device = get_device()

# dataset
test_data = datasets.ImageFolder(test_dir, transform=get_eval_transform())
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

class_names = test_data.classes

# load model
model = load_model(model_path, num_classes=len(class_names), device=device)

correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)
        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total

print(f"Test Accuracy: {accuracy:.2f}%")
