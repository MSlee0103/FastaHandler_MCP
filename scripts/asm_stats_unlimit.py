# FastaHandler: created by Hyungtaek Jung
# Unlimited multiple multi-fasta (multiline) files to calculate assembly stats
# Example command: python3 asm_stats_unlimit.py --input-seqs test1.fa test2.fa test3.fa test4.fa test5.fa --out asm_stats_unlimt.txt (w/ optional for --t cpu and --mem memory)

#!/usr/bin/env python3

import argparse
import os
import gzip
import logging
from collections import Counter
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed

# Setup logging
logging.basicConfig(filename='asm_stats_unlimit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_fasta(file_path):
    """Generator to read sequences from fasta (supports .gz)."""
    open_func = gzip.open if file_path.endswith(".gz") else open
    with open_func(file_path, 'rt') as f:
        seq_id = None
        seq_lines = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq_id:
                    yield seq_id, ''.join(seq_lines).upper()
                seq_id = line[1:]
                seq_lines = []
            else:
                seq_lines.append(line)
        if seq_id:
            yield seq_id, ''.join(seq_lines).upper()

def calculate_summary_stats(file_path):
    """Calculate assembly statistics for a fasta file."""
    sequences = list(read_fasta(file_path))
    genome = ''.join(seq for _, seq in sequences)

    # Basic stats
    input_id = os.path.basename(file_path)
    assembled_genome = len(genome)
    contigs = len(sequences)
    gap_count = genome.count('-')
    uncertain_bp = sum(1 for nt in genome if nt not in 'ATGCN-')

    nucleotide_counts = Counter(genome)
    total_bp = len(genome)

    # Percentages
    gc_percent = (nucleotide_counts.get('G', 0) + nucleotide_counts.get('C', 0)) / total_bp * 100 if total_bp else 0
    a_percent = nucleotide_counts.get('A', 0) / total_bp * 100 if total_bp else 0
    t_percent = nucleotide_counts.get('T', 0) / total_bp * 100 if total_bp else 0
    g_percent = nucleotide_counts.get('G', 0) / total_bp * 100 if total_bp else 0
    c_percent = nucleotide_counts.get('C', 0) / total_bp * 100 if total_bp else 0
    n_percent = nucleotide_counts.get('N', 0) / total_bp * 100 if total_bp else 0

    # N50, L50, N90, L90 calculations
    contig_lengths = sorted([len(seq) for _, seq in sequences], reverse=True)
    n50, l50, n90, l90 = calculate_n50_l50_n90_l90(contig_lengths)

    # Length ranges
    length_ranges = calculate_length_ranges(contig_lengths)

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
        "Ncount": nucleotide_counts.get('N', 0),
        "N50": n50,
        "L50": l50,
        "N90": n90,
        "L90": l90,
        "Max": contig_lengths[0] if contig_lengths else 0,
        "Min": contig_lengths[-1] if contig_lengths else 0,
        "GapCount(-)": gap_count,
        "Uncertain(bp)": uncertain_bp,
        **length_ranges
    }

def calculate_n50_l50_n90_l90(lengths):
    """Compute N50/L50 and N90/L90 using cumulative length logic."""
    if not lengths:
        return 0, 0, 0, 0
    total_length = sum(lengths)
    half_total_length = total_length / 2
    ninety_percent_length = total_length * 0.90
    cumulative_length = 0
    n50 = l50 = n90 = l90 = 0
    for index, length in enumerate(lengths):
        cumulative_length += length
        if cumulative_length >= half_total_length and n50 == 0:
            n50 = length
            l50 = index + 1
        if cumulative_length >= ninety_percent_length and n90 == 0:
            n90 = length
            l90 = index + 1
        if n50 and n90:
            break
    return n50, l50, n90, l90

def calculate_length_ranges(lengths):
    bins = [200, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000]
    ranges = {f"{b}bp": 0 for b in bins}
    ranges["Over10Mbp"] = 0
    for length in lengths:
        for b in bins:
            if length < b:
                ranges[f"{b}bp"] += 1
                break
        else:
            ranges["Over10Mbp"] += 1
    return ranges

def generate_summary_output(summary_stats_list, output_file):
    df = pd.DataFrame(summary_stats_list).set_index("InputID").transpose()
    df.to_csv(output_file, sep='\t')
    logging.info(f"Summary written to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Parallel assembly statistics for multiple fasta files.")
    parser.add_argument("--input-seqs", nargs='+', required=True, help="Input fasta files (.fa or .fa.gz).")
    parser.add_argument("--out", required=True, help="Output file path.")
    parser.add_argument("--t", type=int, default=1, help="Number of CPUs.")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB.")

    args = parser.parse_args()

    if args.t < 1 or args.mem < 1:
        raise ValueError("CPUs and memory must be >=1")
    
    logging.info(f"Processing {len(args.input_seqs)} files with {args.t} CPUs and {args.mem}GB memory")

    # Validate input files
    for file_path in args.input_seqs:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        logging.info(f"Input file: {file_path}")

    # Process files in parallel using futures to improve scaling with many files
    summary_stats_list = []
    with ProcessPoolExecutor(max_workers=args.t) as executor:
        future_to_file = {executor.submit(calculate_summary_stats, f): f for f in args.input_seqs}
        for future in as_completed(future_to_file):
            summary_stats_list.append(future.result())

    # Output results
    generate_summary_output(summary_stats_list, args.out)

if __name__ == "__main__":
    main()
