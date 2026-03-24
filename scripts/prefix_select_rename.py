# FastaHandler: created by Hyungtaek Jung
# A multi-fasta (multiline) file to a single-line fasta with changing ID/Prefix name files only in the input id file (No space after the last IDs)
# Example command: python3 prefix_select_rename.py --input-seq test.fa --input-id rename.txt --out . (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import gzip
import bz2
import tarfile
import zipfile
import re
from pathlib import Path

def open_fasta_stream(file_path):
    """Stream fasta content from compressed or uncompressed files."""
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')
    elif file_path.endswith('.bz2'):
        return bz2.open(file_path, 'rt')
    elif file_path.endswith(('.fa', '.fasta', '.fna', '.fas')):
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

def read_id_map(file_path):
    id_map = {}
    with open(file_path) as f:
        for line in f:
            original_id, new_id = line.strip().split('\t')
            id_map[original_id] = new_id
    return id_map

def process_fasta_stream(stream, id_map):
    """Selectively rename fasta headers based on id_map and skip unlisted ones."""
    fasta_header_pattern = re.compile(r'^>(.*?)\s*$')
    sequences = []
    header, seq_lines = None, []
    for line in stream:
        line = line.strip()
        header_match = fasta_header_pattern.match(line)
        if header_match:
            if header in id_map:
                sequences.append((id_map[header], ''.join(seq_lines)))
            header = header_match.group(1)
            seq_lines = []
        else:
            seq_lines.append(line.upper())
    if header in id_map:
        sequences.append((id_map[header], ''.join(seq_lines)))
    return sequences

def write_output(sequences, output_file):
    with open(output_file, 'w') as f:
        for header, seq in sequences:
            f.write(f">{header}\n{seq}\n")

def main():
    parser = argparse.ArgumentParser(description="prfxselrename - Selectively rename fasta headers based on an ID mapping file.")
    parser.add_argument('--input-seq', required=True, help='Input fasta file (supports .fa, .fasta, .gz, .bz2, .tar.gz, .zip)')
    parser.add_argument('--input-id', required=True, help='ID mapping file (tab-separated)')
    parser.add_argument('--out', required=True, help='Output fasta file')
    args = parser.parse_args()

    if not args.input_seq.endswith(('.fasta', '.fa', '.fas', '.fna', '.tar.gz', '.gz', '.zip', '.bz2')):
        raise ValueError("Unsupported file format.")

    id_map = read_id_map(args.input_id)
    fasta_stream = open_fasta_stream(args.input_seq)
    sequences = process_fasta_stream(fasta_stream, id_map)
    write_output(sequences, args.out)

    print(f"Processing completed. Output saved to {args.out}")

if __name__ == "__main__":
    main()
