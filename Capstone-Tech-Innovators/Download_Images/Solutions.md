> 1. Fixing way:

    CTRL + SHIFT + P

Then select:

    Python: Select Interpreter

Choose this interpreter:

    python venv 3.11.x

after then restart vs code.

> 2. Fixing way:

Change your code to use Bing crawler.

    Bing works much better.

Replace this

    from icrawler.builtin import GoogleImageCrawler

With this

    from icrawler.builtin import BingImageCrawler

> 3, 4, 5

Changes:

    ignoreerrors = True
    ytsearch20 instead of ytsearch10

Now it will:

    skip broken videos
    download 20 per search

Total:

    5 searches × 20 videos = ~100 videos

> 6. This Is NOT Dangerous

Nothing is wrong with:

- your PC

- your dataset

- your environment

- your `OpenCV`

- your `ImageHash`

The script simply skipped those corrupted filenames.

That is why the script still finished.

Now, we should rename all frame files to simple names.

Example:

frame_00001.jpg
frame_00002.jpg
frame_00003.jpg

This is standard practice in ML datasets.

> 7. Real Problem is training slow

You have:

```bash
~39,000 images
CPU only training
ResNet18

This combo = VERY SLOW

So what happens:

It starts loading images

Takes long time

When i think it's stuck

For that reason when i press Ctrl+C → KeyboardInterrupt

    Why it's slow (important)

Each batch:

Loads images from disk
Converts to tensor
Runs through ResNet18

On CPU → this is HEAVY
```

> 8. Explanation and solution of the shortest issue

- Explanation

Without protection:

Main script runs
→ DataLoader starts workers
→ workers re-run script
→ script starts workers again
→ infinite chaos

- Solutions provide in the train_human_detector.py file.

- shortest version issue:

```python
# everything runs immediately
train_loader = DataLoader(..., num_workers=2)

for images, labels in train_loader:
    ...

```

    Issue:

On Windows, num_workers=2 starts new processes
Those processes re-run the whole script
Script runs again → tries to spawn again → 💥 crash

- the correct version of it work due to:

```python
def main():
    # all logic inside here
    ...

if __name__ == "__main__":
    main()

```

    What this does:

- Main script runs normally

- Worker processes DO NOT execute main() `Not provide on that`

- Only the parent process runs training

- Workers only load data

  Result: No infinite spawning → no crash

- Simple analogy

Think of it like this:

Before:

    Every worker says: “Oh I’m the boss too, let me run everything again”

After:

    Only ONE boss runs training Workers just help silently.
