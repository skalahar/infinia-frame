import argparse
import random
import shutil
import subprocess
import os
import json
from PIL import Image, PngImagePlugin

def usage():
    """Displays usage instructions and exits the script."""
    print("Usage: python3 generate_picture.py output_dir")
    exit(1)

def generate_prompt(path: str, filename: str):
    """Generates a random prompt from a JSON file."""
    try:
        with open(os.path.join(path, "src", filename), 'r') as file:
            prompts = json.load(file)

        # Extract the prompt and lists from prompt.json
        prompt = prompts["prompt"]
        categories = prompts["categories"]

        # Generate a dictionary with random selections for each category
        selected_values = {key: random.choice(values) for key, values in categories.items()}

        prompt_statement = prompt

        for key, value in selected_values.items():
            prompt_statement = prompt_statement.replace(f"[{key}]", value)

        # Generate the prompt statement
        return prompt_statement

    except Exception as e:
        print(f"Error reading prompt file: {e}")
        exit(1)

def add_metadata(image_path: str, prompt: str, seed: int):
    """Adds metadata to a PNG image."""
    try:
        image = Image.open(image_path)

        # Add prompt and seed as metadata
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Prompt", prompt)
        metadata.add_text("Seed", str(seed))

        # Save the updated image
        image.save(image_path, pnginfo=metadata)
        print("Metadata added successfully.")
    except Exception as e:
        print(f"Error adding metadata: {e}")
        exit(1)

# Set the paths
file_dir = os.path.dirname(__file__)
installed_dir = os.path.dirname(file_dir)
sd_bin = os.path.join(installed_dir, "OnnxStream/src/build/sd")
sd_model = os.path.join(installed_dir, "models/")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate a new random picture.")
parser.add_argument("output_dir", help="Directory to save the output images")
args = parser.parse_args()

output_dir = args.output_dir
shared_file = "output.png"

# Define parameters
steps = 2
seed = random.randint(1, 10000)

# Generate a random prompt
prompt = generate_prompt(installed_dir, "prompt.json")
prompt = prompt.lower() #Ensure the prompt is in lower case

# Create a unique filename
unique_arg = f"{prompt.replace(' ', '_')}_seed_{seed}"
fullpath = os.path.join(output_dir, f"{unique_arg}.png")

# Construct the command
cmd = [
    sd_bin,
    "--turbo",
    "--models-path", sd_model,
    "--rpi-lowmem",
    "--prompt", prompt,
    "--seed", str(seed),
    "--output", fullpath,
    "--steps", str(steps),
    "--res", "800x480"
]

# Run the command
print(f"Creating image with prompt: '{prompt}'")
print(f"Using seed {seed}")
print(f"Saving to {fullpath}")
print(f"Running command:\n{' '.join(cmd)}")
try:
    subprocess.run(cmd, check=True)
    print("Command executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    exit(1)

# Add metadata to the image
add_metadata(fullpath, prompt, seed)

# Copy the output file to a shared file
shared_fullpath = os.path.join(output_dir, shared_file)
try:
    shutil.copyfile(fullpath, shared_fullpath)
    print(f"Copied to {shared_fullpath}")
except Exception as e:
    print(f"Error copying file: {e}")
    exit(1)
