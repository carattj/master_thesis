import os
import cv2
import numpy as np
import argparse
from skimage.metrics import structural_similarity as ssim

def write_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(f'{content}\n')

def create_file(file_path):
    try:
        with open(file_path, 'w') as file:
            print(f"File '{file_path}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")

def compare_images(image1_path, image2_path, img_fail_path):
    # Load images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    img_fail = cv2.imread(img_fail_path)

    # Check if images are loaded successfully
    if image2 is None:
        return -1, -1, -1, -1
    
    # Check if image2 has zero size
    if image2.size == 0:
        return -2, -2, -2, -2
    
    # Check if image2 and image1 have different shapes
    if image2.shape != image1.shape:
        return -3, -3, -3, -3
    
    # Crop images to consider only the upper part
    height, width, _ = image2.shape
    upper_height = height // 2
    top_offset = height // 13  # Adjust this value according to your specific image # 27
    cropped_image1 = image1[top_offset:upper_height, :]
    cropped_image2 = image2[top_offset:upper_height, :]
    cropped_img_fail = img_fail[top_offset:upper_height, :]

    # Convert cropped images to grayscale
    gray_image1 = cv2.cvtColor(cropped_image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(cropped_image2, cv2.COLOR_BGR2GRAY)
    gray_img_fail = cv2.cvtColor(cropped_img_fail, cv2.COLOR_BGR2GRAY)

    if cropped_image2.shape != cropped_img_fail.shape:
        img_fail = np.rot90(img_fail)
        cropped_img_fail = img_fail[top_offset:upper_height, :]
        gray_img_fail = cv2.cvtColor(cropped_img_fail, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM and MSE
    ssim_score, _ = ssim(gray_image1, gray_image2, full=True)
    mse = np.mean((gray_image1 - gray_image2) ** 2)

    # Calculate SSIM and MSE with fail image
    ssim_score_fail, _ = ssim(gray_img_fail, gray_image2, full=True)
    mse_fail = np.mean((gray_img_fail - gray_image2) ** 2)

    return ssim_score, mse, ssim_score_fail, mse_fail

def main(dir_a, dir_b, out_file_path, fail_img):
    # Iterate over images in both directories
    for i, img_a in enumerate(os.listdir(dir_a)):
        if img_a.endswith(".png"):
            print(f'##### {i} - {img_a}')
            img_a_path = os.path.join(dir_a, img_a)
            image_b_path = os.path.join(dir_b, img_a)  # Assuming filenames are the same
            if os.path.exists(image_b_path):
                ssim_score, mse, ssim_score_fail, mse_fail = compare_images(img_a_path, image_b_path, fail_img)
                img_name = img_a.split('.')[0]
                write_to_file(out_file_path, f'{img_name},{ssim_score},{mse},{ssim_score_fail},{mse_fail}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute similarity (SSIM, MSE) between images with the same name contained in the given two directories (-1 = zero bytes, -2 = absent img)')
    parser.add_argument('--dir_a', '-a', type=str, help='Path to the first directory')
    parser.add_argument('--dir_b', '-b', type=str, help='Path to the second directory')
    parser.add_argument('--out_dir', '-o', type=str, help='Path to the output directory')
    parser.add_argument('--fail_img', '-f', type=str, help='Failed screenshot reference')
    args = parser.parse_args()
    
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    out_file_name = args.dir_b.split('/')[-1]
    out_file = f'sim_{out_file_name}.csv'
    out_file_path = os.path.join(args.out_dir, out_file)
    create_file(out_file_path)
    write_to_file(out_file_path, f'hash,ssim,mse,ssim_fail,mse_fail')

    main(args.dir_a, args.dir_b, out_file_path, args.fail_img)
