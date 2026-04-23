import os
import cv2
from PIL import Image
import imagehash

input_folder = "momo_hut_frames/"
output_folder = "clean_data/momo_hut_normal/"

os.makedirs(output_folder, exist_ok=True)

hashes = set()

blur_threshold = 100

for file in os.listdir(input_folder):

    path = os.path.join(input_folder, file)

    try:
        # --- Duplicate detection ---
        img = Image.open(path)
        img_hash = imagehash.average_hash(img)

        if img_hash in hashes:
            continue

        hashes.add(img_hash)

        # --- Blur detection ---
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        if laplacian_var < blur_threshold:
            continue

        # --- Save clean image ---
        cv2.imwrite(os.path.join(output_folder, file), image)

    except:
        continue

print("Dataset cleaning completed.")