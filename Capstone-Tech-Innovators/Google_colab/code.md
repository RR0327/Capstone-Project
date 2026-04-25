### Install and Import the needed library

!pip install ultralytics -q

import os
import zipfile
import shutil
import random
from pathlib import Path

import torch
from google.colab import drive
from ultralytics import YOLO

### Mounting the drive with google colab

drive.mount("/content/drive")

Configuration of the file AND folder

ZIP_PATH = "/content/drive/MyDrive/Roboflow/Suspicious Detection.yolov8.zip"

LOCAL_ZIP = "/content/dataset.zip"
DATASET_ROOT = Path("/content/Suspicious_dataset")

DRIVE_PROJECT_DIR = "/content/drive/MyDrive/Roboflow/run_detection"
RUN_NAME = "Suspicious_detection"

EPOCHS = 15
IMGSZ = 640
BATCH = 8
WORKERS = 2
PATIENCE = 10

CLASS_NAMES = {
0: "gun",
1: "knife",
2: "NonViolence",
3: "sword",
4: "Sword",
5: "Violance"
}

Checking GPU

if torch.cuda.is_available():
DEVICE = 0
print("GPU found:", torch.cuda.get_device_name(0))
else:
DEVICE = "cpu"
print("GPU not found. Training will run on CPU.")

Copy with Unzip dataset

if not os.path.exists(ZIP_PATH):
raise FileNotFoundError(f"ZIP not found: {ZIP_PATH}")

if DATASET_ROOT.exists():
shutil.rmtree(DATASET_ROOT)

DATASET_ROOT.mkdir(parents=True, exist_ok=True)

print("Copying zip...")
shutil.copy2(ZIP_PATH, LOCAL_ZIP)

print("Unzipping...")
with zipfile.ZipFile(LOCAL_ZIP, "r") as z:
z.extractall(DATASET_ROOT)

print("Unzip done.")

Checking the dataset structure

for root, dirs, files in os.walk(DATASET_ROOT):
level = root.replace(str(DATASET_ROOT), "").count(os.sep)
if level <= 2:
print(" " \* level + os.path.basename(root) + "/")

create the Valid split from Train

train_img_dir = DATASET_ROOT / "train" / "images"
train_lbl_dir = DATASET_ROOT / "train" / "labels"

valid_img_dir = DATASET_ROOT / "valid" / "images"
valid_lbl_dir = DATASET_ROOT / "valid" / "labels"

if not train_img_dir.exists():
raise FileNotFoundError("train/images folder not found.")

if not train_lbl_dir.exists():
raise FileNotFoundError("train/labels folder not found.")

valid_img_dir.mkdir(parents=True, exist_ok=True)
valid_lbl_dir.mkdir(parents=True, exist_ok=True)

image_exts = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]

images = []
for ext in image_exts:
images.extend(train_img_dir.glob(f"\*{ext}"))

print("Total train images before split:", len(images))

if len(images) == 0:
raise ValueError("No images found in train/images.")

random.seed(42)
random.shuffle(images)

val_ratio = 0.2
val_count = max(1, int(len(images) \* val_ratio))

val_images = images[:val_count]

for img_path in val_images:
label_path = train_lbl_dir / f"{img_path.stem}.txt"

    shutil.move(str(img_path), str(valid_img_dir / img_path.name))

    if label_path.exists():
        shutil.move(str(label_path), str(valid_lbl_dir / label_path.name))

print("Validation split created.")
print("Train images:", len(list(train*img_dir.glob("*._"))))
print("Valid images:", len(list(valid_img_dir.glob("_.\_"))))

Fix data.yml

DATA_YAML = DATASET_ROOT / "data.yaml"

content = """train: train/images
val: valid/images

names:
0: gun
1: knife
2: NonViolence
3: sword
4: Sword
5: Violance
"""

DATA_YAML.write_text(content)

print("Final data.yaml:")
print(DATA_YAML.read_text())

Checxk Label Format

sample_labels = list((DATASET_ROOT / "train" / "labels").glob("\*.txt"))[:10]

if len(sample_labels) == 0:
raise ValueError("No label files found.")

for label in sample_labels:
with open(label, "r", encoding="utf-8") as f:
lines = [x.strip() for x in f.readlines() if x.strip()]

    if lines:
        value_count = len(lines[0].split())
        print("Sample label:", label.name)
        print("Value count:", value_count)
        print("Example line:", lines[0])

        if value_count == 5:
            print("Format OK: Normal YOLO detection.")
        elif value_count == 9:
            print("This is OBB format. Use yolov8n-obb.pt instead.")
        else:
            print("Unknown label format.")
        break

Train YOLOv8

os.makedirs(DRIVE_PROJECT_DIR, exist_ok=True)

model = YOLO("yolov8n.pt")

model.train(
data=str(DATA_YAML),
epochs=EPOCHS,
imgsz=IMGSZ,
batch=BATCH,
device=DEVICE,
workers=WORKERS,
project=DRIVE_PROJECT_DIR,
name=RUN_NAME,
patience=PATIENCE,
cache=False,
amp=True,
save=True,
verbose=True,
exist_ok=True
)

Validate Best Model

best_ckpt = Path(DRIVE_PROJECT_DIR) / RUN_NAME / "weights" / "best.pt"

if best_ckpt.exists():
best_model = YOLO(str(best_ckpt))
metrics = best_model.val(data=str(DATA_YAML))
print("Validation complete.")
else:
print("best.pt not found.")

Test prediction

best_ckpt = Path(DRIVE_PROJECT_DIR) / RUN_NAME / "weights" / "best.pt"
best_model = YOLO(str(best_ckpt))

test*images = list((DATASET_ROOT / "valid" / "images").glob("*.\_"))

if len(test_images) == 0:
raise ValueError("No validation images found.")

sample_img = str(test_images[0])

results = best_model.predict(
source=sample_img,
conf=0.25,
save=True
)

print("Prediction done.")
print("Sample image:", sample_img)

Show result Folder

print("Training result folder:")
print(Path(DRIVE_PROJECT_DIR) / RUN_NAME)

print("Best model:")
print(Path(DRIVE_PROJECT_DIR) / RUN_NAME / "weights" / "best.pt")
