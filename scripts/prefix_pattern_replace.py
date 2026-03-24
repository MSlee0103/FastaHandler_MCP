# FastaHandler: created by Hyungtaek Jung
# A multi-fasta (multiline) file to a single-line fasta with replacing ID/Prefix name files like "sed" command
# Example command: python3 prefix_pattern_replace.py --input-seq test.fa --find-ptrn ptrn.txt --replace replace.txt --out output_dir (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import re
import gzip
import bz2
import tarfile
import zipfile
import logging
from Bio import SeqIO
import multiprocessing

# Set up logging
logging.basicConfig(filename='prefix_pattern_replace.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def open_fasta_stream(filepath):
    """Stream fasta content from compressed or uncompressed file."""
    if filepath.endswith('.gz'):
        return gzip.open(filepath, 'rt')
    elif filepath.endswith('.bz2'):
        return bz2.open(filepath, 'rt')
    elif filepath.endswith(('.fa', '.fasta', '.fna')):
        return open(filepath, 'r')
    elif filepath.endswith('.tar.gz'):
        with tarfile.open(filepath, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith(('.fa', '.fasta', '.fna')):
                    return (line.decode().strip() for line in tar.extractfile(member))
    elif filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            for fname in z.namelist():
                if fname.endswith(('.fa', '.fasta', '.fna')):
                    return (line.decode().strip() for line in z.open(fname))
    else:
        raise ValueError("Unsupported file format.")

def process_sequence(record, find_pattern, replace_pattern):
    """Replace pattern in fasta header and description."""
    record.id = re.sub(find_pattern, replace_pattern, record.id)
    record.description = re.sub(find_pattern, replace_pattern, record.description)
    return record

def replace_pattern_in_fasta(input_fasta, find_pattern, replace_pattern, output_fasta, threads):
    input_handle = open_fasta_stream(input_fasta)
    records = list(SeqIO.parse(input_handle, "fasta"))
    with multiprocessing.Pool(threads) as pool:
        modified_records = pool.starmap(process_sequence, [(rec, find_pattern, replace_pattern) for rec in records])

    temp_output_fasta = output_fasta + ".temp"
    with open(temp_output_fasta, "w") as temp_out:
        SeqIO.write(modified_records, temp_out, "fasta")

    multi2singleline(temp_output_fasta, output_fasta)
    os.remove(temp_output_fasta)
    logging.info(f"Modified fasta saved to {output_fasta}")

def multi2singleline(input_file, output_file):
    """Convert multi-line fasta to single-line fasta."""
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        header, seq_lines = None, []
        for line in f_in:
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
    parser = argparse.ArgumentParser(description="Replace pattern in fasta headers and convert to single-line fasta.")
    parser.add_argument("--input-seq", required=True, help="Input fasta file path.")
    parser.add_argument("--find-ptrn", required=True, help="Pattern to find in fasta headers.")
    parser.add_argument("--replace", required=True, help="String to replace the pattern.")
    parser.add_argument("--out", required=True, help="Output fasta file path.")
    parser.add_argument("--t", type=int, default=1, help="CPUs for multiprocessing.")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB.")
    args = parser.parse_args()

    logging.info(f"Input: {args.input_seq}, Output: {args.out}, CPUs: {args.t}, Mem: {args.mem}GB")
    replace_pattern_in_fasta(args.input_seq, args.find_ptrn, args.replace, args.out, args.t)

if __name__ == "__main__":
    main()
