# FastaHandler: created by Hyungtaek Jung
# Extract matched ID/header sequences and their locations from a multi-fasta (multiline) file to be written in a single-line fasta
# Must create the input header file after removing ">"
# Note, users must provide -1 less numbers for start and end location. 
# Example command: python3 id_extract_location.py --input-seq test.fa --hdr-id Seq%_3 --start 30 --end 40 --out test_out.fa (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging

logging.basicConfig(filename="id_extract_location.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Extract sequence by header and location from multi-line FASTA.")
    parser.add_argument("--input-seq", required=True, help="Input FASTA file (.fa, .fasta, .gz, .bz2, .tar.gz, .zip).")
    parser.add_argument("--hdr-id", required=True, help="Header ID to extract (without '>').")
    parser.add_argument("--start", type=int, required=True, help="Start location (1-based).")
    parser.add_argument("--end", type=int, required=True, help="End location (1-based).")
    parser.add_argument("--out", required=False, help="Output FASTA file.")
    parser.add_argument("--t", type=int, default=1, help="CPUs (default: 1).")
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
        sys.exit("Not a proper file format. Please provide a readable file format to call the 'idextloc module.'")

def extract_sequence(filepath, hdr_id, start, end):
    """Extract sequence by header and position."""
    handle = open_fasta_stream(filepath)
    sequence = ""
    found = False
    for line in handle:
        if line.startswith(">"):
            current_header = line[1:].strip()
            found = (current_header == hdr_id)
        elif found:
            sequence += line.strip().upper()
    if not sequence:
        sys.exit("Error: Header ID does not match any sequence in the FASTA file.")
    seq_len = len(sequence)
    if start < 1 or end > seq_len or start > end:
        sys.exit("Error: Start/end positions out of range.")
    return sequence[start-1:end]

def write_output(header, sequence, output_file):
    with open(output_file, 'w') as f:
        f.write(f">{header}\n{sequence}\n")

def main():
    args = parse_args()
    logging.info(f"Input FASTA file: {args.input_seq}")
    logging.info(f"Header ID: {args.hdr_id}, Start: {args.start}, End: {args.end}, CPUs: {args.t}, Memory: {args.mem}GB")

    extracted_seq = extract_sequence(args.input_seq, args.hdr_id, args.start, args.end)
    output_file = args.out or os.path.join(os.getcwd(), "extracted_sequence.fasta")
    write_output(args.hdr_id, extracted_seq, output_file)
    logging.info(f"Extracted sequence saved to: {output_file}")

if __name__ == "__main__":
    main()
