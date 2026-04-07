"""import cv2
import os

video_path = "videos/robbery.mp4"
output_folder = "frames"

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if count % 10 == 0:  # save every 10th frame
        cv2.imwrite(f"{output_folder}/frame_{count}.jpg", frame)

    count += 1

cap.release()
"""

# updated version to process multiple videos in the folder

import cv2
import os

video_folder = "videos"
output_folder = "frames"

os.makedirs(output_folder, exist_ok=True)

for video_file in os.listdir(video_folder):

    video_path = os.path.join(video_folder, video_file)

    cap = cv2.VideoCapture(video_path)

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Save every 15th frame
        if frame_count % 15 == 0:
            frame_name = f"{video_file}_{frame_count}.jpg"
            cv2.imwrite(os.path.join(output_folder, frame_name), frame)

        frame_count += 1

    cap.release()

print("Frame extraction completed!")
