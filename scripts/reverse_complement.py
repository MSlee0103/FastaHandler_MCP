# FastaHandler: created by Hyungtaek Jung
# Make reverse complement sequences from a multi-fasta (multiline) file to be written in a single-line fasta
# Example command: python3 reverse_complement.py --input-seq test.fa --out test_out.fa (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import sys
import gzip
import bz2
import tarfile
import zipfile
import logging

logging.basicConfig(filename="reverse_complement.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Generate reverse complement from multi-line FASTA (compressed or uncompressed).")
    parser.add_argument("--input-seq", required=True, help="Input FASTA file (.fa, .fasta, .gz, .bz2, .tar.gz, .zip).")
    parser.add_argument("--out", required=False, help="Output FASTA file (default: ./output_revcomplement.fasta).")
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

def reverse_complement(sequence):
    complement = str.maketrans("ACGTacgtNn", "TGCAtgcaNn")
    return sequence.translate(complement)[::-1]

def process_fasta_stream(stream, output_file):
    header, seq_lines = None, []
    with open(output_file, 'w') as f_out:
        for line in stream:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    rev_seq = reverse_complement(''.join(seq_lines))
                    f_out.write(f">{header}\n{rev_seq}\n")
                header = line[1:]
                seq_lines = []
            else:
                seq_lines.append(line)
        if header:
            rev_seq = reverse_complement(''.join(seq_lines))
            f_out.write(f">{header}\n{rev_seq}\n")

def main():
    args = parse_args()
    logging.info(f"Input: {args.input_seq}, Output: {args.out}, CPUs: {args.t}, Mem: {args.mem}GB")

    output_file = args.out or os.path.join(os.getcwd(), "output_revcomplement.fasta")
    fasta_stream = open_fasta_stream(args.input_seq)
    process_fasta_stream(fasta_stream, output_file)

    logging.info(f"Reverse complement processing complete. Output saved to {output_file}")

if __name__ == "__main__":
    main()
