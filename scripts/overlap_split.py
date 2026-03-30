# FastaHandler: created by Hyungtaek Jung
# A multi-fasta file to a each fasta (split w/ overlapping)
# Example command: python3 overlap_split.py --input-seq test.fa --overlap-size 100000 --out output_dir (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging

# Set up logging
logging.basicConfig(filename='overlap_split.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(
        description="Split a single FASTA sequence into two overlapping parts.\n"
                    "--input-seq: Indicate the input file and path\n"
                    "--overlap-size: Indicate the overlap size between sequences\n"
                    "--out: Output file prefix\n"
                    "--t: Number of CPUs (integer)\n"
                    "--mem: Number of memory in GB (integer)"
    )
    parser.add_argument("--input-seq", required=True, help="Input FASTA file path (.fa, .fasta, .fna, .gz, .bz2, .tar.gz, .zip)")
    parser.add_argument("--overlap-size", type=int, required=True, help="Overlap size between split sequences")
    parser.add_argument("--out", required=True, help="Output file prefix")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs (default: 1)")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10)")
    
    args = parser.parse_args()

    if not os.path.isfile(args.input_seq):
        sys.exit("Not a proper file format. Please provide a readable file and sequence format to call the “overlapsplit module.”")
    if args.t < 1 or args.mem < 1:
        sys.exit("Not an integer number. Please provide only readable integer numbers to call the proper CPUs and Memory.")
    if args.overlap_size < 0:
        sys.exit("Overlap size must be a non-negative integer.")

    return args

def open_fasta(file_path):
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')
    elif file_path.endswith('.bz2'):
        return bz2.open(file_path, 'rt')
    elif file_path.endswith(('.fa', '.fasta', '.fna')):
        return open(file_path, 'r')
    else:
        return None

def extract_archive(file_path, extract_dir):
    if file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(path=extract_dir)
    elif file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(path=extract_dir)

def process_fasta(input_file, overlap_size, output_prefix):
    handle = open_fasta(input_file)
    if not handle:
        sys.exit("Not a proper file format. Please provide a readable file and sequence format to call the “overlapsplit module.”")

    header, sequence = None, []
    with handle:
        for line in handle:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    split_and_write(header, sequence, overlap_size, output_prefix)
                header = line[1:]
                sequence = []
            else:
                sequence.append(line.upper())
        if header:
            split_and_write(header, sequence, overlap_size, output_prefix)

def split_and_write(header, sequence, overlap_size, output_prefix):
    seq_str = ''.join(sequence)
    total_len = len(seq_str)
    midpoint = total_len // 2
    overlap = overlap_size

    # Calculate splits with overlap
    a_end = midpoint + overlap
    b_start = midpoint + 1

    seq_a = seq_str[:a_end]
    seq_b = seq_str[b_start:]

    out_a = f"{output_prefix}{safe_filename(header)}_a.fa"
    out_b = f"{output_prefix}{safe_filename(header)}_b.fa"

    with open(out_a, 'w') as fa:
        fa.write(f">{header}_a\n{seq_a}\n")
    with open(out_b, 'w') as fb:
        fb.write(f">{header}_b\n{seq_b}\n")

    logging.info(f"Split {header}: {out_a} (1-{a_end}), {out_b} ({b_start}-{total_len})")

def safe_filename(header):
    return ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in header.strip())

def main():
    args = parse_args()
    logging.info(f"Input: {args.input_seq}, Overlap: {args.overlap_size}, Output: {args.out}, CPUs: {args.t}, Memory: {args.mem}GB")

    input_file = args.input_seq
    overlap_size = args.overlap_size
    output_prefix = args.out

    if input_file.endswith(('.tar.gz', '.zip')):
        extract_dir = os.path.splitext(os.path.basename(input_file))[0] + "_extracted"
        os.makedirs(extract_dir, exist_ok=True)
        extract_archive(input_file, extract_dir)
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f.endswith(('.fa', '.fasta', '.fna')):
                    process_fasta(os.path.join(root, f), overlap_size, output_prefix)
    else:
        process_fasta(input_file, overlap_size, output_prefix)

if __name__ == "__main__":
    main()
