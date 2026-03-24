# FastaHandler: created by Hyungtaek Jung
# Concatenate sequences with the same ID from multiple fasta files (unlimited)
# Example command: python3 concatenate_fa.py --input-seq test1.fa test2.fa test3.fa test4.fa test5.fa --out concat_seq_out.fa (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import gzip
import logging
from collections import defaultdict
from multiprocessing import Pool, cpu_count

# Set up logging
logging.basicConfig(filename='concatenate_fa.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_fasta(file_path):
    """Yield sequences (seq_id, sequence) from a fasta file (supports .gz)."""
    open_func = gzip.open if file_path.endswith('.gz') else open
    with open_func(file_path, 'rt') as f:
        seq_id = None
        seq_lines = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq_id:
                    yield seq_id, ''.join(seq_lines)
                seq_id = line[1:]
                seq_lines = []
            else:
                seq_lines.append(line)
        if seq_id:
            yield seq_id, ''.join(seq_lines)

def process_file(file_path):
    """Parse sequences from a single file and return a dictionary."""
    sequences = defaultdict(str)
    for seq_id, seq in parse_fasta(file_path):
        sequences[seq_id] += seq
    logging.info(f"Processed file: {file_path}")
    return sequences

def merge_sequences(seq_dicts):
    """Merge multiple sequence dictionaries."""
    merged = defaultdict(str)
    for seqs in seq_dicts:
        for seq_id, seq in seqs.items():
            merged[seq_id] += seq
    return merged

def generate_fasta_output(sequences, output_file):
    with open(output_file, 'w') as f:
        for seq_id, sequence in sequences.items():
            f.write(f">{seq_id}\n{sequence}\n")
    logging.info(f"Concatenated fasta output written to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Concatenate multiple fasta files.")
    parser.add_argument("--input-seqs", nargs='+', required=True, help="Input fasta files (.fa or .gz).")
    parser.add_argument("--out", required=True, help="Output fasta file.")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs.")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB.")

    args = parser.parse_args()

    # Validate CPUs and memory
    cpu_to_use = min(args.t, cpu_count())
    logging.info(f"Using {cpu_to_use} CPUs and {args.mem} GB memory.")

    # Validate input files
    for file in args.input_seqs:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"Input file not found: {file}")
        logging.info(f"Input file: {file}")

    # Process input files in parallel
    with Pool(cpu_to_use) as pool:
        seq_dicts = pool.map(process_file, args.input_seqs)

    # Merge sequences
    concatenated_sequences = merge_sequences(seq_dicts)

    # Write output
    generate_fasta_output(concatenated_sequences, args.out)

if __name__ == "__main__":
    main()
