import os
import pandas as pd
import argparse
from androguard.misc import AnalyzeAPK

def get_identifiers_names(path):
    a, dx, d = AnalyzeAPK(path)
    
    fields = set()
    methods = set()
    classes = set()

    for c in d.get_classes():
        classes.add(c.name)
        for m in c.get_methods():
            methods.add(m.name)
        for f in c.get_fields():
            fields.add(f.name)
    return fields, methods, classes

def write_to_file(file, content):
    with open(file, 'w') as f:
        for line in content:
            f.write(f"{line}\n")

def process_apk(apk_file, output_dir):
    apk_name = os.path.basename(apk_file).split('.')[0]
    try:
        fields, methods, classes = get_identifiers_names(apk_file)
        write_to_file(f'{output_dir}/{apk_name}_fields.txt', fields)
        write_to_file(f'{output_dir}/{apk_name}_methods.txt', methods)
        write_to_file(f'{output_dir}/{apk_name}_classes.txt', classes)

    except Exception as e:
        print('Failed: ' + apk_file + "\t" + str(e))


# Initialize argument parser
parser = argparse.ArgumentParser(description="Process APK files and generate CSV output")
parser.add_argument("-i", "--input_dir", dest="input_dir", help="Path to the directory containing APK files")
parser.add_argument("-o", "--output_dir", dest="output_dir", help="Path to the output CSV file")
args = parser.parse_args()

apk_files = os.listdir(args.input_dir)

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

for apk_file in apk_files:
    print(f'APK = {apk_file}')
    apk_path = os.path.join(args.input_dir, apk_file)
    process_apk(apk_path, args.output_dir)
