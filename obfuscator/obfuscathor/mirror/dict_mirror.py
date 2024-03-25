import os
import argparse

def parse_class_identifier(line):
    # Split the line by '/' and return the last part
    line = line.replace('-','').replace(';','').replace('$','')
    parts = line.split('/')
    last_part = parts[-1].strip()
    if last_part[0] == 'R':
        last_part = 'r' + last_part[1:]  # Construct a new string with the modification
    return last_part

def parse_method_identifier(line):
    line = line.replace('<','').replace('>','')
    line = line.replace('-','')
    return line

def parse_field_identifier(line):
    line = line.replace('-','')
    return line

def collect_txt_files(input_dir, output_dir):
    categories = {'fields': set(), 'methods': set(), 'classes': set()}

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isfile(filepath) and filename.endswith('.txt'):
            category = None
            if filename.endswith('fields.txt'):
                category = 'fields'
            elif filename.endswith('methods.txt'):
                category = 'methods'
            elif filename.endswith('classes.txt'):
                category = 'classes'

            if category:
                # Read each line from the file and add unique lines to the category set
                with open(filepath, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line:  # Skip empty lines
                            if category == 'classes':
                                line = parse_class_identifier(line)
                            if category == 'methods':
                                line = parse_method_identifier(line)
                            if category == 'fields':
                                line = parse_field_identifier(line)
                            categories[category].add(line)

    # Write unique lines to separate output files for each category
    for category, lines in categories.items():
        output_file = os.path.join(output_dir, f'{category}.txt')
        with open(output_file, 'w') as out_file:
            for line in sorted(lines):  # Sort the lines alphabetically
                out_file.write(line + '\n')

def main():
    parser = argparse.ArgumentParser(description='Collect lines from txt files into separate category files.')
    parser.add_argument('--input_directory', '-i', type=str, help='Path to the input directory containing txt files')
    parser.add_argument('--output_directory', '-o', type=str, help='Path to the output directory where category files will be saved')
    args = parser.parse_args()

    input_dir = args.input_directory
    output_dir = args.output_directory

    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    collect_txt_files(input_dir, output_dir)
    print(f'Lines collected from {input_dir} and saved to {output_dir}.')

if __name__ == '__main__':
    main()
