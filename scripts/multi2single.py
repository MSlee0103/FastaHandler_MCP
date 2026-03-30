# FastaHandler: created by Hyungtaek Jung
# A multi-fasta (multiline) file to a single-line fasta
# Example command: python3 multi2single.py --input-seq test.fa --out test_out.fa (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging

logging.basicConfig(filename="multi2single.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Convert multi-line FASTA to single-line FASTA (compressed or uncompressed).")
    parser.add_argument("--input-seq", required=True, help="Input FASTA file (.fa, .fasta, .gz, .bz2, .tar.gz, .zip).")
    parser.add_argument("--out", required=False, help="Output FASTA file.")
    parser.add_argument("--t", type=int, default=1, help="CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    args = parser.parse_args()

    if not os.path.isfile(args.input_seq):
        sys.exit("Error: Input file not found.")
    if args.t < 1 or args.mem < 1:
        sys.exit("Error: CPUs and memory must be positive integers.")
    if not args.out:
        args.out = os.path.join(os.getcwd(), "singleline_output.fasta")
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
                if member.isfile() and member.name.endswith(('.fa', '.fasta')):
                    return (line.decode().strip() for line in tar.extractfile(member))
    elif filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            for fname in z.namelist():
                if fname.endswith(('.fa', '.fasta')):
                    return (line.decode().strip() for line in z.open(fname))
    else:
        sys.exit("Unsupported file format.")
    return None

def multi2singleline(input_handle, output_file):
    with open(output_file, 'w') as f_out:
        header, seq_lines = None, []
        for line in input_handle:
            if line.startswith(">"):
                if header:
                    f_out.write(f"{header}\n{''.join(seq_lines)}\n")
                header = line.strip()
                seq_lines = []
            else:
                seq_lines.append(line.strip())
        if header:
            f_out.write(f"{header}\n{''.join(seq_lines)}\n")

def main():
    args = parse_args()
    logging.info(f"Input: {args.input_seq}, Output: {args.out}, CPUs: {args.t}, Mem: {args.mem}GB")

    input_handle = open_fasta_stream(args.input_seq)
    if input_handle:
        multi2singleline(input_handle, args.out)
        logging.info(f"Processed: {args.input_seq}")
    else:
        sys.exit("No FASTA file found in archive.")

if __name__ == "__main__":
    main()
