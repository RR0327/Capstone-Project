import os
import shutil
import random

# Source dataset
SOURCE = "dataset/train"

# Target dataset
TARGET = "dataset_small/train"

CLASSES = ["human", "other"]

# Number of images per class
LIMIT = 500  # total = 1000 images

for cls in CLASSES:
    src_folder = os.path.join(SOURCE, cls)
    dst_folder = os.path.join(TARGET, cls)

    os.makedirs(dst_folder, exist_ok=True)

    images = os.listdir(src_folder)
    random.shuffle(images)

    selected = images[:LIMIT]

    for img in selected:
        src_path = os.path.join(src_folder, img)
        dst_path = os.path.join(dst_folder, img)

        try:
            shutil.copy(src_path, dst_path)
        except:
            pass

    print(f"{cls}: {len(selected)} images copied")

print("Small dataset created successfully!")
