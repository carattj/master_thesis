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
parser = argparse.ArgumentParser(description="Extract identifiers from the given APK.")
parser.add_argument("-i", "--input_apk", dest="input_apk", help="Path to the APK")
parser.add_argument("-o", "--output_dir", dest="output_dir", help="Path to the output directory")
args = parser.parse_args()

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

print(f'APK = {args.input_apk}')
process_apk(args.input_apk, args.output_dir)
