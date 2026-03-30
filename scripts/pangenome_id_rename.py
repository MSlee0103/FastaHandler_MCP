# FastaHandler: created by Hyungtaek Jung
# This script to rename the fasta header text file for pangenome, then as an input for prefix_slect_rename.py.
# Make sure the original Fasta headers do not have any space. The space must be replaced with "_". 
# Example command: python3 pangenome_id_rename.py --input test.txt --out output_dir (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import os
import sys
import argparse
import gzip
import bz2
import tarfile
import zipfile
import logging
import multiprocessing

logging.basicConfig(filename='pangenome_id_rename.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description="Process fasta header information and add new column based on conditions.")
    parser.add_argument('--input', required=True, help='Input file path (.txt, .fasta, .fa, .fna, .gz, .bz2, .zip, .tar.gz)')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--t', type=int, default=1, help='Number of CPUs (default: 1)')
    parser.add_argument('--mem', type=int, default=10, help='Memory in GB (default: 10)')
    return parser.parse_args()

def open_file_stream(filepath):
    if filepath.endswith('.gz'):
        return gzip.open(filepath, 'rt')
    elif filepath.endswith('.bz2'):
        return bz2.open(filepath, 'rt')
    elif filepath.endswith(('.fa', '.fasta', '.fna', '.txt')):
        return open(filepath, 'r')
    elif filepath.endswith('.tar.gz'):
        with tarfile.open(filepath, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile():
                    f = tar.extractfile(member)
                    return (line.decode().strip() for line in f)
    elif filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            extracted = z.namelist()[0]
            return (line.decode().strip() for line in z.open(extracted, 'r'))
    else:
        sys.exit("Not a proper file format. Please provide a readable file format to call the pang_hdr_name module.")

def process_line(line):
    parts = line.split()
    if len(parts) < 3:
        return None
    first_col_char_only = ''.join([i for i in parts[0] if not i.isdigit()])
    ori_seq_id = parts[1].split('=')[1]
    ori_seq_tag = "#1#" if ori_seq_id.startswith("h1") else "#2#" if ori_seq_id.startswith("h2") else None
    if not ori_seq_tag:
        return None
    new_column = f"{first_col_char_only}{ori_seq_tag}{ori_seq_id}"
    original_columns_with_underscores = "_".join(parts[:3])
    return f"{original_columns_with_underscores}\t{new_column}"

def process_stream(handle):
    return [result for result in (process_line(line) for line in handle if line.strip()) if result]

def write_output(lines, output_file):
    with open(output_file, 'w') as f:
        f.write("\n".join(lines) + "\n")

def main():
    args = parse_args()
    logging.info(f"Input: {args.input}, Output: {args.output}, CPUs: {args.t}, Mem: {args.mem}GB")

    handle = open_file_stream(args.input)
    processed_lines = process_stream(handle)
    write_output(processed_lines, args.output)
    logging.info(f"Processing completed. Output saved to {args.output}")

if __name__ == "__main__":
    main()
