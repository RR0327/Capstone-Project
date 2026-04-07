# utils.py:
import os
from typing import List, Optional, Tuple

import torch
import torch.nn as nn
from PIL import Image
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_train_transform(image_size: int = 224) -> transforms.Compose:
    return transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
        ]
    )


def get_eval_transform(image_size: int = 224) -> transforms.Compose:
    return transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
        ]
    )


def build_dataloaders(
    train_dir: str,
    val_dir: str,
    batch_size: int = 32,
    num_workers: int = 0,
    image_size: int = 224,
) -> Tuple[DataLoader, DataLoader, List[str]]:
    train_data = datasets.ImageFolder(
        train_dir, transform=get_train_transform(image_size)
    )
    val_data = datasets.ImageFolder(val_dir, transform=get_eval_transform(image_size))

    train_loader = DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )
    val_loader = DataLoader(
        val_data,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )

    return train_loader, val_loader, train_data.classes


def build_model(num_classes: int = 2, pretrained: bool = True) -> nn.Module:
    model = models.resnet18(pretrained=pretrained)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


def save_model(model: nn.Module, model_path: str) -> None:
    model_dir = os.path.dirname(model_path)
    if model_dir:
        os.makedirs(model_dir, exist_ok=True)
    torch.save(model.state_dict(), model_path)


def load_model(
    model_path: str,
    num_classes: int = 2,
    device: Optional[torch.device] = None,
) -> nn.Module:
    if device is None:
        device = get_device()

    model = build_model(num_classes=num_classes, pretrained=False)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model


def predict_image(
    model: nn.Module,
    img_path: str,
    class_names: List[str],
    device: Optional[torch.device] = None,
    image_size: int = 224,
) -> str:
    if device is None:
        device = get_device()

    image = Image.open(img_path).convert("RGB")
    image = get_eval_transform(image_size)(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    return class_names[predicted.item()]
