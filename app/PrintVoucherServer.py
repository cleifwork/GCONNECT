import os
import sys
import cv2
import time
import subprocess
import numpy as np
import win32com.client as win32
from PIL import Image
from tkinter import messagebox
from utils import FILE_PATHS, exe_dir

# Define the base directory path
base_dir = os.path.join(exe_dir, 'img')

def check_voucher_list():
    # Check in the root folder
    if os.path.isfile(FILE_PATHS["voucher_list"]):
        return FILE_PATHS["voucher_list"]  # Return path if found in the root folder

    # Check in the raw_csv folder
    raw_csv_path = os.path.join(FILE_PATHS["csv_folder"], "VoucherList.csv")
    if os.path.isfile(raw_csv_path):
        return raw_csv_path  # Return path if found in the raw_csv folder

    # If not found in either location, display an error and exit
    messagebox.showerror("Error", "No 'VoucherList.csv' file found! \nPlease run 'EXTRUP & SYNC' first.")
    sys.exit()


def remove_background_and_crop(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # If the image has no alpha channel, add one
    if image.shape[2] != 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a mask where white pixels are set to 0 and all others to 1
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Find contours of the non-transparent areas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize the bounding box to the full image dimensions
    x_min, y_min = image.shape[1], image.shape[0]
    x_max, y_max = 0, 0

    # Get the bounding box that encloses all non-transparent pixels
    if contours:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)

        # Apply the mask to the alpha channel of the image
        image[:, :, 3] = mask

        # Crop the image to the bounding box
        cropped_image = image[y_min:y_max, x_min:x_max]

        # Save the cropped image
        result_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGRA2RGBA))
        result_image.save(output_path)
    else:
        # Check if the image has a transparent background
        alpha_channel = image[:, :, 3]
        transparent_background = np.all(alpha_channel == 0)

        if transparent_background:
            print("Image has a transparent background.")

            # Find contours of the non-transparent areas (excluding fully transparent pixels)
            mask = alpha_channel > 0
            contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                x_min, y_min = image.shape[1], image.shape[0]
                x_max, y_max = 0, 0

                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)
                    x_max = max(x_max, x + w)
                    y_max = max(y_max, y + h)

                # Crop the image to the bounding box
                cropped_image = image[y_min:y_max, x_min:x_max]

                # Save the cropped image
                result_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGRA2RGBA))
                result_image.save(output_path)
        else:
            print("No non-white areas or transparent background found in the image.")


def is_landscape(image):
    width, height = image.size
    return width / height > 1.25


