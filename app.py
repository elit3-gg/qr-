import os
from PIL import Image, ImageDraw, ImageFont
import math
import re

# Constants for A3 paper size in pixels at 300 DPI
A3_WIDTH = int(11.7 * 300)  # 297 mm width in inches at 300 DPI
A3_HEIGHT = int(16.5 * 300)  # 420 mm height in inches at 300 DPI

# Define the size of each QR code in pixels
DPI = 300
QR_SIZE_INCHES = 2.0  # 2 inches
QR_SIZE_PIXELS = int(QR_SIZE_INCHES * DPI)

# Define the number of columns
NUM_COLUMNS = 5  # Adjusted number of columns to fit the A3 page

def extract_number(filename):
    # Extract the first number found in the filename
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

def create_qr_collage_with_names(input_folder, output_image):
    # Get all image paths from the folder
    qr_image_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not qr_image_paths:
        print("No QR code images found in the folder.")
        return

    # Sort image paths by the numeric part of the filename
    qr_image_paths.sort(key=lambda path: extract_number(os.path.basename(path)))

    # Calculate the number of rows needed
    num_images = len(qr_image_paths)
    num_rows = math.ceil(num_images / NUM_COLUMNS)

    # Create a blank A3 image
    collage = Image.new('RGB', (A3_WIDTH, A3_HEIGHT), color='white')

    # Font for names (ensure the font file is available in your system)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Calculate spacing
    spacing_x = (A3_WIDTH - (NUM_COLUMNS * QR_SIZE_PIXELS)) // (NUM_COLUMNS + 1)
    spacing_y = (A3_HEIGHT - (num_rows * QR_SIZE_PIXELS)) // (num_rows + 1)

    # Draw object for adding text to the collage
    draw = ImageDraw.Draw(collage)

    # Resize QR codes and paste them into the collage
    for idx, qr_path in enumerate(qr_image_paths):
        qr_img = Image.open(qr_path).resize((QR_SIZE_PIXELS, QR_SIZE_PIXELS), Image.LANCZOS)

        # Calculate position
        row = idx // NUM_COLUMNS
        col = idx % NUM_COLUMNS
        x = spacing_x + col * (QR_SIZE_PIXELS + spacing_x)
        y = spacing_y + row * (QR_SIZE_PIXELS + spacing_y)

        # Paste the QR image
        collage.paste(qr_img, (x, y))

        # Extract the name from the filename and add text below the QR code
        file_name = os.path.basename(qr_path).split('_QR')[0]  # Extract {Name}
        text_bbox = font.getbbox(file_name)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (QR_SIZE_PIXELS // 2) - (text_width // 2)
        text_y = y + QR_SIZE_PIXELS + 5  # Place text just below the QR code

        draw.text((text_x, text_y), file_name, fill="black", font=font)

    # Save the collage as a high-quality PDF
    collage.save(output_image, "PDF", resolution=DPI)
    print(f"Collage saved as {output_image}")

# Example usage
input_folder = "/Users/vallerikoushik/Documents/QR-COde/qr-/Syrus_QR"  # Replace with your folder path
output_image = "Syrus_QR_2inches.pdf"
create_qr_collage_with_names(input_folder, output_image)
