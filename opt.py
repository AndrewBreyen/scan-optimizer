from PIL import Image, ImageEnhance, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tkinter as tk
from tkinter import filedialog
import os

def optimize_image(image_path, output_path):
    """
    Optimize an image by converting it to grayscale, enhancing contrast and brightness,
    applying a median filter to reduce noise, and applying a threshold to create a binary image.
    Save the optimized image to the specified output path.
    """
    # Open the image
    img = Image.open(image_path)

    # Convert to grayscale
    img = img.convert('L')

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)

    # Enhance brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)

    # Apply a median filter to reduce noise and smooth out texture
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # Apply a threshold to create a binary image (black and white)
    threshold = 128
    img = img.point(lambda p: p > threshold and 255)

    # Save optimized image
    img.save(output_path)

def convert_to_pdf(image_paths, pdf_path):
    """
    Create a PDF from the specified image paths.
    """
    # Create a PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Iterate over the image paths and add each image to the PDF
    for i, image_path in enumerate(image_paths):
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        optimized_image_path = f"{base_name}_optimized.jpg"
        optimize_image(image_path, optimized_image_path)
        c.drawImage(optimized_image_path, 0, 0, width=letter[0], height=letter[1],
                    preserveAspectRatio=True, anchor='n')
        os.remove(optimized_image_path)

        # Add a new page for the next image
        if i < len(image_paths) - 1:
            c.showPage()

    # Check if the output file already exists
    if os.path.exists(pdf_path):
        # Prompt the user to confirm if they want to overwrite the file
        response = input(f"File '{pdf_path}' already exists. Overwrite? (y/n) ")
        if response.lower() != 'y':
            print('Quitting...')
            exit()

    # Save the PDF
    c.save()

# Ask user for input images
root = tk.Tk() 
root.withdraw()  # Hide the root window

# Ask for files -- one or more images
print("Select one or more images to optimize and convert to PDF:")
input_image_paths = filedialog.askopenfilenames()

# Set output PDF path
if len(input_image_paths) == 1:
    output_pdf_path = os.path.splitext(input_image_paths[0])[0] + '.pdf'
else:
    output_pdf_path = os.path.splitext(input_image_paths[0])[0] + '_combined.pdf'

print(f"Optimizing and converting {len(input_image_paths)} images to PDF...")
# Optimize the images and convert to PDF
convert_to_pdf(input_image_paths, output_pdf_path)
print("Done!")