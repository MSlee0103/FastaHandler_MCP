# FastaHandler: created by Hyungtaek Jung
# Remove the duplicate ID and sequence from a multi-fasta (multiline) file to be written in a single-line fasta
# Include duplicated headers and their occurrence counts
# Example command: python3 remove_duplicate.py --input-seq test.fa --out . (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging
from collections import Counter, defaultdict

logging.basicConfig(filename="remove_duplicate.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def open_fasta_stream(file_path):
    """Stream fasta content from compressed or uncompressed file."""
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')
    elif file_path.endswith('.bz2'):
        return bz2.open(file_path, 'rt')
    elif file_path.endswith(('.fa', '.fasta', '.fna')):
        return open(file_path, 'r')
    elif file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith(('.fa', '.fasta', '.fna')):
                    return (line.decode().strip() for line in tar.extractfile(member))
    elif file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as z:
            for fname in z.namelist():
                if fname.endswith(('.fa', '.fasta', '.fna')):
                    return (line.decode().strip() for line in z.open(fname))
    else:
        raise ValueError("Unsupported file format.")

def process_fasta(stream):
    header_counts = Counter()
    sequences = defaultdict(str)
    header = None
    for line in stream:
        line = line.strip()
        if line.startswith(">"):
            header = line[1:]
            header_counts[header] += 1
        elif header:
            sequences[header] += line
    return header_counts, sequences

def write_header_counts(header_counts, output_dir):
    path = os.path.join(output_dir, "out_header_count.txt")
    with open(path, 'w') as f:
        f.write("Header\tCount\n")
        for header, count in sorted(header_counts.items()):
            f.write(f"{header}\t{count}\n")

def write_unique_fasta(header_counts, sequences, output_dir):
    path = os.path.join(output_dir, "out_rmv_dupl.fasta")
    with open(path, 'w') as f:
        for header, seq in sequences.items():
            if header_counts[header] == 1:
                f.write(f">{header}\n{seq}\n")

def main():
    parser = argparse.ArgumentParser(description="Remove duplicate FASTA headers and count occurrences.")
    parser.add_argument("--input-seq", required=True, help="Input FASTA file (supports .fa, .fasta, .gz, .bz2, .tar.gz, .zip).")
    parser.add_argument("--output", "--out", default="./", help="Output directory.")
    parser.add_argument("--t", type=int, default=1, help="CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    args = parser.parse_args()

    if args.t < 1 or args.mem < 1:
        sys.exit("Error: CPUs and memory must be positive integers.")

    os.makedirs(args.output, exist_ok=True)
    logging.info(f"Processing {args.input_seq}")

    fasta_stream = open_fasta_stream(args.input_seq)
    header_counts, sequences = process_fasta(fasta_stream)
    write_header_counts(header_counts, args.output)
    write_unique_fasta(header_counts, sequences, args.output)

    logging.info("Processing complete.")

if __name__ == "__main__":
    main()