def resize_and_center(image, box_width, box_height):
    # Calculate the aspect ratio of the image
    aspect_ratio = image.width / image.height

    # Determine the size based on the aspect ratio
    if box_width / box_height > aspect_ratio:
        # Fit to height
        new_height = box_height
        new_width = int(new_height * aspect_ratio)
    else:
        # Fit to width
        new_width = box_width
        new_height = int(new_width / aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a new image with the same size as the bounding box and a transparent background
    centered_image = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))

    # Calculate the position to paste the resized image onto the centered image
    paste_position = ((box_width - new_width) // 2, (box_height - new_height) // 2)

    # Paste the resized image onto the centered image
    centered_image.paste(resized_image, paste_position)
    return centered_image


def combine_images_from_tmp(base_dir):
    """
    Combines images from the 'tmp' subfolder with 'voucher_logo.png' and saves them in the 'vlogo' subfolder.
    :param base_dir: The base directory where the 'vlogo', 'tmp', and 'img' folders are located.
    """
    # Define subfolder paths relative to the base directory
    vlogo_path = os.path.join(base_dir, 'vlogo')
    tmp_path = os.path.join(base_dir, 'vlogo', 'tmp')
    img_path = base_dir

    # Check if all expected images are already in the vlogo folder
    expected_images = [os.path.join(vlogo_path, f"vlogo{i}.png") for i in range(1, 10)]
    if all(os.path.exists(image) for image in expected_images):
        print("All combined images already exist. Exiting function.")
        return

    # Ensure the vlogo folder exists
    if not os.path.exists(vlogo_path):
        os.makedirs(vlogo_path)

    # Loop through the images in the tmp folder
    for i in range(1, 10):  # Assuming there are 9 images named png_1.png, png_2.png, etc.
        tmp_image_path = os.path.join(tmp_path, f"png_{i}.png")
        voucher_logo_path = os.path.join(img_path, "voucher_logo.png")
        output_image_path = os.path.join(vlogo_path, f"vlogo{i}.png")

        # Skip if the output image already exists
        if os.path.exists(output_image_path):
            # print(f"Image {output_image_path} already exists. Skipping.")
            continue

        # Check if the tmp image exists
        if os.path.exists(tmp_image_path):
            try:
                # Open the two images (overlay and base)
                base_image = Image.open(voucher_logo_path).convert("RGBA")
                overlay_image = Image.open(tmp_image_path).convert("RGBA")

                # Combine the images by alpha compositing
                combined_image = Image.alpha_composite(base_image, overlay_image)

                # Save the combined image in the vlogo folder
                combined_image.save(output_image_path, "PNG")
                # print(f"Combined image saved as {output_image_path}")
            except Exception as e:
                print(f"Error combining images {tmp_image_path} and {voucher_logo_path}: {e}")
        else:
            print(f"Image {tmp_image_path} does not exist.")


def start_http_server():
    # Construct paths to node.exe and http-server
    http_server_command = os.path.join(exe_dir, 'nodejs', 'node.exe')
    http_server_script = os.path.join(exe_dir, 'node_modules', 'http-server', 'bin', 'http-server')

    # Check if node.exe and http-server exist
    if not os.path.isfile(http_server_command) or not os.path.isfile(http_server_script):
        print("Error: Node.js or http-server not found.")
        return

    # Check if http-server (node.exe) is already running
    try:
        tasklist_output = subprocess.check_output('tasklist /FI "IMAGENAME eq node.exe" 2>NUL', shell=True).decode('utf-8')
        if "node.exe" in tasklist_output:
            print("http-server is already running. Stopping it...")
            subprocess.call('taskkill /F /IM "node.exe" /T >NUL', shell=True)  # Terminate the process
            time.sleep(2)  # Allow time for the process to terminate
    except subprocess.CalledProcessError:
        print("Error: Failed to check tasklist.")

    # Properly quote the paths to handle spaces
    http_server_command = f'"{http_server_command}"'
    http_server_script = f'"{http_server_script}"'

    # Combine the command to run http-server
    command = f'{http_server_command} {http_server_script}'

    # Run the http-server command in a new console window, without keeping it open unnecessarily
    subprocess.Popen(f'start /min cmd /c \"{command} && exit\"', shell=True)  # The 'exit' will close the console window after server starts
    

def open_browser():
    print(f"Customizing your vouchers now...")
    time.sleep(1)

    url = f"http://localhost:8080/app/PrintVoucher.html"

    # Open the URL in the default browser
    subprocess.Popen(f'start "" "{url}"', shell=True)

    # Allocate 5 seconds loading time to make sure web form has been rendered completely
    # Allocate higher value for slow internet connection
    time.sleep(5)

    # Create WScript Shell Object to access filesystem
    WshShell = win32.Dispatch("WScript.Shell")

    # Select, or bring focus to a window named `Google Chrome`
    WshShell.AppActivate("Google Chrome")

    # Wait for 2 seconds, then press Ctrl+P to open the print window
    time.sleep(2)
    WshShell.SendKeys("^p")    


def main():
    # Check if VoucherList exist
    check_voucher_list()

    # Define subfolder paths relative to the base directory
    qr_logo_path = os.path.join(base_dir, 'put_qr_logo_here')

     # Define file paths
    qr_code_path = os.path.join(qr_logo_path, 'qr_code.png')
    logo_path = os.path.join(qr_logo_path, 'logo.png')   

    # Check if "put_qr_logo_here" folder exists or if qr_code.png or logo.png are missing
    if not os.path.exists(qr_logo_path) or not os.path.isfile(qr_code_path) or not os.path.isfile(logo_path):
        combine_images_from_tmp(base_dir)
        start_http_server()
        open_browser()
        return

    # Define file paths for cropped images and the temp image
    qr_code_cropped_path = os.path.join(qr_logo_path, 'qr_code_cropped.png')
    logo_cropped_path = os.path.join(qr_logo_path, 'logo_cropped.png')
    qr_logo_temp_path = os.path.join(qr_logo_path, 'qr_logo_temp.png')

    # Remove background and crop QR code and logo images
    remove_background_and_crop(qr_code_path, qr_code_cropped_path)
    remove_background_and_crop(logo_path, logo_cropped_path)

    # Load the cropped QR code and logo images
    qr_code_image = Image.open(qr_code_cropped_path).convert("RGBA")
    logo_image = Image.open(logo_cropped_path).convert("RGBA")

    # Determine the orientation of the logo and set the main image and coordinates
    if is_landscape(logo_image):
        right_rectangle_coords = (955, 161, 1251, 267)  # Landscape coordinates
    else:
        right_rectangle_coords = (955, 161, 1251, 373)  # Portrait coordinates        

    # Load the main image
    main_image = Image.open(qr_logo_temp_path).convert("RGBA")

    # Resize the main image to 1283 x 750 pixels
    main_image = main_image.resize((1283, 750), Image.Resampling.LANCZOS)

    # Define the coordinates of the gray rectangles (left, top, right, bottom for the left rectangle)
    left_rectangle_coords = (40, 161, 330, 451)

    # Calculate the width and height of each rectangle
    left_rectangle_width = left_rectangle_coords[2] - left_rectangle_coords[0]
    left_rectangle_height = left_rectangle_coords[3] - left_rectangle_coords[1]
    right_rectangle_width = right_rectangle_coords[2] - right_rectangle_coords[0]
    right_rectangle_height = right_rectangle_coords[3] - right_rectangle_coords[1]

    # Resize the QR code and logo images to fit within the rectangles while maintaining aspect ratio
    qr_code_centered = resize_and_center(qr_code_image, left_rectangle_width, left_rectangle_height)
    logo_centered = resize_and_center(logo_image, right_rectangle_width, right_rectangle_height)

    # Paste the resized images onto the main image at the specified coordinates
    main_image.paste(qr_code_centered, (left_rectangle_coords[0], left_rectangle_coords[1]), qr_code_centered)
    main_image.paste(logo_centered, (right_rectangle_coords[0], right_rectangle_coords[1]), logo_centered)

    # Save the final image
    output_path = os.path.join(base_dir, 'voucher_logo.png')
    main_image.save(output_path)

    # Rename the folder
    new_folder_path = os.path.join(base_dir, 'put_qr_logo_here_UPDATED')
    os.rename(qr_logo_path, new_folder_path)    

    combine_images_from_tmp(base_dir)
    start_http_server()
    open_browser()

if __name__ == "__main__":
    main()
