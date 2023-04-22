# SETUP =======================================================================
from PIL import Image
import numpy as np
import os
from collections import defaultdict



# NOTES =======================================================================
# Each .bmp file in ./images/ gets converted into a hardcoded byte-array in a C
# header file. The naming scheme is animation_framesToUseThis. So for ('A_1', '
# A_2-423'), animation A gets stored as one reference to A_1, then 422 referenc
# es to A_2. Animations cannot currently be paused. If you want to wait, repeat
# a frame as much as needed. 



# SCRIPT ======================================================================
header_file = open("images_animations.h", "w")
header_file.write("#include <stdint.h>\n\n") 

# FILES
images = [file for file in os.listdir("./images/") if file.endswith(".bmp")] # list of image files

# BYTE ARRAYS
for image in images:
    image_name = image[:-4].replace("-","_")
    data = np.array(Image.open(f"./images/{image}"))

    line = f"uint8_t {image_name}[{data.size}] = {{"
    for byte in bytes(data):
        line += f"{str(byte)},"
    line += "};\n"

    header_file.write(line)

header_file.write("\n")

# ANIMATIONS
animations = [image.split("_") for image in images] # like ("example", "1.bmp")
animations = [(image[0], image[1][:-4].replace("-","_")) for image in animations] # like ("example", "1")
animations = sorted(animations, key = lambda x: (x[0], x[1]))

d = defaultdict(list)
for k, *v in animations:
    d[k].append(*v)
animations = dict(d)

for anim_name in animations.keys():
    line = f"uint8_t* ANIMATION_{anim_name.upper()}[X__ABC__X] = {{"

    animation_length = 0
    anim_frame_codes = animations[anim_name]
    for frame_code in anim_frame_codes:

        if len(frame_code) == 1: # momnetary frame
            line += f"{anim_name}_{frame_code},"
            animation_length += 1
        else: # frame that gets played multiple refreshes in a row
            repeats = [*map(int, frame_code.split("_"))] # like [2, 9]
            repeats = range(repeats[0], repeats[1] + 1) # like [2, 3, ..., 8, 9]
            for _ in repeats:
                line += f"{anim_name}_{frame_code},"
                animation_length += 1

    line = line.replace("X__ABC__X", str(animation_length))
    line += "}\n"
    header_file.write(line)
    


# CLEANUP =====================================================================
header_file.close()

