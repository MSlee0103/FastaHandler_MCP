# FastaHandler: created by Hyungtaek Jung
# Extract multiple matched ID/header sequences and their locations from a multi-fasta (multiline) file to be written in a single-line fasta
# Must create the input header file after removing ">"
# Must provide with a tap-separated ID/header and their locations (start/end)
# Note, users must provide -1 less numbers for start and end location. 
# Example command: python3 id_extract_multi_location.py --input-seq test.fa --input-ext hdrmulti_id.txt --out test_out.fa (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging

logging.basicConfig(filename="id_extract_multi_location.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Extract sequences based on headers and location from a multi-line FASTA file using multiple header and location information.")
    parser.add_argument("--input-seq", required=True, help="Input FASTA file (.fa, .fasta, .gz, .bz2, .tar.gz, .zip).")
    parser.add_argument("--input-ext", required=True, help="Input text file with header, start, end (tab-separated).")
    parser.add_argument("--out", required=False, help="Output FASTA file path.")
    parser.add_argument("--t", type=int, default=1, help="CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    args = parser.parse_args()

    if not os.path.isfile(args.input_seq):
        sys.exit("Error: Input FASTA file not found.")
    if not os.path.isfile(args.input_ext):
        sys.exit("Error: Input extract file not found.")
    if args.t < 1 or args.mem < 1:
        sys.exit("Error: CPUs and memory must be positive integers.")
    return args

def open_fasta_stream(filepath):
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
        sys.exit("Not a proper file format. Please provide a readable file format to call the 'idextractlocamulti module.'")

def index_fasta(filepath):
    index = {}
    handle = open_fasta_stream(filepath)
    header, seq_lines = None, []
    for line in handle:
        if line.startswith(">"):
            if header:
                index[header] = ''.join(seq_lines)
            header = line[1:].strip()
            seq_lines = []
        else:
            seq_lines.append(line.strip())
    if header:
        index[header] = ''.join(seq_lines)
    return index

def read_extract_file(filepath):
    extract_info = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            fields = line.strip().split('\t')
            if len(fields) != 3:
                logging.warning(f"Invalid line {line_num} in extract file. Skipping.")
                continue
            header, start, end = fields
            try:
                extract_info.append((header, int(start), int(end)))
            except ValueError:
                logging.warning(f"Invalid start/end in line {line_num}. Skipping.")
    return extract_info

def main():
    args = parse_args()
    logging.info(f"Input FASTA: {args.input_seq}, Extract file: {args.input_ext}, CPUs: {args.t}, Mem: {args.mem}GB")

    fasta_index = index_fasta(args.input_seq)
    extract_info = read_extract_file(args.input_ext)

    output_file = args.out or os.path.join(os.getcwd(), "extracted_sequences.fasta")
    with open(output_file, 'w') as f_out:
        for header, start, end in extract_info:
            if header not in fasta_index:
                logging.warning(f"Header '{header}' not found.")
                continue
            sequence = fasta_index[header]
            seq_len = len(sequence)
            if start < 1 or end > seq_len or start > end:
                logging.warning(f"Invalid positions for header '{header}'. Skipping.")
                continue
            extracted_seq = sequence[start-1:end]
            f_out.write(f">{header}_{start}_{end}\n{extracted_seq}\n")

    logging.info(f"Extraction completed. Output saved to: {output_file}")

if __name__ == "__main__":
    main()
