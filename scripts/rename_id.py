# FastaHandler: created by Hyungtaek Jung
# A multi-fasta (multiline) file to a single-line fasta with changing ID/Prefix names
# Example command: python3 rename_id.py --input-seq test.fa --out test_out.fa --new-name Changed (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging

logging.basicConfig(filename="rename_id.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Convert multi-line FASTA to single-line FASTA and rename headers.")
    parser.add_argument("--input-seq", required=True, help="Input FASTA file (.fa, .fasta, .gz, .bz2, .tar.gz, .zip).")
    parser.add_argument("--out", required=False, help="Output FASTA file.")
    parser.add_argument("--new-name", required=True, help="New ID/prefix for FASTA headers.")
    parser.add_argument("--t", type=int, default=1, help="CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    return parser.parse_args()

def open_fasta_stream(file_path):
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

def rename_and_convert(input_stream, output_file, new_name):
    header_count = 1
    header, seq_lines = None, []

    with open(output_file, 'w') as f_out:
        for line in input_stream:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    f_out.write(f">{new_name}_{header_count}\n{''.join(seq_lines)}\n")
                    header_count += 1
                header = line[1:]
                seq_lines = []
            else:
                seq_lines.append(line.upper())
        if header:
            f_out.write(f">{new_name}_{header_count}\n{''.join(seq_lines)}\n")

def main():
    args = parse_args()
    logging.info(f"Input: {args.input_seq}, Output: {args.out}, New name: {args.new_name}, CPUs: {args.t}, Mem: {args.mem}GB")

    output_file = args.out or os.path.join(os.getcwd(), f"renameid_seq_T{args.t}.fa")
    fasta_stream = open_fasta_stream(args.input_seq)
    rename_and_convert(fasta_stream, output_file, args.new_name)

    logging.info(f"Processing complete. Output saved to {output_file}")

if __name__ == "__main__":
    main()
