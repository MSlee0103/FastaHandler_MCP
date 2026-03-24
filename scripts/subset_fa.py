# FastaHandler: created by Hyungtaek Jung
# Subset based on sequence length from a multi-fasta (multiline) file
# Example usage: python subset_fa.py --input-seq test_mRNA1.fasta --filter 50 --out output_subset.fasta --t 1 --mem 2

#!/usr/bin/env python3
import argparse
import os
import logging
import gzip
import bz2
import zipfile
from multiprocessing import Pool, cpu_count
from Bio import SeqIO
from io import TextIOWrapper

# Setup logging
logging.basicConfig(filename="subset_fa_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s")

def open_fasta(file_path):
    """Open compressed or uncompressed fasta files for reading."""
    if file_path.endswith('.gz'):
        return TextIOWrapper(gzip.open(file_path, 'rb'))
    elif file_path.endswith('.bz2'):
        return TextIOWrapper(bz2.open(file_path, 'rb'))
    elif file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as z:
            name_list = z.namelist()
            if len(name_list) != 1:
                raise ValueError("Zip file should contain exactly one fasta file.")
            return TextIOWrapper(z.open(name_list[0], 'r'))
    else:
        return open(file_path, 'r')

def filter_record(record, min_len):
    """Filter records based on sequence length."""
    return len(record.seq) >= min_len

def process_records(records, min_len):
    """Filter records and collect matching sequences."""
    return [f">{rec.id}\n{str(rec.seq)}\n" for rec in records if filter_record(rec, min_len)]

def chunk_iterator(iterator, chunk_size):
    """Yield chunks of records from an iterator."""
    chunk = []
    for record in iterator:
        chunk.append(record)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

def worker_process(chunk, min_len):
    """Process chunk of records in a worker process."""
    return process_records(chunk, min_len)

def main(input_seq, filter_length, output_file, num_processes, memory):
    logging.info(f"Input file: {input_seq}")
    logging.info(f"Filter length: {filter_length}")
    logging.info(f"Output file: {output_file}")
    logging.info(f"CPUs: {num_processes}, Memory: {memory}GB")

    # Determine CPUs
    num_processes = max(1, num_processes or cpu_count())

    with open_fasta(input_seq) as handle:
        record_iterator = SeqIO.parse(handle, "fasta")

        # Chunk records for multiprocessing
        chunk_size = 1000  # Adjustable chunk size for each process
        chunks = list(chunk_iterator(record_iterator, chunk_size))

    with Pool(processes=num_processes) as pool:
        results = pool.map(partial(worker_process, min_len=filter_length), chunks)

    # Write output in one go
    with open(output_file, 'w') as f_out:
        for filtered_seqs in results:
            f_out.writelines(filtered_seqs)

    logging.info("Processing completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subset FASTA files based on sequence length.")
    parser.add_argument("--input-seq", required=True, help="Input sequence file path.")
    parser.add_argument("--filter", type=int, required=True, help="Minimum sequence length.")
    parser.add_argument("--out", required=True, help="Output FASTA file path.")
    parser.add_argument("--t", type=int, default=1, help="CPUs (default: 1).")
    parser.add_argument("--mem", type=int, default=10, help="Memory in GB (default: 10).")
    args = parser.parse_args()

    main(args.input_seq, args.filter, args.out, args.t, args.mem)
