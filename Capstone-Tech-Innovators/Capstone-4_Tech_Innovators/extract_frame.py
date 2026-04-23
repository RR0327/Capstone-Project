import cv2 
import os

video_folder = "Momo_Hut/"
output_folder = "momo_hut_frames/"

os.makedirs(output_folder, exist_ok=True)

for video_file in os.listdir(video_folder):
    video_path = os.path.join(video_folder, video_file)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Save every 5th frame
        if frame_count % 5 == 0:
            frame_name = f"{video_file}_{frame_count}.jpg"
            cv2.imwrite(os.path.join(output_folder, frame_name), frame)

        frame_count += 1

    cap.release()

print("Frame extraction completed!")