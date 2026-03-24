# FastaHandler: created by Hyungtaek Jung
# A multi-fasta (multiline) file to a single-line fasta with changing ID/Prefix name files (No space after the last IDs)
# Example command: python3 prefix_rename.py --input-seq test.fa --input-id id_list.txt --out output_dir (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import gzip
import bz2
import tarfile
import zipfile
import re
from pathlib import Path
import multiprocessing as mp

def open_fasta_stream(file_path):
    """Stream FASTA content from compressed or uncompressed file."""
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')
    elif file_path.endswith('.bz2'):
        return bz2.open(file_path, 'rt')
    elif file_path.endswith(('.fasta', '.fa', '.fna', '.fas')):
        return open(file_path, 'r')
    elif file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith(('.fa', '.fasta', '.fna', '.fas')):
                    return (line.decode().strip() for line in tar.extractfile(member))
    elif file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as z:
            for fname in z.namelist():
                if fname.endswith(('.fa', '.fasta', '.fna', '.fas')):
                    return (line.decode().strip() for line in z.open(fname))
    else:
        raise ValueError("Unsupported file format.")

def process_fasta_lines(lines, id_map):
    fasta_header_pattern = re.compile(r'^>(.*?)\s*$')
    sequences = []
    header, seq_lines = None, []
    for line in lines:
        if isinstance(line, bytes):
            line = line.decode().strip()
        else:
            line = line.strip()
        header_match = fasta_header_pattern.match(line)
        if header_match:
            if header:
                sequences.append((header, ''.join(seq_lines)))
            header = id_map.get(header_match.group(1), header_match.group(1))
            seq_lines = []
        else:
            seq_lines.append(line.upper())
    if header:
        sequences.append((header, ''.join(seq_lines)))
    return sequences

def write_output(sequences, output_file):
    with open(output_file, 'w') as f:
        for header, seq in sequences:
            f.write(f">{header}\n{seq}\n")

def read_id_map(id_map_file):
    id_map = {}
    with open(id_map_file) as f:
        for line in f:
            original_id, new_id = line.strip().split('\t')
            id_map[original_id] = new_id
    return id_map

def main():
    parser = argparse.ArgumentParser(description="prfxrename - FASTA header renaming tool with compression support")
    parser.add_argument('--input-seq', required=True, help='Input FASTA file (supports .fasta, .fa, .gz, .bz2, .tar.gz, .zip)')
    parser.add_argument('--input-id', required=True, help='ID mapping file (tab-separated)')
    parser.add_argument('--out', required=True, help='Output FASTA file')
    parser.add_argument('--t', type=int, default=1, help='Number of CPUs (default: 1)')
    parser.add_argument('--mem', type=int, default=10, help='Memory in GB (default: 10)')
    args = parser.parse_args()

    if args.t < 1 or args.mem < 1:
        raise ValueError("CPUs and memory must be positive integers.")

    id_map = read_id_map(args.input_id)

    fasta_stream = open_fasta_stream(args.input_seq)
    sequences = process_fasta_lines(fasta_stream, id_map)
    write_output(sequences, args.out)
    print(f"Processing completed. Output saved to {args.out}")

if __name__ == "__main__":
    main()
