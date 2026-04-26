# 1. Install and Import Libraries

```python
!pip install ultralytics -q
```

### What it means

- `pip install` → installs a Python package
- `ultralytics` → official library for YOLOv8
- `-q` → quiet mode (less output)

### Why needed

YOLOv8 is not built into Python or Colab, so you must install it first.

---

```python
import os
import zipfile
import shutil
import random
from pathlib import Path
```

### Explanation

These are **built-in Python libraries**:

- `os` → interact with file system (folders, paths)
- `zipfile` → unzip dataset
- `shutil` → copy/move files
- `random` → shuffle dataset
- `Path` → easier way to handle file paths

---

```python
import torch
from google.colab import drive
from ultralytics import YOLO
```

### Explanation

- `torch` → PyTorch (deep learning engine)
- `drive` → connect Google Drive
- `YOLO` → main class to train and run YOLOv8

---

# 2. Mount Google Drive

```python
drive.mount("/content/drive")
```

### What happens

- Connects your Google Drive to Colab
- `/content/drive` becomes your Drive folder

### Why needed

Your dataset is stored in Drive:

```
MyDrive/Roboflow/...
```

Without mounting, Colab cannot access it.

---

# 3. Configuration Section

This is where you define everything.

```python
ZIP_PATH = "/content/drive/MyDrive/Roboflow/Suspicious Detection.yolov8.zip"
```

- Location of dataset zip in Google Drive

---

```python
LOCAL_ZIP = "/content/dataset.zip"
```

- Temporary copy inside Colab

---

```python
DATASET_ROOT = Path("/content/Suspicious_dataset")
```

- Folder where dataset will be extracted

---

```python
DRIVE_PROJECT_DIR = "/content/drive/MyDrive/Roboflow/run_detection"
RUN_NAME = "Suspicious_detection"
```

- Where training results will be saved
- `RUN_NAME` → folder name of this experiment

---

```python
EPOCHS = 15
IMGSZ = 640
BATCH = 8
WORKERS = 2
PATIENCE = 10
```

### Beginner explanation

- `EPOCHS` → how many times model sees dataset
- `IMGSZ` → image size (YOLO standard: 640)
- `BATCH` → how many images processed at once
- `WORKERS` → parallel data loading threads
- `PATIENCE` → early stopping if no improvement

---

`BATCH = 8`

The batch size determines how many images the model processes at once before updating its internal weights. A batch size of 8 is relatively small, which is helpful if you have limited GPU memory (VRAM). Larger batch sizes can lead to more stable training but require more powerful hardware.

`WORKERS = 2`

This refers to the number of CPU threads or processes dedicated to loading and preprocessing the data. While the GPU handles the actual math of the neural network, the "workers" prepare the images in the background.

Having 2 workers means the CPU will try to stay two steps ahead of the GPU to ensure it never has to wait for data.

`PATIENCE = 10`

Patience is a setting for "early stopping."

If the model's performance on the validation set does not improve for 10 consecutive epochs, the training will stop automatically even if it hasn't reached the 15th epoch.

This prevents the model from overfitting and saves time.

---

```python
CLASS_NAMES = {
    0: "gun",
    1: "knife",
    2: "NonViolence",
    3: "sword",
    4: "Sword",
    5: "Violance"
}
```

### Important concept

This defines your detection classes.

But here is a problem:

- `"sword"` and `"Sword"` → duplicate meaning
- `"Violance"` → typo

This can confuse the model. You should clean it later.

---

# 4. Check GPU

```python
if torch.cuda.is_available():
```

- Checks if GPU is available

---

`torch`: Refers to the PyTorch library, a popular framework for deep learning.

`.cuda`: Refers to CUDA (Compute Unified Device Architecture), which is a platform created by NVIDIA that allows software to use the GPU for much faster mathematical processing than a standard CPU.

`.is_available()`: This function returns True if your system has an NVIDIA GPU installed and the correct drivers/CUDA toolkit are properly configured. Otherwise, it returns False.

---

```python
DEVICE = 0
```

