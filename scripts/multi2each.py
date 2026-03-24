# FastaHandler: created by Hyungtaek Jung
# A multi-fasta file to a each (split) fasta
# Example command: python3 multi2each.py --input-seq test.fa --out output_dir (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging
from multiprocessing import Pool, cpu_count

# Setup logging
logging.basicConfig(filename='multi2each.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(
        description="Split multi-FASTA file into individual FASTA files for each sequence.\n"
                    "--input-seq: Input file path (supports .fa, .fasta, .gz, .bz2, .tar.gz, .zip)\n"
                    "--out: Output directory for individual FASTA files\n"
                    "--t: Number of CPUs (default: 1)\n"
                    "--mem: Memory in GB (default: 10)"
    )
    parser.add_argument("--input-seq", required=True, help="Input multi-FASTA file path")
    parser.add_argument("--out", required=True, help="Output directory for separated FASTA files")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs (default: 1)")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10)")
    args = parser.parse_args()

    if not os.path.isfile(args.input_seq):
        sys.exit("Not a proper file format. Please provide a readable file and sequence format to call the “multi2each module.”")

    if args.t < 1 or args.mem < 1:
        sys.exit("Not an integer number. Please provide only readable integer numbers to call the proper CPUs and Memory.")

    os.makedirs(args.out, exist_ok=True)

    return args

def open_fasta(file_path):
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')
    elif file_path.endswith('.bz2'):
        return bz2.open(file_path, 'rt')
    elif file_path.endswith(('.fa', '.fasta')):
        return open(file_path, 'r')
    else:
        return None

def extract_archive(file_path, extract_dir):
    if file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(path=extract_dir)
    elif file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

def safe_filename(header):
    return ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in header.strip())

def split_fasta(args):
    header, seq_lines, output_dir = args
    filename = f"{safe_filename(header)}.fa"
    output_file = os.path.join(output_dir, filename)
    with open(output_file, 'w') as f:
        f.write(f">{header}\n{''.join(seq_lines)}\n")
    logging.info(f"Wrote: {output_file}")

def process_fasta(input_file, output_dir, cpus):
    sequences = []
    current_header = None
    seq_lines = []
    
    handle = open_fasta(input_file)
    if not handle:
        sys.exit("Not a proper file format. Please provide a readable file and sequence format to call the “multi2each module.”")

    with handle:
        for line in handle:
            line = line.strip()
            if line.startswith(">"):
                if current_header:
                    sequences.append((current_header, seq_lines.copy(), output_dir))
                current_header = line[1:]
                seq_lines = []
            else:
                seq_lines.append(line.upper())
        if current_header:
            sequences.append((current_header, seq_lines, output_dir))

    with Pool(processes=cpus) as pool:
        pool.map(split_fasta, sequences)

def main():
    args = parse_args()
    logging.info(f"Input: {args.input_seq}, Output: {args.out}, CPUs: {args.t}, Memory: {args.mem}GB")

    input_file = args.input_seq
    output_dir = args.out

    if input_file.endswith(('.tar.gz', '.zip')):
        extract_dir = os.path.join(output_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        extract_archive(input_file, extract_dir)
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f.endswith(('.fa', '.fasta')):
                    process_fasta(os.path.join(root, f), output_dir, args.t)
    else:
        process_fasta(input_file, output_dir, args.t)

if __name__ == "__main__":
    main()
