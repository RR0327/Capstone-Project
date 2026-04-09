> Needed python version is py 3.11.x

- create virtual environment (venv)
- install libraries
- write scripts for dataset collection
- run crawler scripts

> currently installed:

- icrawler → for downloading images

- yt-dlp → for downloading YouTube videos

- OpenCV → for extracting frames from videos

> 1. Why VS Code Shows Import Errors

```bash
Import "cv2" could not be resolved
Import "icrawler.builtin" could not be resolved
Import "yt_dlp" could not be resolved
```

> 2. What Your Terminal Output Means

```bash
start crawling...
parsing result page https://www.google.com/search?q=CCTV+suspicious+activity
```

This means:

- crawler started
- it contacted Google
- it tried to parse image results

But then you got:

    TypeError: 'NoneType' object is not iterable

> Why the Crawler Failed

This is not your fault.

Google recently changed their HTML structure.

So `icrawler` sometimes fails to parse Google results.

This is a known issue.

> 3. What Your Terminal Output Means

This line shows the script started searching YouTube using `yt-dlp`:

    [youtube:search] Extracting URL: ytsearch10:shop robbery CCTV

Meaning:

    Search YouTube → "shop robbery CCTV"
    Download top 10 videos

Then each video is downloaded:

    Destination: videos\CCTV of store robbery.mp4
    100% downloaded

So your script successfully downloaded multiple CCTV robbery videos.

> 4. About This Warning

You saw:

    WARNING: No supported JavaScript runtime could be found

This is not an error.

It only means:

    yt-dlp cannot run JavaScript engine

But your videos still downloaded successfully, so you can ignore this warning.

> 5. Why This Error Happened

At the end you saw:

    ERROR: This video is not available

This happens when:

- video deleted

- video private

- region blocked

This is very normal when downloading from YouTube.

Your script stopped because yt-dlp stops on errors by default.

> 6. What Those Warnings Mean

Example warning:

```bash
cv::findDecoder imread_('frames\├»┬╝ΓÇÜTop 5 BEST Security Cameras...
can't open/read file: check file path/integrity
```

This happens because:

Some frame filenames contain special Unicode characters like:

```bash

├»┬╝
ΓÇÜ
├óΓé¼ΓÇ£
```

These came from YouTube video titles when frames were extracted.

Example original video title:

```bash
Top 5 BEST Security Cameras (2026) – NO Monthly Fees & 2K Night Vision!
```

When converted to filenames → encoding breaks.

So `OpenCV` cannot read those files properly.

> 7. Train process being slow

Example:

This:
KeyboardInterrupt

Means:

When I manually stopped the training (Ctrl + C)

    NOT a crash
    NOT a bug
    NOT a code issue

> 8. The error happens when the shortest version run

In the shortest version i used:

```python
num_workers=2
```

This tells PyTorch:

“Use multiple processes to load data faster”

But on Windows, multiprocessing works differently (it uses spawn, not fork).

So Python tries to re-run your whole script again inside each worker → crash.

That’s why you see:

```bash
RuntimeError: An attempt has been made to start a new process...
```
