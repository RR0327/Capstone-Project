import os
import random
import shutil

source = "dataset/train/other"
val_folder = "dataset/val/other"

os.makedirs(val_folder, exist_ok=True)

files = os.listdir(source)

random.shuffle(files)

split = int(0.2 * len(files))

for file in files[:split]:
    shutil.move(os.path.join(source, file), os.path.join(val_folder, file))

print("Other dataset split complete.")
