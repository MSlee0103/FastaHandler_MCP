# FastaHandler: created by Hyungtaek Jung
# This script to make a sequence partition based on the name of CL in the fasta header.
# Example usage: python3 chr_pansn_extract.py --input-fa FAfile --output Outfolder (--t and --mem optional)

#!/usr/bin/env python3
import os
import gzip
import argparse
from multiprocessing import Pool, cpu_count
from Bio import SeqIO
import logging

# Set up logging
logging.basicConfig(filename='chr_pansn_extract.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description='Separate fasta sequences into groups based on CL: prefix in headers.')
    parser.add_argument('--input-fa', required=True, help='Input fasta file path (*.fasta, *.fa, *.fasta.gz, *.fa.gz)')
    parser.add_argument('--output', required=True, help='Output directory for separated fasta files')
    parser.add_argument('--t', type=int, default=1, help='Number of CPUs to use (default: 1)')
    parser.add_argument('--mem', type=int, default=10, help='Memory in GB to use (default: 10)')
    return parser.parse_args()

def validate_file_extension(file_path):
    if not any(file_path.endswith(ext) for ext in ['.fasta', '.fa', '.fasta.gz', '.fa.gz']):
        raise ValueError("Invalid file format. Provide a .fasta, .fa, .fasta.gz, or .fa.gz file.")

def read_fasta(file_path):
    """Yield records one by one (no full memory loading)."""
    open_func = gzip.open if file_path.endswith('.gz') else open
    with open_func(file_path, 'rt') as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            yield record

def group_sequences(file_path):
    """Groups sequences by CL prefix."""
    groups = {}
    for record in read_fasta(file_path):
        header = record.description
        if 'CL:' in header:
            cl_prefix = header.split('CL:')[1].split('_')[0]
            groups.setdefault(cl_prefix, []).append(record)
        else:
            logging.warning(f"No 'CL:' found in header: {header}")
    return groups

def write_group(group_record):
    """Write records for a group to a fasta file."""
    group, records, output_dir = group_record
    output_file = os.path.join(output_dir, f"{group}.fasta")
    with open(output_file, 'w') as f:
        SeqIO.write(records, f, 'fasta')
    logging.info(f"Wrote {len(records)} sequences to {output_file}")

def main():
    args = parse_args()

    try:
        validate_file_extension(args.input_fa)
    except ValueError as e:
        logging.error(e)
        print(e)
        return

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    cpu_count_to_use = min(args.t, cpu_count())
    logging.info(f"Using {cpu_count_to_use} CPUs and {args.mem} GB memory")

    # Group sequences
    groups = group_sequences(args.input_fa)
    logging.info(f"Found {len(groups)} groups")

    # Parallel write
    group_data = [(group, records, args.output) for group, records in groups.items()]
    with Pool(processes=cpu_count_to_use) as pool:
        pool.map(write_group, group_data)

if __name__ == "__main__":
    main()

