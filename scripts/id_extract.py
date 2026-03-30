# FastaHandler: created by Hyungtaek Jung
# Extract matched ID/header sequences from a multi-fasta (multiline) file to be written in a single-line fasta
# Must create the input header file after removing ">"
# Example command: python3 id_extract.py --input-seq test.fa --input-hdr test_id.txt --out test_out.fa (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging

logging.basicConfig(filename="id_extract.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Extract sequences based on headers from a multi-line FASTA file.")
    parser.add_argument("--input-seq", required=True, help="Input FASTA file (.fa, .fasta, .gz, .bz2, .tar.gz, .zip).")
    parser.add_argument("--input-hdr", required=True, help="Header file (one per line, without '>').")
    parser.add_argument("--out", required=False, help="Output FASTA file path.")
    parser.add_argument("--t", type=int, default=1, help="CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    args = parser.parse_args()

    if not os.path.isfile(args.input_seq):
        sys.exit("Error: Input FASTA file not found.")
    if not os.path.isfile(args.input_hdr):
        sys.exit("Error: Input header file not found.")
    if args.t < 1 or args.mem < 1:
        sys.exit("Error: CPUs and memory must be positive integers.")
    return args

def open_file_stream(filepath):
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
        sys.exit("Not a proper file format. Please provide a readable file format to call the 'idextract module.'")

def extract_sequences(input_seq_file, header_set, output_file):
    handle = open_file_stream(input_seq_file)
    with open(output_file, 'w') as f_out:
        header, seq_lines = None, []
        for line in handle:
            if line.startswith(">"):
                if header in header_set:
                    f_out.write(f">{header}\n{''.join(seq_lines)}\n")
                header = line[1:].strip()
                seq_lines = []
            else:
                seq_lines.append(line.strip())
        if header in header_set:
            f_out.write(f">{header}\n{''.join(seq_lines)}\n")

def main():
    args = parse_args()
    logging.info(f"Input FASTA: {args.input_seq}, Header file: {args.input_hdr}, CPUs: {args.t}, Mem: {args.mem}GB")

    with open(args.input_hdr, 'r') as f_header:
        header_set = set(line.strip() for line in f_header if line.strip())

    output_file = args.out or os.path.join(os.getcwd(), "extracted_sequences.fasta")
    extract_sequences(args.input_seq, header_set, output_file)
    logging.info(f"Extraction completed. Output saved to: {output_file}")

if __name__ == "__main__":
    main()
