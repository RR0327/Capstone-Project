import os

folder = "frames"

files = os.listdir(folder)

count = 0

for file in files:

    old_path = os.path.join(folder, file)

    if os.path.isfile(old_path):

        new_name = f"frame_{count}.jpg"
        new_path = os.path.join(folder, new_name)

        os.rename(old_path, new_path)

        count += 1

print("Renaming completed.")
