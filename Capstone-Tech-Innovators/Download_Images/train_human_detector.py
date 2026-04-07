"""import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Image transforms
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ]
)

# Dataset
train_dataset = datasets.ImageFolder("dataset/train", transform=transform)
val_dataset = datasets.ImageFolder("dataset/val", transform=transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)

# Load pretrained ResNet18
model = models.resnet18(weights="DEFAULT")

# Change final layer (2 classes)
model.fc = nn.Linear(model.fc.in_features, 2)

model = model.to(device)

# Loss & optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# Training
epochs = 5

for epoch in range(epochs):

    model.train()
    running_loss = 0

    for images, labels in train_loader:

        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs} Loss: {running_loss:.4f}")

print("Training complete")

# Save model
torch.save(model.state_dict(), "human_detector.pth")
"""

# Shortest version for train the dataset easily
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# -----------------------------
# Device (CPU for now)
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# -----------------------------
# Transforms
# -----------------------------
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ]
)

# -----------------------------
# Dataset
# -----------------------------
train_dataset = datasets.ImageFolder("dataset/train", transform=transform)

print("Classes:", train_dataset.classes)
print("Total training images:", len(train_dataset))

# -----------------------------
# DataLoader (UPDATED)
# -----------------------------
train_loader = DataLoader(
    train_dataset,
    batch_size=8,  # Reduced batch size
    shuffle=True,
    num_workers=2,  # Faster loading

    # No multiprocessing → no error, But slower

    # num_workers=0   # Set to 0 for Windows compatibility (if needed)
)

# -----------------------------
# Model (ResNet18)
# -----------------------------
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Modify final layer (2 classes: human vs other)
model.fc = nn.Linear(model.fc.in_features, 2)
model = model.to(device)

# -----------------------------
# Loss & Optimizer
# -----------------------------
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# -----------------------------
# Training Loop (UPDATED)
# -----------------------------
num_epochs = 5

for epoch in range(num_epochs):
    print(f"\nEpoch {epoch+1}/{num_epochs} started...")

    running_loss = 0.0

    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)

        # Forward
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        # Print progress every 50 batches
        if i % 50 == 0:
            print(f"Batch {i}/{len(train_loader)} | Loss: {loss.item():.4f}")

    epoch_loss = running_loss / len(train_loader)
    print(f"Epoch {epoch+1} finished | Avg Loss: {epoch_loss:.4f}")

print("\nTraining Completed!")

# -----------------------------
# Save Model
# -----------------------------
torch.save(model.state_dict(), "human_detector.pth")
print("Model saved as human_detector.pth")
"""

# Solution of the shortest version for train the dataset easily
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader


def main():
    # -----------------------------
    # Device
    # -----------------------------
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # -----------------------------
    # Transforms
    # -----------------------------
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ]
    )

    # -----------------------------
    # Dataset
    # -----------------------------
    train_dataset = datasets.ImageFolder("dataset/train", transform=transform)

    print("Classes:", train_dataset.classes)
    print("Total training images:", len(train_dataset))

    # -----------------------------
    # DataLoader
    # -----------------------------
    train_loader = DataLoader(
        train_dataset, batch_size=8, shuffle=True, num_workers=2  # Now safe
    )

    # -----------------------------
    # Model
    # -----------------------------
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model = model.to(device)

    # -----------------------------
    # Loss & Optimizer
    # -----------------------------
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # -----------------------------
    # Training Loop
    # -----------------------------
    num_epochs = 5

    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch+1}/{num_epochs} started...")

        running_loss = 0.0

        for i, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            if i % 50 == 0:
                print(f"Batch {i}/{len(train_loader)} | Loss: {loss.item():.4f}")

        epoch_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1} finished | Avg Loss: {epoch_loss:.4f}")

    print("\nTraining Completed!")
    torch.save(model.state_dict(), "human_detector.pth")
    print("Model saved as human_detector.pth")


# THIS IS THE FIX
if __name__ == "__main__":
    main()
"""

# Code for train the small dataset


import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader


def main():
    # -----------------------------
    # Device
    # -----------------------------
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # -----------------------------
    # Transforms
    # -----------------------------
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ]
    )

    # -----------------------------
    # Dataset
    # -----------------------------
    train_dataset = datasets.ImageFolder("dataset_small/train", transform=transform)

    print("Classes:", train_dataset.classes)
    print("Total training images:", len(train_dataset))

    # -----------------------------
    # DataLoader
    # -----------------------------
    train_loader = DataLoader(
        train_dataset, batch_size=8, shuffle=True, num_workers=2  # Now safe
    )

    # -----------------------------
    # Model
    # -----------------------------
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model = model.to(device)

    # -----------------------------
    # Loss & Optimizer
    # -----------------------------
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # -----------------------------
    # Training Loop
    # -----------------------------
    num_epochs = 5

    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch+1}/{num_epochs} started...")

        running_loss = 0.0

        for i, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            if i % 50 == 0:
                print(f"Batch {i}/{len(train_loader)} | Loss: {loss.item():.4f}")

        epoch_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1} finished | Avg Loss: {epoch_loss:.4f}")

    print("\nTraining Completed!")
    torch.save(model.state_dict(), "human_detector.pth")
    print("Model saved as human_detector.pth")


# THIS IS THE FIX
if __name__ == "__main__":
    main()
