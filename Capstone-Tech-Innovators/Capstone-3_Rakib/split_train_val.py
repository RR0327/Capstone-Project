import os
import shutil
import random

SOURCE = "dataset_small/train"
VAL = "dataset_small/val"

CLASSES = ["human", "other"]
SPLIT = 0.2  # 20% for validation

for cls in CLASSES:
    src_folder = os.path.join(SOURCE, cls)
    val_folder = os.path.join(VAL, cls)

    os.makedirs(val_folder, exist_ok=True)

    images = os.listdir(src_folder)
    random.shuffle(images)

    split_index = int(len(images) * SPLIT)
    val_images = images[:split_index]

    for img in val_images:
        src_path = os.path.join(src_folder, img)
        dst_path = os.path.join(val_folder, img)

        shutil.move(src_path, dst_path)

    print(f"{cls}: {len(val_images)} moved to validation")

print("Train/Val split complete!")
