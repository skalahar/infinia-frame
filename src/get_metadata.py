import sys
from PIL import Image
from PIL.ExifTags import TAGS

def get_image_metadata(image_path):
    try:
        # Open the image
        img = Image.open(image_path)

        # Display image format and size
        print(f"Image Format: {img.format}")
        print(f"Image Size: {img.size} (Width x Height)")
        print(f"Color Mode: {img.mode}")

        # Extract metadata
        metadata = img.info  # Metadata dictionary for PNG

        print("\nMetadata:")
        if metadata:
            for key, value in metadata.items():
                print(f"{key}: {value}")
        else:
            print("No metadata found.")

        # Extract EXIF data if available (PNG usually doesn't store EXIF)
        exif_data = img.getexif()
        if exif_data and len(exif_data.keys()) > 0:
            print("\nEXIF Data:")
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                print(f"{tag_name}: {value}")
        else:
            print("\nNo EXIF Data found.")

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"Error: {e}")

# Main function to handle command-line argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_metadata.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    get_image_metadata(image_path)
