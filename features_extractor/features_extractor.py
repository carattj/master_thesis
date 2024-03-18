import os
import csv
import argparse
from androguard.misc import AnalyzeAPK


def extract_apk_info(input_dir, output_file):
    # Iterate over each APK file in the input directory
    for apk_file in os.listdir(input_dir):
        if apk_file.endswith('.apk'):
            apk_path = os.path.join(input_dir, apk_file)

            # Get APK size
            size = os.path.getsize(apk_path)

            # Extract permissions
            try:
                a = a, dx, d = AnalyzeAPK(apk_path)
                permissions = a.get_permissions()
                permissions = ';'.join(permissions)
            except Exception as e:
                permissions = 'Error extracting permissions'

            # Extract version code, version name, target SDK version, and minimum SDK version
            version_code = a.get_androidversion_code()
            version_name = a.get_androidversion_name()
            target_sdk_version = a.get_target_sdk_version()
            min_sdk_version = a.get_min_sdk_version()

            # Write the extracted information to the CSV file
            write_to_file(output_file, f'{apk_file},{size},{permissions},{version_code},{version_name},{target_sdk_version},{min_sdk_version}')

def write_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(f'{content}\n')

def create_file(file_path):
    try:
        with open(file_path, 'w') as file:
            print(f"File '{file_path}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract APK information and write to CSV')
    parser.add_argument('-i', '--input', dest='input_dir', help='Path to the directory containing APKs')
    parser.add_argument('-o', '--output', dest='output_file', help='Path to the output CSV file')
    args = parser.parse_args()

    create_file(args.output_file)
    write_to_file(args.output_file, 'hash,size,permissions,version_code,version_name,target_sdk_version,min_sdk_version')

    extract_apk_info(args.input_dir, args.output_file)
