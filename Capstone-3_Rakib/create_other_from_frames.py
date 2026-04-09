import os
import shutil
import random

source = "frames"

train_other = "dataset/train/other"
val_other = "dataset/val/other"

os.makedirs(train_other, exist_ok=True)
os.makedirs(val_other, exist_ok=True)

images = os.listdir(source)

random.shuffle(images)

split = int(0.8 * len(images))

train_imgs = images[:split]
val_imgs = images[split:]

for img in train_imgs:
    shutil.copy(os.path.join(source, img), os.path.join(train_other, img))

for img in val_imgs:
    shutil.copy(os.path.join(source, img), os.path.join(val_other, img))

print("Other dataset created from frames.")
