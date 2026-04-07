> Method 1 — Download Images from Google Automatically

**Library Used**

    icrawler

> Why we use it

- Automatically downloads images from search engines

- Lets you specify keywords

- Easy to use for dataset creation

- Used by many ML researchers for quick dataset collection

**Install**

    pip install icrawler

> Method 2 — Download Videos from YouTube

**Library Used**

    yt-dlp

> Why we use it

- Downloads videos from YouTube

- Very reliable

- Faster than older libraries

**Install**

    pip install yt-dlp

> Then Extract Frames from Video

You will convert videos → images.

**Library used:**

    OpenCV

> Why we use it:

- Extract frames from CCTV videos

- Core computer vision library

- Used in almost all CV research

**Install**

    pip install opencv-python

> Libraries Summary (Important for Your Report)

| Library  | Purpose                       |
| -------- | ----------------------------- |
| icrawler | Download images automatically |
| yt-dlp   | Download YouTube videos       |
| OpenCV   | Extract frames from videos    |
| PyTorch  | Train deep learning models    |

> For CCTV research papers, datasets often reach:

```bash
100k – 500k images
```

> The trick researchers use:

```bash
YouTube videos → extract frames → auto dataset
```

1 video = 1000+ images

So 100 videos → 100k images.

> My project will likely become right now after the 1 and 2 step of `Problemface.md`

```bash
CCTV Video
↓
Frame Extraction
↓
Human Detection
↓
Suspicious Behavior Detection
```

> Current update,

```
|--images.py
|--videos.py
|--extract_frames.py
```

> My Research Dataset Pipeline [ 1,2]

- Your pipeline will now look like this:

```bash
Google Images +
YouTube CCTV Videos
↓
Download Dataset
↓
Extract Frames
↓
Image Dataset (50k–100k)
↓
Train Model
```

Later you will train using `PyTorch`.

> research dataset pipeline [3, 4, 5]

```bash
Google Images
     ↓
images.py
     ↓
Image Dataset
     ↓
YouTube CCTV videos
     ↓
videos.py
     ↓
CCTV Video Dataset
```

> The next step is very important for your research:

- You must convert the videos into images (frames) so they can be used for training your computer vision model.

- Your ML model (using `PyTorch`) will train on images, not videos.

- To extract frames we use `OpenCV`, which is the most common computer vision library.

> A real dataset pipeline:

```bash
images.py → image dataset
videos.py → CCTV videos
extract_frames.py → frames (images)
```

Now we will clean the dataset automatically, which is very important before training your model.

Your script will do 3 things:

1. Remove duplicate images
2. Remove blurred images
3. Keep only clear images

This improves dataset quality a lot before training with `PyTorch`.

We will use two reliable libraries:

`OpenCV` → image processing

`ImageHash` → detect duplicate images

Both are safe and widely used.

    Install Required Libraries

Run in terminal:

```bash
pip install imagehash pillow
```

You already installed `OpenCV`, so no need to reinstall.

> What the Script Does

**Duplicate Removal**

Using `ImageHash`

Example:

frame_100.jpg
frame_101.jpg
frame_102.jpg

If they look **identical → duplicates are removed.**

**Blur Detection**

Using `OpenCV`

_Blurry frames_ like:

- motion blur
- camera shake
- low focus

will be removed automatically.

> A real research dataset pipeline:

```bash
YouTube CCTV videos
↓
videos.py
↓
extract_frames.py
↓
frames
↓
clean_dataset.py
↓
clean_frames (final dataset)
↓
Model training
```

> The next stage will be:

    Human Detection Model

Using `YOLOv8`.

This will:

- detect humans

- ignore animals / objects

- prepare your human vs other dataset

which directly supports your research topic.

> Current Research Pipeline

```bash
YouTube CCTV videos
        ↓
yt-dlp downloader
        ↓
videos
        ↓
frame extraction
        ↓
frames
        ↓
dataset cleaning
        ↓
clean_frames
```

> Next REAL Research Step

Now we should start building the Human vs Other classifier for your topic:

The next model will use:

- PyTorch

- TorchVision

- ResNet18

to classify:

```bash
Human
vs
Other (animal / object)
```

This directly supports your suspicious behavior detection pipeline.

> Goal of this model:

```bash
Input Image → Model → Prediction
↓
Human / Other
```

We will use:

- `PyTorch` → deep learning framework

- `TorchVision` → dataset & transforms

- `ResNet18` → lightweight CNN model

This is very good for CPU training, which matches your setup.

**Libraries:**

     pip install torch torchvision matplotlib scikit-learn

> After the work of create other from frames file the pipeline looks:

```bash

YouTube CCTV Videos
        ↓
yt-dlp download
        ↓
extract_frames.py
        ↓
frames
        ↓
clean_dataset.py
        ↓
clean_frames
        ↓
dataset
   ├── human
   └── other

```

> The best way to train the model

```bash
Reduce dataset temporarily

For testing, DON’T train on 39K images.

Do this:

Modify your dataset (quick test mode)

Inside dataset:

dataset/
├── train/
│ ├── human (take 1000 images)
│ ├── other (take 1000 images)

        OR

use the shortest version of the `train_human_detector.py`

```

> Which one should YOU use?

```python
Option	                            Speed	        Recommended
num_workers=0	                    Slow	        Debug only
num_workers=2 + main() fix	    Faster	        BEST
```

- Final Insight

You didn’t mess up — you just hit:

        “Windows multiprocessing trap” (every ML engineer faces this)

> What’s happening right now?

- Currently we have ~38,934 images

- CPU training (no GPU)

- Batch size = 8 → ~4867 batches per epoch

- 5 epochs → ~24,000 iterations

        That’s why it’s taking very long

> For better my Idea is: Train on 1K images first

which is 100% the correct move.

> Why this is smart:

- Faster debugging

- Catch errors early
- Test pipeline (dataset → model → training)

- Iterate quickly

        Big datasets are used after everything is stable

> Best Practice (Industry Style)

- Small dataset (500–1000 images) → Debug & test

- Medium dataset (5K–10K) → Tune model

- Full dataset (30K+) → Final training

> Final pipeline will look like:

```bash
CCTV Video
     ↓
Frame Extraction
     ↓
Human Detection
     ↓
Behavior Classification
     ↓
Suspicious Alert
```
