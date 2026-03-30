# FastaHandler: created by Hyungtaek Jung
# Open Reading Frames / Transcription May Begin Anywhere
# 6 possible reading frames includng forward & reverse complement sequences
# ">>>" and "<<<" tags to highlight the longest_nt_seq and longest_protein_seq
# Fasta file header must be no "space" and convert an automatic singleline
# Need to install Biopython
# A total of four outputs (Edited from 6f4.py)
# Example usage: python translate_dna.py --input-seq test_files.fasta.gz --out transated.fa (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import gzip
import bz2
import tarfile
import zipfile
from Bio import SeqIO
from Bio.Seq import Seq
from multiprocessing import Pool, cpu_count
from functools import partial
import logging

# Setup logging
logging.basicConfig(filename='translate_dna.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Efficient decompression handling
def extract_sequences(file_path):
    records = []
    if file_path.endswith('.gz'):
        with gzip.open(file_path, 'rt') as f:
            records.extend(SeqIO.parse(f, 'fasta'))
    elif file_path.endswith('.bz2'):
        with bz2.open(file_path, 'rt') as f:
            records.extend(SeqIO.parse(f, 'fasta'))
    elif file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as z:
            for name in z.namelist():
                with z.open(name) as f:
                    records.extend(SeqIO.parse(f.read().decode().splitlines(), 'fasta'))
    elif file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile():
                    f = tar.extractfile(member)
                    records.extend(SeqIO.parse(f.read().decode().splitlines(), 'fasta'))
    elif file_path.endswith(('.fasta', '.fa', '.fna')):
        with open(file_path, 'r') as f:
            records.extend(SeqIO.parse(f, 'fasta'))
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    return records

# Find ORFs
def find_orfs(sequence):
    start_codon = "ATG"
    stop_codons = {"TAA", "TAG", "TGA"}
    orfs = set()
    for strand, seq in [(+1, sequence), (-1, sequence.reverse_complement())]:
        seq_len = len(seq)
        for frame in range(3):
            i = frame
            while i < seq_len - 2:
                codon = seq[i:i+3]
                if codon == start_codon:
                    for j in range(i+3, seq_len-2, 3):
                        if seq[j:j+3] in stop_codons:
                            orfs.add(str(seq[i:j+3]))
                            break
                i += 3
    return orfs

# Process a record
def process_record(record, output_dir):
    try:
        orfs_nt = find_orfs(record.seq)
        orfs_protein = [str(Seq(orf).translate(to_stop=True)) for orf in orfs_nt]
        longest_nt = max(orfs_nt, key=len, default=None)
        longest_prot = max(orfs_protein, key=len, default=None)

        write_orfs(record.id, orfs_nt, 'nt', output_dir)
        write_orfs(record.id, orfs_protein, 'prot', output_dir)

        if longest_nt:
            write_selected(record.id + '_longest_nt', longest_nt, 'nt_sltd', output_dir)
        if longest_prot:
            write_selected(record.id + '_longest_prot', longest_prot, 'prot_sltd', output_dir)

    except Exception as e:
        logging.error(f"Error processing {record.id}: {e}")

# Write ORFs
def write_orfs(header, orfs, orf_type, output_dir):
    out_file = os.path.join(output_dir, f"out_{orf_type}.fasta")
    with open(out_file, 'a') as f:
        for orf in orfs:
            f.write(f">{header}\n{orf}\n")

# Write selected ORF
def write_selected(header, sequence, file_suffix, output_dir):
    out_file = os.path.join(output_dir, f"out_{file_suffix}.fasta")
    with open(out_file, 'a') as f:
        f.write(f">{header}\n{sequence}\n")

# Main workflow
def process_files(input_files, output_dir, threads):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pool = Pool(processes=threads)
    for file in input_files:
        records = extract_sequences(file)
        pool.map(partial(process_record, output_dir=output_dir), records)
    pool.close()
    pool.join()

def main():
    parser = argparse.ArgumentParser(description="Efficient ORF extraction from compressed/uncompressed FASTA files.")
    parser.add_argument("--input-seq", required=True, help="FASTA file pattern (e.g., '*.fasta' or '*.fasta.gz')")
    parser.add_argument("--out", required=True, help="Output directory for ORF sequences")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs (default: 1)")
    parser.add_argument("--mem", type=int, default=10, help="Memory (GB), not enforced (default: 10)")
    args = parser.parse_args()

    if args.t < 1:
        raise ValueError("Number of CPUs must be at least 1")

    input_files = [f for f in glob.glob(args.input_seq)]
    if not input_files:
        raise ValueError("No input files found with the provided pattern")

    process_files(input_files, args.out, args.t)
    logging.info(f"Processing completed for files: {input_files}")

if __name__ == "__main__":
    main()
