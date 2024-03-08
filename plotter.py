# Test code for the addTextWithPillow function

import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math

# The addTextWithPillow function as defined previously

def addTextWithPillow(main_cv2_img, text, font_path, centroid, font_size, angle, scale_factor=1.0):
    # Convert the cv2 image to a PIL image
    main_img = Image.fromarray(cv2.cvtColor(main_cv2_img, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(main_img)
    font = ImageFont.truetype(font_path, int(font_size * scale_factor))

    # Get text width and height using the specified methods
    text_width = int(draw.textlength(text, font=font))
    text_height = int(font.getmask(text).getbbox()[3])

    # Calculate the dimensions of the image needed to accommodate the rotated text
    diagonal = int(math.sqrt(text_width ** 2 + text_height ** 2) * 1.5)  # Increase canvas size
    text_img = Image.new('RGBA', (diagonal, diagonal), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)

    # Draw the text onto the text image, centered
    text_draw.text((diagonal // 2 - text_width // 2, diagonal // 2 - text_height // 2), text, font=font, fill="blue")

    # Rotate the text image
    rotated_text_img = text_img.rotate(angle, expand=1)

    # Calculate the position to paste the rotated text image
    x = int(centroid[0] - rotated_text_img.width // 2)
    y = int(centroid[1] - rotated_text_img.height // 2)
    text_position = (x, y)

    # Paste the rotated text image onto the main image
    main_img.paste(rotated_text_img, text_position, rotated_text_img.split()[3])

    # Convert the PIL image back to a cv2 image
    cv2_image = np.array(main_img)
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)

    return cv2_image

# Create a sample main image using cv2
cv2_img = np.zeros((600, 800, 3), dtype=np.uint8)

# Define font path (ensure this path is correct for your system)
font_path = "calibrib.ttf"

# Call the function with sample text, font, position, etc.
result_cv2_image = addTextWithPillow(cv2_img, "Sample Text", font_path, (400, 300), 40, 45)

# Display the result using cv2
cv2.imshow('Result Image', result_cv2_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

