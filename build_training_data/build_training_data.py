import os
import pandas as pd

def filter_indexes(df):
    """
    Filter DataFrame based on given conditions and return indexes.
    """
    return df[((df.ssim == 1) | ((df.ssim >= 0.9) & (df.ssim_fail < 0.78)))].index.tolist()

def process_csv(csv_file, output_dir):
    """
    Process a CSV file and write filtered indexes to an output file.
    """
    # Load CSV file into DataFrame
    df = pd.read_csv(csv_file, index_col='hash')
    
    # Filter indexes
    filtered_indexes = filter_indexes(df)
    
    # Write filtered indexes to output file
    output_file = os.path.splitext(os.path.basename(csv_file))[0] + "_hashes_for_training.txt"
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        for index in filtered_indexes:
            f.write(str(index) + '\n')
    print(f"Filtered indexes for '{csv_file}' written to '{output_path}'.")

def main(input_dir, output_dir):
    """
    Process all CSV files in the given directory.
    """
    # Get list of CSV files in the directory
    csv_files = [file for file in os.listdir(input_dir) if file.endswith('.csv')]
    
    # Process each CSV file
    for csv_file in csv_files:
        process_csv(os.path.join(input_dir, csv_file), output_dir)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process CSV files in a directory and extract filtered indexes.')
    parser.add_argument('--input_dir', '-i', type=str, help='Path to the input directory containing CSV files.')
    parser.add_argument('--output_dir', '-o', type=str, help='Path to the output directory to save filtered indexes.')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Call main function with input and output directories
    main(args.input_dir, args.output_dir)
