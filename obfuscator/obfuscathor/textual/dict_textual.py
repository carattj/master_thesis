import re
import argparse
from unidecode import unidecode

def parse_text(text):
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Remove accents from letters
    text = unidecode(text)
    # Extract individual words
    words = text.split()
    # Remove duplicates while preserving order
    unique_words = list(dict.fromkeys(words))
    return unique_words

def write_to_file(words, output_file):
    with open(output_file, 'w') as file:
        for word in words:
            file.write(word + '\n')

def main():
    parser = argparse.ArgumentParser(description='Parse text and remove punctuation.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Path to the input text file.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to the output text file.')
    args = parser.parse_args()

    with open(args.input, 'r') as file:
        input_text = file.read()

    # Parse the text
    words = parse_text(input_text)
    # Write the parsed words to a file
    write_to_file(words, args.output)

    print(f'Parsed text has been written to {args.output}.')

if __name__ == "__main__":
    main()