- Use GPU (index 0)

---

```python
print("GPU found:", torch.cuda.get_device_name(0))
```

- Shows GPU name

---

```python
else:
    DEVICE = "cpu"
```

- If no GPU → use CPU (very slow)

---

# 5. Copy and Unzip Dataset

```python
if not os.path.exists(ZIP_PATH):
    raise FileNotFoundError(...)
```

- Checks if dataset exists
- If not → stop program

---

```python
if DATASET_ROOT.exists():
    shutil.rmtree(DATASET_ROOT)
```

- Deletes old dataset folder (clean start)

---

`if DATASET_ROOT.exists():`: It checks if a folder or file at the path defined by DATASET_ROOT already exists on your hard drive.

`shutil.rmtree(DATASET_ROOT)`: If the folder does exist, this command "removes the directory tree." It deletes the folder and everything inside it—all subfolders and files—permanently.

---

```python
DATASET_ROOT.mkdir(parents=True, exist_ok=True)
```

- Creates new dataset folder

---

`.mkdir()`: This command tells the system to make a new directory (folder).

`parents=True`: This is a powerful safety feature. If you are trying to create a path like data/project/images, but the data or project folders don't exist yet, this setting will automatically create all those "parent" folders in one go. Without it, the code would crash if any part of the path is missing.

`exist_ok=True`: This prevents the code from crashing if the folder already exists. Usually, trying to create a folder that is already there causes an error; with this set to True, the script simply moves on quietly.

---

```python
shutil.copy2(ZIP_PATH, LOCAL_ZIP)
```

- Copies dataset from Drive → Colab

  Why?

Colab runs faster when working locally.

---

```python
with zipfile.ZipFile(LOCAL_ZIP, "r") as z:
    z.extractall(DATASET_ROOT)
```

- Unzips dataset into folder

---

`with zipfile.ZipFile(LOCAL_ZIP, "r") as z:`: It opens the file located at LOCAL_ZIP in read mode ("r").

The with statement is a "context manager." It ensures that the zip file is properly closed as soon as the extraction is finished, which prevents memory leaks or file corruption.

`as z` creates a temporary variable (an alias) to represent that open zip file.

`z.extractall(DATASET_ROOT)`: This takes every single file and folder inside the zip archive and unzips them into the folder defined by DATASET_ROOT.

---

# 6. Check Dataset Structure

```python
for root, dirs, files in os.walk(DATASET_ROOT):
```

- Walks through all folders

---

`os.walk(DATASET_ROOT)`: This function "walks" through the directory tree. For every directory it finds (starting at your root), it yields a 3-item tuple.

`root`: A string containing the path to the current directory the loop is looking at.

`dirs`: A list of the names of the subdirectories inside the current root.

`files`: A list of the names of the non-directory files inside the current root.

---

```python
level = root.replace(...).count(os.sep)
```

- Calculates folder depth

---

`root.replace(DATASET_ROOT, "")`: This takes the full path of the current folder and removes the base path. For example, if your dataset is at data/dataset and the loop is currently in data/dataset/train/images, this operation leaves you with just /train/images.

`os.sep`: This is a built-in constant that represents the operating system's path separator (/ on Linux/Mac and \ on Windows). Using this instead of a hardcoded slash makes your code cross-platform.

`.count(...)`: This counts how many separators are in the remaining string.

---

```python
if level <= 2:
    print(...)
```

- Prints structure (only first few levels)

### Lets Visualizing the structure:

```
/dataset (Level 0)
├── train (Level 1)
│   ├── images (Level 2)
│   │   ├── img1.jpg (Level 3 - Hidden)
│   │   └── img2.jpg (Level 3 - Hidden)
│   └── labels (Level 2)
└── val (Level 1)
```

    The print command will trigger for the folders, but it won't trigger for the deep nested files or any sub-folders deeper than level 2.

This is a best practice when `handling large computer vision datasets`. Since a typical dataset might `contain 50,000+ images`, you only want to see a high-level summary (e.g., "Found the train/images folder") `rather than a printout of every single file path`.

