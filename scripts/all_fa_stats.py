# FastaHandler: created by Hyungtaek Jung
# A multi-fasta (multiline) file to calculate assembly stats comprehensively (N50, N90, L50, L90)
# Example command: python3 all_fa_stats.py --input-seq test1.fa --out all_stats_out.txt (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import re
import gzip
import logging
from collections import Counter
import numpy as np
import pandas as pd

# Set up logging
logging.basicConfig(filename='all_fa_stats.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def open_fasta(file_path):
    """
    Open a fasta file, handling both compressed and uncompressed formats efficiently.
    """
    if file_path.endswith(('.gz', '.tar.gz', '.bz2')):
        return gzip.open(file_path, 'rt')
    elif file_path.endswith('.zip'):
        import zipfile
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            fasta_files = [f for f in zip_ref.namelist() if f.endswith(('.fa', '.fasta', '.fna'))]
            if not fasta_files:
                raise ValueError("No fasta file found in the zip archive.")
            return zip_ref.open(fasta_files[0], 'r')
    else:
        return open(file_path, 'r')

def parse_fasta(file_path):
    """
    Reads a fasta file efficiently, extracting only the first part of the header.
    """
    sequences = {}
    current_seq_id = None

    with open_fasta(file_path) as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                current_seq_id = line.split()[0][1:]
                sequences[current_seq_id] = []
            else:
                sequences[current_seq_id].append(line)

    return {seq_id: "".join(seq).replace(" ", "").upper() for seq_id, seq in sequences.items()}

def calculate_summary_stats(file_path):
    sequences = parse_fasta(file_path)
    genome = "".join(sequences.values())

    input_id = os.path.basename(file_path)
    assembled_genome = len(genome)
    contigs = len(sequences)
    gap_count = genome.count("-")
    uncertain_bp = sum(1 for char in genome if char not in "ATGCN-")

    nucleotide_counts = Counter(genome)
    total_bp = len(genome)

    gc_percent = (nucleotide_counts["G"] + nucleotide_counts["C"]) / total_bp * 100
    a_percent = nucleotide_counts["A"] / total_bp * 100
    t_percent = nucleotide_counts["T"] / total_bp * 100
    g_percent = nucleotide_counts["G"] / total_bp * 100
    c_percent = nucleotide_counts["C"] / total_bp * 100
    n_percent = nucleotide_counts["N"] / total_bp * 100

    sorted_contigs = sorted(sequences.values(), key=len, reverse=True)
    total_length = sum(len(contig) for contig in sorted_contigs)

    half_total_length = total_length / 2
    cumulative_length = 0
    n50, l50 = None, 0
    for index, contig in enumerate(sorted_contigs):
        cumulative_length += len(contig)
        if cumulative_length >= half_total_length and n50 is None:
            n50 = len(contig)
            l50 = index + 1

    ninety_percent_length = total_length * 0.90
    cumulative_length = 0
    n90, l90 = None, 0
    for index, contig in enumerate(sorted_contigs):
        cumulative_length += len(contig)
        if cumulative_length >= ninety_percent_length and n90 is None:
            n90 = len(contig)
            l90 = index + 1

    range_counts = Counter()
    for length in map(len, sequences.values()):
        if length < 200:
            range_counts["200bp"] += 1
        elif 200 < length < 1000:
            range_counts["1Kbp"] += 1
        elif 1000 < length < 5000:
            range_counts["5Kbp"] += 1
        elif 5000 < length < 10000:
            range_counts["10Kbp"] += 1
        elif 10000 < length < 50000:
            range_counts["50Kbp"] += 1
        elif 50000 < length < 100000:
            range_counts["100Kbp"] += 1
        elif 100000 < length < 500000:
            range_counts["500Kbp"] += 1
        elif 500000 < length < 1000000:
            range_counts["1Mbp"] += 1
        elif 1000000 < length < 5000000:
            range_counts["5Mbp"] += 1
        else:
            range_counts["Over10Mbp"] += 1

    logging.info("Summary statistics calculated successfully.")
    return {
        "InputID": input_id,
        "AssembledGenome": assembled_genome,
        "Contigs": contigs,
        "GC(%)": round(gc_percent, 2),
        "A(%)": round(a_percent, 2),
        "T(%)": round(t_percent, 2),
        "G(%)": round(g_percent, 2),
        "C(%)": round(c_percent, 2),
        "N(%)": round(n_percent, 2),
        "Ncount": nucleotide_counts["N"],
        "N50": n50,
        "N90": n90,
        "L50": l50,
        "L90": l90,
        "Max": len(sorted_contigs[0]),
        "Min": len(sorted_contigs[-1]),
        "GapCount(-)": gap_count,
        "Uncertain(bp)": uncertain_bp,
        "200bp": range_counts["200bp"],
        "1Kbp": range_counts["1Kbp"],
        "5Kbp": range_counts["5Kbp"],
        "10Kbp": range_counts["10Kbp"],
        "50Kbp": range_counts["50Kbp"],
        "100Kbp": range_counts["100Kbp"],
        "500Kbp": range_counts["500Kbp"],
        "1Mbp": range_counts["1Mbp"],
        "5Mbp": range_counts["5Mbp"],
        "Over10Mbp": range_counts["Over10Mbp"]
    }

def generate_summary_output(summary_stats, output_file):
    headers = [
        "InputID", "AssembledGenome", "Contigs", "GC(%)", "A(%)", "T(%)", "G(%)", "C(%)", "N(%)", "Ncount",
        "N50", "N90", "L50", "L90", "Max", "Min", "GapCount(-)", "Uncertain(bp)",
        "200bp", "1Kbp", "5Kbp", "10Kbp", "50Kbp", "100Kbp", "500Kbp", "1Mbp", "5Mbp", "Over10Mbp"
    ]

    data = [[summary_stats[header] for header in headers]]
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(output_file, sep='\t', index=False)

    logging.info(f"Summary output written to {output_file} successfully.")

def main():
    parser = argparse.ArgumentParser(description="Comprehensive Python script for analyzing fasta files.")
    parser.add_argument("--input-seq", required=True, help="Input fasta file path.")
    parser.add_argument("--out", required=True, help="Output file path for summary results.")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs.")
    parser.add_argument("--mem", type=int, default=10, help="Amount of memory in gigabytes.")

    args = parser.parse_args()

    if args.t < 1 or args.mem < 1:
        print("Invalid CPU or memory value. Please provide integers greater than 0.")
        return

    if not os.path.isfile(args.input_seq):
        raise FileNotFoundError("Input file not found.")

    summary_stats = calculate_summary_stats(args.input_seq)

    generate_summary_output(summary_stats, args.out)

if __name__ == "__main__":
    main()

