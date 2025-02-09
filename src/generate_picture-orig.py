import argparse
import random
import shutil
import subprocess
import os
import json
from PIL import Image, PngImagePlugin

def usage():
    print("Usage: python3 generate_picture.py output_dir")
    exit(1)

def generate_prompt(path: str, filename: str):
    prompts = []
    with open(f"{path}/src/{filename}") as file:
        prompts = json.load(file)

    #Extract the lists from prompt.json
    animals, items, art_styles = prompts

    #select a random entry from each list
    animal = random.choice(animals)
    item = random.choice(items)
    art_style = random.choice(art_styles)

    #generate the prompt statement
    prompt_statement = f"{animal} wearing {item} {art_style}"

    return prompt_statement

def add_metadata(image_path: str, prompt: str, seed: int):
    image = Image.open(image_path)

    #Add prompt to metadata
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text = "f{prompt}"
    metadata.add_text = "f{seed}"

    #Save the updated image
    image.save(image_path, pnginfo = metadata)

parser = argparse.ArgumentParser(description="Generate a new random picture.")
parser.add_argument("output_dir", help="Directory to save the output images")
args = parser.parse_args()

# Set the paths
installed_dir = "/home/skalahar/PicturePi"
#installed_dir = "./"
sd_bin = f"{installed_dir}/OnnxStream/src/build/sd"
sd_model = f"{installed_dir}/models/"

output_dir = args.output_dir
shared_file = 'output.png'

steps = 5
seed = random.randint(1, 10000)

# Define Prompt
prompt = generate_prompt(installed_dir, "prompt.json")

# Create a unique argument for the filename
unique_arg = f"{prompt.replace(' ', '_')}_seed_{seed}"
fullpath = os.path.join(output_dir, f"{unique_arg}.png")

# Construct the command
cmd = [
    sd_bin,
    "--turbo",
    "--models-path", sd_model,
    "--rpi-lowmem",
    "--prompt", f"{prompt}",
    "--seed", str(seed),
    "--output", fullpath,
    "--steps", str(steps),
    "--res","800x480"
]

# Run the command
print(f"Creating image with prompt: '{prompt}'")
print(f"Using seed {seed}")
print(f"Saving to {fullpath}")
print(f"Running command:\n{cmd}")
subprocess.run(cmd)
print("Command executed successfully.")

add_metadata(fullpath, prompt, seed)
print("Added Metadata.")

shared_fullpath = os.path.join(output_dir, shared_file)

shutil.copyfile(fullpath, shared_fullpath)
print(f"Copied to {shared_fullpath}")
