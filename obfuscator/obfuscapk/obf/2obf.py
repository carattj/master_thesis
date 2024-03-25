import subprocess
import os
import sys
import time

# usage: python obf.py ./apk ./apks.txt ./fields
# bring apks in the same working directory

def write_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(f'{content}\n')

def run_command(apk_files, mode, input_dir, output_dir, stats_dir):

    # Iterate over each APK file
    for i, apk_file in enumerate(apk_files):
        print(f'## Mode - {mode[0]} + {mode[1]}')
        print(f'## APK {i} - {apk_file}')

        start_time = time.time()  # Record start time
        
        command = [
            "docker", "run", "--rm", "-it",
            "-u", "1001:1001",
            "-v", f"{os.getcwd()}:/workdir",
            "obfuscapk", "-i",
            "-o", f"{mode[0]}",
            "-o", f"{mode[1]}",
            "-o", "Rebuild", "-o", "NewAlignment", "-o", "NewSignature",
            os.path.join(input_dir, apk_file),
            "-w",
            os.path.join(output_dir, f'{mode[0]}_{mode[1]}'),
        ]

        try:
            subprocess.run(command, check=True)
            end_time = time.time()
            duration = end_time - start_time
            write_to_file(os.path.join(stats_dir, f'{mode[0]}_{mode[1]}.csv'), f'{apk_file},{True},{duration:.2f}')
            print(f"### Successful (Time: {duration:.2f} seconds)")
        except subprocess.CalledProcessError as e:
            end_time = time.time()
            duration = end_time - start_time
            write_to_file(os.path.join(stats_dir, f'{mode[0]}_{mode[1]}.csv'), f'{apk_file},{False},{duration:.2f}')
            print(f"### Fail")
            continue

def process_apks(input_dir, output_dir, stats_dir, modes):

    apk_files = os.listdir(input_dir)
    print(f'## APKs to be obfuscated = {len(apk_files)}')
    
    for i, mode in enumerate(modes):
        print(f'\n# Mode {i} - {mode[0]} + {mode[1]}')
        write_to_file(os.path.join(stats_dir, f'{mode[0]}_{mode[1]}.csv'), 'hash,obfuscated,time')
        run_command(apk_files, mode, input_dir, output_dir, stats_dir)

def main():
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python script.py INPUT_DIRECTORY OUTPUT_DIRECTORY")
        sys.exit(1)
    
    # Extract input arguments
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    stats_dir = os.path.join(output_dir, 'stats')
    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)

    modes = [['FieldRename','MethodRename'],['FieldRename','ClassRename'],['MethodRename', 'ClassRename']]

    print(f'# Obfuscation')
    print(f'## input directory = {input_dir}')
    print(f'## output directory = {output_dir}')
    print(f'## number of modes = {len(modes)}')

    process_apks(input_dir, output_dir, stats_dir, modes)

if __name__ == "__main__":
    main()
