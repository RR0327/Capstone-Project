import os
import random
import shutil

source_dir = "dataset"
train_human = "dataset/train/human"
val_human = "dataset/val/human"

os.makedirs(train_human, exist_ok=True)
os.makedirs(val_human, exist_ok=True)

images = []

for folder in os.listdir(source_dir):

    path = os.path.join(source_dir, folder)

    if os.path.isdir(path) and folder not in ["train", "val"]:
        for img in os.listdir(path):
            images.append(os.path.join(path, img))

random.shuffle(images)

split = int(0.8 * len(images))

train_imgs = images[:split]
val_imgs = images[split:]

for img in train_imgs:
    shutil.copy(img, train_human)

for img in val_imgs:
    shutil.copy(img, val_human)

print("Dataset split completed.")
