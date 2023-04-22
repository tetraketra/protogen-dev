from PIL import Image
import numpy as np
import  os

with open("images.h", "w") as images_gifs:
    images_gifs.write("#include <stdint.h>\n\n")

    images = [file for file in os.listdir("./images/") if file.endswith(".bmp")]
    
    for image in images:
        image_name = image[:-4].replace("-","_")
        data = np.array(Image.open(f"./images/{image}"))

        rep = f"uint8_t {image_name}[{data.size}] = {{"
        for byte in bytes(data):
            rep += f"{str(byte)},"
        rep += "};\n"

        images_gifs.write(rep)
