# FastaHandler: created by Hyungtaek Jung
# A multi-fasta (multiline) file to calculate each fasta sequence stats
# Example command: python3 each_fa_stats.py --input-seq test1.fa --out test_stats_out.txt (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import re
import gzip
import logging
from concurrent.futures import ThreadPoolExecutor
from Bio import SeqIO

# Set up logging
logging.basicConfig(filename='each_fa_stats.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_fasta(file_path):
    """Return a generator for sequence records, supporting gzip."""
    if file_path.endswith(".gz"):
        with gzip.open(file_path, "rt") as handle:
            yield from SeqIO.parse(handle, "fasta")
    else:
        with open(file_path, "r") as handle:
            yield from SeqIO.parse(handle, "fasta")

def process_record(record):
    """Process a single record: ID and sequence length (ATGCN only)."""
    clean_seq = re.sub(r'[^ATGCN]', '', str(record.seq).upper())
    return (record.id, len(clean_seq))

def calculate_summary_stats(file_path, threads=1):
    """Calculate sequence statistics in parallel."""
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(process_record, read_fasta(file_path)))
    return results

def generate_summary_output(summary_stats, output_file):
    with open(output_file, 'w') as f:
        for seq_id, length in summary_stats:
            f.write(f"{seq_id}\t{length}\n")
    logging.info(f"Summary output written to {output_file} successfully.")

def main():
    parser = argparse.ArgumentParser(description="Fast and parallel fasta statistics generator.")
    parser.add_argument("--input-seq", required=True, help="Input fasta file path (.fa or .fa.gz).")
    parser.add_argument("--out", required=True, help="Output file path for summary results.")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs.")
    parser.add_argument("--mem", type=int, default=10, help="Amount of memory in gigabytes.")

    args = parser.parse_args()

    if args.t < 1 or args.mem < 1:
        raise ValueError("Invalid CPU or memory values. Must be integers >= 1.")
    if not os.path.isfile(args.input_seq):
        raise FileNotFoundError(f"Input file not found: {args.input_seq}")

    logging.info(f"Running with {args.t} CPUs and {args.mem} GB memory")
    logging.info(f"Reading input: {args.input_seq}")

    stats = calculate_summary_stats(args.input_seq, args.t)
    logging.info(f"Processed {len(stats)} sequences.")
    generate_summary_output(stats, args.out)

if __name__ == "__main__":
    main()
