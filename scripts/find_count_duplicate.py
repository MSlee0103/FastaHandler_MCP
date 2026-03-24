# FastaHandler: created by Hyungtaek Jung
# Find and count the duplicate ID and sequence from a multi-fasta (multiline) file
# Example command: python3 find_count_duplicate.py --input-seq test.fa --out test_out.txt (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging

logging.basicConfig(filename="find_count_duplicate.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Find and count duplicated headers in a multi-line FASTA file.")
    parser.add_argument("--input-seq", required=True, help="Input FASTA file path (supports .fa, .fasta, .gz, .bz2, .tar.gz, .zip).")
    parser.add_argument("--out", required=False, help="Output summary file path.")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    args = parser.parse_args()

    if not os.path.isfile(args.input_seq):
        sys.exit("Error: Input FASTA file not found or inaccessible.")
    if args.t < 1 or args.mem < 1:
        sys.exit("Error: CPUs and memory must be positive integers.")
    return args

def open_fasta_stream(filepath):
    """Open FASTA file with support for compression."""
    if filepath.endswith('.gz'):
        return gzip.open(filepath, 'rt')
    elif filepath.endswith('.bz2'):
        return bz2.open(filepath, 'rt')
    elif filepath.endswith(('.fa', '.fasta')):
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
        sys.exit("Not a proper file format. Please provide a readable file format to call the 'findcntdupl module.'")

def count_headers(filepath):
    """Count duplicated headers in the FASTA file."""
    index = {}
    handle = open_fasta_stream(filepath)
    for line in handle:
        if line.startswith(">"):
            header = line[1:].strip()
            index[header] = index.get(header, 0) + 1
    return index

def write_output(index, output_file):
    with open(output_file, 'w') as f:
        f.write("Headers\tCounts\n")
        for header, count in index.items():
            if count > 1:
                f.write(f"{header}\t{count}\n")

def main():
    args = parse_args()
    logging.info(f"Input FASTA file: {args.input_seq}")
    logging.info(f"Output summary file: {args.out if args.out else 'default output path'}")
    logging.info(f"CPUs: {args.t}, Memory: {args.mem}GB")

    index = count_headers(args.input_seq)

    output_path = args.out or os.path.join(os.getcwd(), "duplicated_headers.txt")
    write_output(index, output_path)

    logging.info(f"Duplicated headers written to: {output_path}")

if __name__ == "__main__":
    main()
