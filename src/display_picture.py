# display_image.py
#   Intelligently crop and scale supplied image
#   and then display on e-ink display.

import argparse
import cv2
from inky.auto import auto
import numpy as np
from PIL import Image

def load_image(image_path):
    return cv2.imread(image_path)

def save_image(image_path, image):
    cv2.imwrite(image_path, image)

def display(inky, image, saturation=1.0):
    if image.shape[0] > image.shape[1]:
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    inky.set_image(Image.fromarray(image), saturation=saturation)
    inky.show()


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("image", 
        help="input image")
    ap.add_argument("-o", "--output", default="",
        help="name to save cropped display image if provided")
    ap.add_argument("-p", "--portrait", action="store_true",
                    default=False, help="Portrait orientation")
    ap.add_argument("-c", "--centre_crop", action="store_true",
                    default=False, help="Simple centre cropping")
    ap.add_argument("-r", "--resize_only", action="store_true",
                    default=False, help="Simply resize image to display ignoring aspect ratio")
    ap.add_argument("-s", "--simulate_display", action="store_true",
                    default=False, help="Do not interact with e-paper display")
    args = vars(ap.parse_args())

    simulate_display = args["simulate_display"]

    if simulate_display:
        disp_w, disp_h = (800, 480)
    else:
        inky = auto(ask_user=True, verbose=True)
        disp_w, disp_h = inky.resolution

    if args["portrait"]:
        disp_w, disp_h = disp_h, disp_w
    
    image = load_image(args["image"])

    if not simulate_display:
        display(inky, image)

    if args["output"]:
        save_image(args["output"], image)


