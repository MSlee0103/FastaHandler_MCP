# FastaHandler: created by Hyungtaek Jung
# This script to find unique and similar sequecnes against its own input sequecne.
# Usage: python3 size_pattern_search.py --input-fa input.fa.gz --target-fa target.fa.gz --char-size 100 --out output.txt (default both direction search)

#!/usr/bin/env python3
import argparse, os, sys, gzip, bz2, zipfile, logging
from multiprocessing import Pool, cpu_count
from functools import partial
from Bio import Align
from io import TextIOWrapper

# Setup logging
logging.basicConfig(filename="size_pattern_search.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description='Find mismatches and sequence identity in FASTA sequences.')
    parser.add_argument('--input-fa', required=True, help='Input FASTA file')
    parser.add_argument('--target-fa', required=True, help='Target FASTA file')
    parser.add_argument('--char-size', type=int, required=True, help='Character size for searching')
    parser.add_argument('--out', required=True, help='Output directory')
    parser.add_argument('--t', type=int, default=1, help='CPUs (default: 1)')
    parser.add_argument('--mem', type=int, default=10, help='Memory in GB (default: 10)')
    args = parser.parse_args()

    if args.t < 1 or args.mem < 1:
        sys.exit("Error: Provide positive integers for CPUs and memory.")
    return args

# Decompression supporting stream reading
def open_fasta(filepath):
    if filepath.endswith('.gz'):
        return TextIOWrapper(gzip.open(filepath, 'rb'))
    elif filepath.endswith('.bz2'):
        return TextIOWrapper(bz2.open(filepath, 'rb'))
    elif filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as zf:
            name = zf.namelist()[0]
            return TextIOWrapper(zf.open(name, 'r'))
    else:
        return open(filepath, 'r')

# Read FASTA sequences as a single string (concatenated, lowercase)
def read_sequence(filepath):
    seq = []
    with open_fasta(filepath) as handle:
        for line in handle:
            if not line.startswith('>'):
                seq.append(line.strip().lower())
    return ''.join(seq)

# Match search
def find_match(input_seq, target_seq):
    idx = input_seq.find(target_seq)
    if idx != -1:
        mismatches = sum(1 for a, b in zip(input_seq[idx:idx+len(target_seq)], target_seq) if a != b)
        return idx, idx + len(target_seq) - 1, mismatches
    return -1, -1, len(target_seq)

# Chunk generator
def generate_chunks(seq_len, match_start, match_end, char_size):
    chunks = []
    idx = match_end + 1 if match_end != -1 else 0
    while idx < seq_len:
        chunks.append((idx, min(idx + char_size - 1, seq_len - 1)))
        idx += char_size
    idx = match_start - char_size if match_start != -1 else seq_len - char_size
    while idx >= 0:
        chunks.append((idx, idx + char_size - 1))
        idx -= char_size
    if match_start != -1:
        chunks = [c for c in chunks if c[1] < match_start or c[0] > match_end]
    return sorted(chunks)

# Alignment worker
def align_chunk(chunk_info, aligner):
    chunk_seq, full_seq, chunk_range = chunk_info
    min_mism, max_identity = len(chunk_seq), 0.0
    for i in range(len(full_seq) - len(chunk_seq) + 1):
        if chunk_range[0] <= i <= chunk_range[1]:
            continue  # Skip self-comparison
        window_seq = full_seq[i:i+len(chunk_seq)]
        alignment = aligner.align(chunk_seq, window_seq)[0]
        matches = alignment.score
        identity = (matches / len(chunk_seq)) * 100
        mismatches = len(chunk_seq) - matches
        if mismatches < min_mism:
            min_mism = mismatches
        if identity > max_identity:
            max_identity = identity
        if min_mism == 0 and max_identity == 100:
            break
    return (chunk_range[0], chunk_range[1], min_mism, f"{max_identity:.2f}%")

# Process chunks in parallel
def process_chunks(chunks, full_seq, cpus):
    aligner = Align.PairwiseAligner()
    aligner.mode = 'local'
    aligner.match_score, aligner.mismatch_score = 1, 0
    aligner.open_gap_score, aligner.extend_gap_score = 0, 0
    chunk_data = [(full_seq[start:end+1], full_seq, (start, end)) for start, end in chunks]
    with Pool(cpus) as pool:
        results = pool.map(partial(align_chunk, aligner=aligner), chunk_data)
    return results

# Write output
def write_results(output_dir, input_len, match_info, results):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'Input_Index.txt'), 'w') as f:
        f.write(f"Input Index: 1-{input_len}\n")
    with open(os.path.join(output_dir, 'Input_Match_Index.txt'), 'w') as f:
        if match_info[0] != -1:
            f.write(f"Input Match Index: {match_info[0]+1}-{match_info[1]+1}\n")
        else:
            f.write("Input Match Index: Not Found\n")
        f.write(f"Input Mismatch Number: {match_info[2]}\n")
    with open(os.path.join(output_dir, 'size_unique_search.txt'), 'w') as f:
        f.write("Idx_start\tIdx_end\tMism_num\tSeq_idty\n")
        for s, e, mism, ident in results:
            f.write(f"{s+1}\t{e+1}\t{mism}\t{ident}\n")

def main():
    args = parse_args()
    logging.info(f"Started with CPUs: {args.t}, Memory: {args.mem}GB")
    input_seq = read_sequence(args.input_fa)
    target_seq = read_sequence(args.target_fa)
    match_info = find_match(input_seq, target_seq)
    chunks = generate_chunks(len(input_seq), *match_info[:2], args.char_size)
    results = process_chunks(chunks, input_seq, args.t)
    write_results(args.out, len(input_seq), match_info, results)
    logging.info("Completed successfully.")

if __name__ == "__main__":
    main()
