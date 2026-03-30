# FastaHandler: created by Hyungtaek Jung
# This script to find and trim anchor sequecnes from input fasta.
# Usage: python3 find_anchor_trim.py --input-fa ref_seq.fa --anchor1-fa anchor1_seq.fa --anchor2-fa anchor2_seq.fa --out ./ --t 1 --mem 10

#!/usr/bin/env python3

import os
import sys
import argparse
import gzip
import bz2
import zipfile
import logging
import multiprocessing as mp
import parasail
from Bio import SeqIO

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Script to find anchors in sequences and trim input sequence accordingly.')
    parser.add_argument('--input-fa', required=True, help='Input fasta file path')
    parser.add_argument('--anchor1-fa', required=True, help='First anchor fasta file path')
    parser.add_argument('--anchor2-fa', required=True, help='Second anchor fasta file path')
    parser.add_argument('--out', required=True, help='Output directory')
    parser.add_argument('--t', type=int, default=1, help='Number of CPUs (default: 1)')
    parser.add_argument('--mem', type=int, default=10, help='Memory in GB (default: 10)')
    args = parser.parse_args()

    if args.t < 1 or args.mem < 1:
        sys.exit("Not an integer number. Please provide only readable integer numbers to call the proper CPUs and Memory.")
    return args

def setup_logging(output_dir):
    log_file = os.path.join(output_dir, 'find_anchor_trim.log')
    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def open_fasta_stream(filepath):
    if filepath.endswith('.gz'):
        return gzip.open(filepath, 'rt')
    elif filepath.endswith('.bz2'):
        return bz2.open(filepath, 'rt')
    elif filepath.endswith(('.fasta', '.fa', '.fna')):
        return open(filepath, 'r')
    elif filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            extracted = z.namelist()[0]
            return z.open(extracted, 'r')
    else:
        sys.exit("Not a proper file format. Please provide a readable file format to call the 'find_anchor_trim module.'")

def read_fasta_file(filepath):
    handle = open_fasta_stream(filepath)
    sequences = []
    for record in SeqIO.parse(handle, 'fasta'):
        sequences.append(str(record.seq))
    if not sequences:
        sys.exit(f"No sequences found in {filepath}")
    return ''.join(sequences).upper()

def write_fasta_file(filepath, header, sequence):
    with open(filepath, 'w') as f:
        f.write(f">{header}\n{sequence}\n")

def smith_waterman_alignment(input_seq, anchor_seq):
    matrix = parasail.matrix_create("ACGTN", 2, -1)
    result = parasail.sw_stats(anchor_seq, input_seq, 10, 1, matrix)
    return result

def find_alignments(args):
    input_anchor, input_seq, anchor_seq = args
    result = smith_waterman_alignment(input_seq, anchor_seq)
    matches = result.matches
    length = result.length
    mismatches = length - matches
    seq_identity = (matches / length) * 100 if length > 0 else 0
    idx_start = result.end_ref - length + 1
    idx_end = result.end_ref + 1
    return {'Input_anchor': input_anchor, 'Idx_start': idx_start, 'Idx_end': idx_end, 'Mism_num': mismatches, 'Seq_idty': seq_identity}

def main():
    args = parse_arguments()
    os.makedirs(args.out, exist_ok=True)
    setup_logging(args.out)
    logging.info(f"Input files: {args.input_fa}, {args.anchor1_fa}, {args.anchor2_fa}")
    logging.info(f"CPUs: {args.t}, Memory: {args.mem}GB")

    input_seq = read_fasta_file(args.input_fa)
    anchor1_seq = read_fasta_file(args.anchor1_fa)
    anchor2_seq = read_fasta_file(args.anchor2_fa)

    input_index_path = os.path.join(args.out, 'input_index.txt')
    with open(input_index_path, 'w') as f:
        f.write(f"Input Index: 1-{len(input_seq)}\n")
    logging.info(f"input_index.txt saved to {input_index_path}")

    tasks = [('Anchor1', input_seq, anchor1_seq), ('Anchor2', input_seq, anchor2_seq)]
    with mp.Pool(args.t) as pool:
        results = pool.map(find_alignments, tasks)

    filtered_results = []
    for res in results:
        if res['Mism_num'] <= 50 and res['Seq_idty'] >= 90:
            res['Seq_idty'] = f"{res['Seq_idty']:.0f}%"
            filtered_results.append(res)

    anchor_match_index_path = os.path.join(args.out, 'anchor_match_index.txt')
    with open(anchor_match_index_path, 'w') as f:
        f.write("Input_anchor\tIdx_start\tIdx_end\tMism_num\tSeq_idty\n")
        for res in filtered_results:
            f.write(f"{res['Input_anchor']}\t{res['Idx_start']}\t{res['Idx_end']}\t{res['Mism_num']}\t{res['Seq_idty']}\n")
    logging.info(f"anchor_match_index.txt saved to {anchor_match_index_path}")

    # Trim logic
    trim_start, trim_end = 0, len(input_seq)
    best_matches = {r['Input_anchor']: r for r in filtered_results}
    if 'Anchor1' in best_matches:
        trim_start = int(best_matches['Anchor1']['Idx_end'])
    if 'Anchor2' in best_matches:
        trim_end = int(best_matches['Anchor2']['Idx_start']) - 1

    trimmed_seq = input_seq[trim_start:trim_end]
    header = next(SeqIO.parse(open_fasta_stream(args.input_fa), 'fasta')).id
    trimmed_input_path = os.path.join(args.out, 'trimmed_input.fa')
    write_fasta_file(trimmed_input_path, header, trimmed_seq)
    logging.info(f"trimmed_input.fa saved to {trimmed_input_path}")
    logging.info("Processing completed successfully.")

if __name__ == "__main__":
    main()
