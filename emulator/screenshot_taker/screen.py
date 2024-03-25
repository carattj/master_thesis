import os
import subprocess
import argparse
import time

adb_path = '/home/ubuntu/Android/platform-tools/adb'
emulator_path = '/home/ubuntu/Android/emulator/emulator'
avdmanager_path = '/home/ubuntu/Android/cmdline-tools/latest/bin/avdmanager'
aapt_path = '/home/ubuntu/Android/build-tools/29.0.3/aapt'

# Function to create AVD
def create_avd(avd_name, system_image):
    subprocess.run([avdmanager_path, 'create', 'avd', '-n', avd_name, '-k', system_image])

# Function to launch emulator
def launch_emulator(emulator_name):
    subprocess.Popen([emulator_path, '-avd', emulator_name, '-no-window', '-no-audio'])

# Function to install and run APK
def install_and_run_apk(apk_path):
    subprocess.run([adb_path, 'install', apk_path])
    package_name = subprocess.check_output([aapt_path, 'dump', 'badging', apk_path, '|', 'grep', 'package']).decode().split("'")[1]
    subprocess.run([adb_path, 'shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER', '1'])
    time.sleep(10)  # Wait for app to fully launch

# Function to take screenshot
def take_screenshot(apk_name, apk_directory, output_directory):
    screenshot_name = os.path.splitext(apk_name)[0] + ".png"
    subprocess.run([adb_path, 'shell', 'screencap', '-p', '/sdcard/screenshot.png'])
    subprocess.run([adb_path, 'pull', '/sdcard/screenshot.png', os.path.join(output_directory, screenshot_name)])
    subprocess.run([adb_path, 'shell', 'rm', '/sdcard/screenshot.png'])

    package_name = subprocess.check_output([aapt_path, 'dump', 'badging', os.path.join(apk_directory, apk_name), '|', 'grep', 'package']).decode().split("'")[1]
    subprocess.run([adb_path, 'uninstall', package_name])

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")

# Main function
def main(apk_directory, output_directory, avd_name, system_image):
    # Create AVD
    create_avd(avd_name, system_image)
    
    # Launch emulator
    launch_emulator(avd_name)
    
    # Wait for emulator to boot up
    time.sleep(30)  # Adjust as needed
    
    # Install and run each APK in the directory
    for i, filename in enumerate(os.listdir(apk_directory)):
        if filename.endswith(".apk"):
            print(f'\n###### {i} - {filename}')
            apk_path = os.path.join(apk_directory, filename)
            install_and_run_apk(apk_path)
            take_screenshot(filename, apk_directory, output_directory)
    
    # Close emulator
    subprocess.run([adb_path, 'emu', 'kill'])

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run APKs on an Android emulator and take screenshots.')
    parser.add_argument('--apk_directory', '-a', type=str, help='Path to the directory containing APK files.')
    parser.add_argument('--output_directory', '-o', type=str, help='Path to the directory where screenshots will be saved.')
    parser.add_argument('--avd_name', '-n', type=str, help='Name of the Android Virtual Device (AVD).')
    args = parser.parse_args()

    create_directory(args.output_directory)
    
    main(args.apk_directory, args.output_directory, args.avd_name, "system-images;android-28;google_apis;x86")
