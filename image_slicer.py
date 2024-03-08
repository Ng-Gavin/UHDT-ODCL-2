from PIL import Image
import os

def cut_images(folder_path, output_folder, tile_size=(320, 320)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(folder_path, filename)
            with Image.open(image_path) as img:
                for i in range(0, img.width, tile_size[0]):
                    for j in range(0, img.height, tile_size[1]):
                        # Ensure the crop does not exceed the image dimensions
                        box = (i, j, min(i + tile_size[0], img.width), min(j + tile_size[1], img.height))
                        cut_image = img.crop(box)

                        # Save only if the cropped image has the full 320x320 pixels
                        if cut_image.size == tile_size:
                            cut_image.save(os.path.join(output_folder, f'{filename[:-4]}_{i}_{j}.png'))


# Example usage
cut_images('background_original', 'backgrounds')