---

# 7. Create Validation Split

```python
train_img_dir = DATASET_ROOT / "train" / "images"
```

- Path to training images

---

```python
valid_img_dir.mkdir(...)
```

- Create validation folders if not exist

---

```python
images = []
for ext in image_exts:
    images.extend(train_img_dir.glob(f"*{ext}"))
```

- Collect all images

---

```python
random.shuffle(images)
```

- Shuffle images randomly

---

```python
val_ratio = 0.2
```

- 20% data → validation

---

```python
val_images = images[:val_count]
```

- Select first 20% for validation

---

```python
shutil.move(...)
```

- Moves images + labels to validation folder

---

### Concept

- Train set → model learns
- Validation set → model is tested during training

---

# 8. Fix data.yaml

```python
DATA_YAML = DATASET_ROOT / "data.yaml"
```

- YOLO config file

---

```python
content = """train: train/images
val: valid/images
...
"""
```

- Defines dataset structure

---

```python
DATA_YAML.write_text(content)
```

- Writes config file

---

### Why important

YOLO reads this file to:

- know where images are
- know class names

---

# 9. Check Label Format

```python
sample_labels = list(... )[:10]
```

- Take first 10 label files

---

```python
lines = [x.strip() for x in f.readlines()]
```

- Read label file

---

### YOLO format

Each line:

```
class x_center y_center width height
```

Total = 5 values

---

```python
if value_count == 5:
```

- Normal YOLO detection

---

```python
elif value_count == 9:
```

- OBB (oriented bounding box)

---

### Concept

This ensures dataset is compatible with YOLOv8

---

# 10. Train YOLOv8

```python
model = YOLO("yolov8n.pt")
```

### Explanation

- Loads pretrained YOLOv8 nano model
- "n" = smallest, fastest

---

```python
model.train(...)
```

### Key parameters

- `data` → dataset config
- `epochs` → training cycles
- `imgsz` → image size
- `batch` → batch size
- `device` → GPU/CPU
- `project` → save folder
- `name` → run name
- `patience` → early stopping

---

### Concept

Training = model learns:

- detect objects
- draw bounding boxes
- classify them

---

# 11. Validate Model

```python
best_ckpt = Path(...) / "best.pt"
```

- Path to best trained model

---

```python
best_model = YOLO(str(best_ckpt))
```

- Load trained model

---

```python
metrics = best_model.val(...)
```

- Evaluate model performance

---

### Metrics include

- mAP (accuracy)
- precision
- recall

---

# 12. Test Prediction

```python
results = best_model.predict(...)
```

### What happens

- Takes one image
- Detects objects
- Draws boxes
- Saves result

---

```python
conf=0.25
```

- Confidence threshold
- Lower = more detections

---

# 13. Show Results

```python
print(Path(DRIVE_PROJECT_DIR) / RUN_NAME)
```

- Shows where results are saved

---

```python
print(... "best.pt")
```

- Shows trained model path

---

# Final Working Concept (Very Important)

Your pipeline is doing this:

1. Load dataset from Drive
2. Prepare dataset (clean + split)
3. Define classes
4. Train YOLO model
5. Validate performance
6. Test on sample image
7. Save trained model

---

# Big Picture Understanding

Think of YOLO like this:

- Input → image
- Output → boxes + labels

Example:

```
Image → [gun detected, confidence 0.92]
```

---

# Critical Observations (You Should Fix)

1. Duplicate classes
   - sword vs Sword

2. Typo
   - Violance → Violence

3. Class imbalance (likely)
   - may affect accuracy

---

# What You Should Now Understand

After this explanation, you should clearly know:

- how dataset flows
- how training works
- what each parameter controls
- how YOLO uses data.yaml
- difference between train and validation

---

Now we can go deeper.

When you're ready, tell me:
"I want to understand YOLOv8 architecture"

Then I’ll break down:

- backbone
- neck
- head
- how detection actually works internally

step by step, from zero level to research-level understanding.
