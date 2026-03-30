# FastaHandler: created by Hyungtaek Jung
# This script to find and merge fa file if they match a certain pattern.
# Usage: python3 find_merge_fa.py --input-folder ./ --pattern-fa "*input.fasta" --out ./output_merge_files.fa

#!/usr/bin/env python3

import os
import sys
import argparse
import gzip
import bz2
import tarfile
import zipfile
import glob
from multiprocessing import Pool, cpu_count
import logging

# Setup logging
logging.basicConfig(filename='find_merge_fa.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def extract_lines(file_path):
    """Stream lines from compressed or uncompressed FASTA."""
    if file_path.endswith('.gz'):
        with gzip.open(file_path, 'rt') as f:
            for line in f:
                yield line.strip()
    elif file_path.endswith('.bz2'):
        with bz2.open(file_path, 'rt') as f:
            for line in f:
                yield line.strip()
    elif file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as z:
            for file_info in z.infolist():
                with z.open(file_info) as f:
                    for line in f.read().decode().splitlines():
                        yield line.strip()
    elif file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile():
                    f = tar.extractfile(member)
                    for line in f.read().decode().splitlines():
                        yield line.strip()
    elif file_path.endswith(('.fa', '.fasta')):
        with open(file_path, 'r') as f:
            for line in f:
                yield line.strip()
    else:
        raise ValueError("Not a proper file format or pattern. Please provide a readable file, sequence, and pattern format to call the find_merge_fa module.")

def single_line_fasta(lines):
    """Convert multi-line FASTA to single-line FASTA."""
    header, seq_lines = None, []
    for line in lines:
        if line.startswith(">"):
            if header:
                yield header, ''.join(seq_lines)
            header = line
            seq_lines = []
        else:
            seq_lines.append(line.upper())
    if header:
        yield header, ''.join(seq_lines)

def process_file(file_path):
    """Process a single FASTA file."""
    fasta_entries = list(single_line_fasta(extract_lines(file_path)))
    logging.info(f"Processed file: {file_path}, Entries: {len(fasta_entries)}")
    return os.path.basename(file_path), fasta_entries

def merge_fasta(input_folder, pattern_fa, output_file, threads, memory):
    pattern = os.path.join(input_folder, '**', pattern_fa)
    input_files = glob.glob(pattern, recursive=True)
    if not input_files:
        raise ValueError("No files found with the given pattern.")

    logging.info(f"Found {len(input_files)} files: {input_files}")

    with Pool(processes=threads) as pool:
        results = pool.map(process_file, input_files)

    with open(output_file, 'w') as out_f:
        for base_filename, entries in results:
            for header, sequence in entries:
                out_f.write(f">{base_filename}\n{sequence}\n")

    logging.info(f"Merged output written to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="find_merge_fa: Search, process, and merge FASTA files (compressed/uncompressed).")
    parser.add_argument("--input-folder", required=True, help="Specify the working folder (including subfolders).")
    parser.add_argument("--pattern-fa", required=True, help="Specify input pattern (e.g., '*.fasta' or '*.fasta.gz').")
    parser.add_argument("--out", required=True, help="Specify output file path.")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    args = parser.parse_args()

    if args.t < 1 or args.mem < 1:
        raise ValueError("Not an integer number. Please provide only readable integer numbers to call the proper CPUs and Memory.")

    logging.info(f"Input folder: {args.input_folder}, Pattern: {args.pattern_fa}, Output: {args.out}, CPUs: {args.t}, Memory: {args.mem}GB")

    merge_fasta(args.input_folder, args.pattern_fa, args.out, args.t, args.mem)

if __name__ == "__main__":
    main()
