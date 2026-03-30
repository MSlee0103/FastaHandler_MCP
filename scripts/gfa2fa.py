# FastaHandler: created by Hyungtaek Jung
# This script to convert a gfa file to fasta file
# Example command: python3 gfa2fa.py --input-gfa test.gfa --out test_out.fa (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import gzip
import logging
import multiprocessing
from itertools import islice

def parse_args():
    parser = argparse.ArgumentParser(description="Convert GFA file to FASTA format (compressed or uncompressed).")
    parser.add_argument("--input-gfa", required=True, help="Input GFA file (.gfa or .gfa.gz).")
    parser.add_argument("--out", required=True, help="Output FASTA file.")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    return parser.parse_args()

def setup_logging():
    logging.basicConfig(filename='gfa2fa.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def open_file(file_path):
    return gzip.open(file_path, 'rt') if file_path.endswith('.gz') else open(file_path, 'r')

def convert_lines_to_fasta(lines):
    return [f">{parts[1]}\n{parts[2]}\n"
            for line in lines if line.startswith('S')
            for parts in [line.strip().split('\t')] if len(parts) >= 3]

def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            return
        yield chunk

def gfa_to_fasta(input_gfa, output_fasta, num_cpus, chunk_size=1000):
    with open_file(input_gfa) as f_in, open(output_fasta, 'w') as f_out, multiprocessing.Pool(num_cpus) as pool:
        for idx, chunk in enumerate(chunked_iterable(f_in, chunk_size)):
            fasta_chunks = pool.map(convert_lines_to_fasta, [chunk])
            for fasta_lines in fasta_chunks:
                f_out.writelines(fasta_lines)
            logging.info(f"Processed chunk {idx + 1}")

def main():
    args = parse_args()
    setup_logging()
    logging.info(f"Starting GFA to FASTA conversion with {args.t} CPUs and {args.mem}GB memory.")
    gfa_to_fasta(args.input_gfa, args.out, args.t)
    logging.info(f"GFA to FASTA conversion completed. Output saved to {args.out}")

if __name__ == "__main__":
    main()
