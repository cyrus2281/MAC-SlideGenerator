from PIL import Image
import os

def resize_image(size, image_path, output_path):
    try:
        if not output_path:
            # Overwrite the initial image if not given an output path
            output_path = image_path
        # Open the image file
        image = Image.open(image_path)
        # Resize the image
        resized_image = image.resize(size)
        # write to given file 
        resized_image.save(output_path)
    except Exception as e:
        print(f"Error resizing image: {str(e)}")
        
def resize_directory_images(size, input_directory, output_directory):
    try:
        if not output_directory:
            # Overwrite the initial image if not given an output path
            output_directory = input_directory
        # Create the output directory if it does not exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        directory_items = os.listdir(input_directory)
        # Iterate over each file in the input directory
        for file_name in directory_items:
            # Check if the file is an image
            if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
                # Get the full path of the input image
                input_image_path = os.path.join(input_directory, file_name)
                # Get the full path of the output image
                output_image_path = os.path.join(output_directory, file_name)
                # Resize the image
                resize_image(size, input_image_path, output_image_path)
    except Exception as e:
        print(f"Error resizing images: {str(e)}")