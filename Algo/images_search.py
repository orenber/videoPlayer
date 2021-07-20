import os
from Utility.file_location import *

images_dir = full_file([os.pardir, "Resources","images"])

print(images_dir)

for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(path)).replace(" ", ".").lower()
            print(label,path)
