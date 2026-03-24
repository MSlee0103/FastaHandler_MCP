import sys
import subprocess
from typing import Literal, List
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("FastaHandler")

BASE_DIR = Path(__file__).resolve().parent

def parse_options(option_str: str):
    """
    Convert a string in the 'key=value, key2=value2' format into a dictionary
    """
    options = {}
    if not option_str:
        return options
    
    for part in option_str.split(','):
        part = part.strip()
        if not part: continue
        
        if '=' in part:
            k, v = part.split('=', 1)
            options[k.strip()] = v.strip()

    return options

def run_fastahandler(module_name: str, args: List[str], output_path: Path):
    """
    Command: python <module> <args>
    """
    script_path = BASE_DIR / "scripts" / f"{module_name}.py"

    if not script_path.exists():
        return {
            "status": "failed", 
            "message": f"Script not found: {script_path}",
            "command_executed": "N/A"
        }

    cmd = [sys.executable, str(script_path)] + args
    
    output_dir = str(output_path.parent.absolute())

    try:
        process = subprocess.run(
            cmd,
            cwd=output_dir,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

    except subprocess.CalledProcessError as e:
        return {
            "status": "failed",
            "message": f"Execution failed: {e.stderr}",
            "stderr" : e.stderr,
            "command_executed": " ".join(cmd)
        }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e),
            "command_executed": " ".join(cmd)
        }

    return {
        "status" : "success",
        "command_executed" : " ".join(cmd),
        "output": str(output_path.absolute()),
    }

@mcp.tool()
def assembly_stats(
    input_files: List[Path],
    output: Path,
    mode: Literal["all_fa_stats", "each_fa_stats", "asm_stats_unlimit"],
    options: str = ""
):
    """
    A tool for calculating comprehensive statistics for FASTA files.

    Args:
        input_files: The input file path(s).
            - For 'all_fa_stats' and 'each_fa_stats': Provide a SINGLE file.
            - For 'asm_stats_unlimit':Provide a LIST of multiple file paths (e.g., ["asm1.fa", "asm2.fa"]).

        output: [PATH] Output file path.
            - If not provided, must generate based on the input filename and mode.
            - If provided, the result is saved to this specific path.
            
        mode: The specific module to execute.
            1. 'all_fa_stats':
               The all_fa_stats module generates global FASTA statistics, treating an entire multi-line file as a single dataset.
               It reports sequence length distribution, GC content, N50, L90, nucleotide composition (including ambiguous bases, "n"), and more.
               This provides a comprehensive overview of genome or transcriptome assemblies to aid in assessing assembly quality.

            2. 'each_fa_stats':
               The each_fa_stats module generates per-sequence statistics from multi-line FASTA files.
               It reports metrics such as sequence length, GC content, and base composition for each row (single FASTA entry).
               Useful for identifying unusually long contigs or scaffolds (e.g., before splitting with overlap_split).

            3. 'asm_stats_unlimit':
               The asm_stats_unlimit module extends all_fa_stats to an unlimited number of input files, enabling large-scale comparisons.
               It produces detailed assembly statistics—such as contiguity, completeness, and base composition—for each dataset.
               The output is a structured text file, allowing researchers to compare multiple assemblies in parallel.      

        options: Optional parameters in 'key=value' format, separated by commas. (e.g. "cpu=1, mem=10")
            - 'cpu': Number of CPUs (default: 1).
            - 'mem': Memory in GB (default: 10).
        
        Returns: The execution status and the exact CLI command used.
        - status : Execution status string.
        - command_executed: The EXACT shell command that was run.
        - output: The absolute path to the directory or file generated.
    """

    output.parent.mkdir(parents=True, exist_ok=True)
    params = parse_options(options)

    cpu = str(params.get("cpu", "1"))
    mem = str(params.get("mem", "10"))
    
    args = []

    args.extend(["--out", str(output)])
    args.extend(["--t", cpu])
    args.extend(["--mem", mem])

    if mode in ["all_fa_stats", "each_fa_stats"]:
        args.extend(["--input-seq", str(input_files[0].absolute())])       
    elif mode == "asm_stats_unlimit":
        files = [str(f.absolute()) for f in input_files]
        args.extend(["--input-seqs"])
        args.extend(files)

    return run_fastahandler(mode, args, output)

@mcp.tool()
def concat_and_edit(
    input_files: List[Path],
    output: Path,
    mode: Literal["concatenate_fa", "rename_id", "prefix_pattern_replace", "prefix_rename", "prefix_select_rename"],
    options: str = ""
):
    """
    A comprehensive tool for FASTA file manipulation, including concatenation, renaming, and pattern replacement.

    Args:
        input_files: The input file path(s).
        - For 'concatenate_fa': Provide a LIST of paths (maps to --input-seqs).
        - For 'rename_id', 'prefix_pattern_replace', 'prefix_rename' and 'prefix_select_rename' : Provide a SINGLE path in a list (maps to --input-seq).

        output: [PATH] Output file path.
            - If not provided, must generate based on the input filename and mode.
            - If provided, the result is saved to this specific path.

        mode: The specific manipulation module to execute.
            1. 'concatenate_fa': To make a concatenated fasta file for unlimited fasta files sharing matching prefix IDs.
            2. 'rename_id': To rename prefix IDs and headers from a single-line fasta. Multi-line-formatted FASTA file inputs are converted into the single-line format, and renamed sequences are assigned a sequential numbering (e.g., prefix_1).
            3. 'prefix_pattern_replace': To apply consistent edits across all headers while leaving non-matching entries intact using user-defined search string and user-defined replacement text. 
            4. 'prefix_rename': To rename prefix IDs and headers from a fasta with a user's input text file. It reads a user-supplied, tab-separated mapping file specifying the original and new IDs, replacing each matching header while leaving unmatched entries unchanged.
            5. 'prefix_select_rename': To rename prefix IDs and headers from a fasta with a user's input text file. It applies a user-supplied, tab-separated mapping file to rename only the entries whose IDs/headers are found in both the mapping file and the input FASTA file. Unlike prefix_rename, unmatched entries are discarded, and only mapped sequences are retained.

        options: Parameters in 'key=value' format, separated by commas. (e.g. "cpu=1, mem=10")
            [Common Parameters]
            - 'cpu': Number of CPUs (default: 1). *Note: Not supported by prefix_select_rename.
            - 'mem': Memory in GB (default: 10). *Note: Not supported by prefix_select_rename.

            [Mode-Specific Parameters]
            - 'new_name': [Required for rename_id] A new prefix ID/header name (accept both integer and strings, but no space).
            - 'find_ptrn': [Required for prefix_pattern_replace] A pattern in prefix ID/header name file (accept both integer and strings, but no space).
            - 'replace': [Required for prefix_pattern_replace] A new prefix ID/header name for replacement.
            - 'input_id': [Required for prefix_rename & prefix_select_rename] Path to tab-separated ID mapping file.

        Returns: The execution status and the exact CLI command used.
        - status : Execution status string.
        - command_executed: The EXACT shell command that was run.
        - output: The absolute path to the directory or file generated.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    params = parse_options(options)
    
    args = []
    args.extend(["--out", str(output.absolute())])

    if mode != "prefix_select_rename":
        cpu = str(params.get("cpu", "1"))
        mem = str(params.get("mem", "10"))
        args.extend(["--t", cpu])
        args.extend(["--mem", mem])

    if mode == "concatenate_fa":
        files = [str(f.absolute()) for f in input_files]
        args.extend(["--input-seqs"])
        args.extend(files)
    elif mode == "rename_id":
        new_name = params.get("new_name")
        if not new_name:
            return {"status": "failed", "message": "Missing required option: 'new_name'"}       
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--new-name", str(new_name)])       
    elif mode == "prefix_pattern_replace":
        find_ptrn = params.get("find_ptrn")
        replace = params.get("replace")   
        if not find_ptrn or not replace:
             return {"status": "failed", "message": "Missing options: 'find_ptrn' or 'replace'"}
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--find-ptrn", str(find_ptrn)])
        args.extend(["--replace", str(replace)])    
    elif mode == "prefix_rename":
        input_id = params.get("input_id")
        if not input_id:
            return {"status": "failed", "message": "Missing required option: 'input_id'"}
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--input-id", str(input_id)])   
    elif mode == "prefix_select_rename":
        input_id = params.get("input_id")
        if not input_id:
            return {"status": "failed", "message": "Missing required option: 'input_id'"}
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--input-id", str(input_id)])

    return run_fastahandler(mode, args, output)

@mcp.tool()
def extract_and_translate(
    input_files: List[Path],
    output: Path,
    mode: Literal["chr_pansn_extract", "extract_pattern", "id_extract_multi_location", "translate_dna"],
    options: str = ""
):
    """
    A comprehensive tool for FASTA sequence extraction, translation, and partitioning based on patterns, genomic coordinates, and prefixes.
    
    Args:
        input_files: The input file path(s).
            - For 'extract_pattern', 'id_extract_multi_location', and 'chr_pansn_extract': Provide a SINGLE file path in a list (e.g., ["input.fa"]).
            - For 'translate_dna': Provide a LIST of file paths for one or multiple files (e.g., ["input1.fa", "input2.fa"]).

        output: [PATH] Path to the output file or directory.
            - For 'extract_pattern' and 'id_extract_multi_location': Provide an output FILE path.
            - For 'chr_pansn_extract' and 'translate_dna': Provide an output DIRECTORY path.
            - If not provided, an appropriate path must be generated based on the input filename and mode.

        mode: The specific manipulation module to execute.
            1. 'chr_pansn_extract': To partition pangenome FASTA sequences into groups based on chromosome-like prefixes (e.g., CL). Accepts plain or compressed input files, uses multiprocessing, and generates one FASTA file per prefix group for chromosome-level or pangenome-based analyses.
            2. 'extract_pattern': To filter sequences by length or specified nucleotide (or amino acid) patterns. Automatically converts multi-line FASTA to single-line format, detects both motifs and reverse complements (supporting string/integer queries), and outputs a FASTA file containing only the pattern-matched sequences.
            3. 'id_extract_multi_location': TO further expand ID/header-based extraction functionality to handle multiple IDs and sequence locations simultaneously. Inputs include a tab-delimited file with IDs/headers and their corresponding coordinates, plus the FASTA file to be searched. For long IDs, preprocessing with rename_id is advised.
            4. 'translate_dna': To translate DNA or RNA sequences into protein sequences, supporting both fundamental research and applied biotechnology. It processes a multi-entry FASTA input file and generates translations in all six reading frames, treating “U” as “T.” The module identifies the best open reading frame or the longest protein sequence.

        options: Parameters in 'key=value' format, separated by commas. (e.g. "cpu=4, mem=16, len_over=100")
            [Common Parameters]
            - 'cpu': Specify thread numbers (integer, default: 1).
            - 'mem': Specify memory numbers in GB (integer, default: 10).

            [Mode-Specific Parameters]
            - 'input_ptrn': [Optional for extract_pattern] Path to an input text file to find and filter a specific sequence pattern.
            - 'len_over': [Optional for extract_pattern] Integer specifying a length size to filter out.
            - 'input_ext': [Required for id_extract_multi_location] Path to a tab-separated text file containing the IDs/headers (without ">") and coordinates. *Note: Use -1 value for coordinates due to Python indexing.
            Note: If neither 'input_ptrn' nor 'len_over' is provided for extract_pattern, the input FASTA is returned unchanged.

        Returns: The execution status and the exact CLI command used.
        - status : Execution status string.
        - command_executed: The EXACT shell command that was run.
        - output: The absolute path to the directory or file generated.
    """


    output.parent.mkdir(parents=True, exist_ok=True)
    params = parse_options(options)

    cpu = str(params.get("cpu", "1"))
    mem = str(params.get("mem", "10"))

    args = []
    args.extend(["--out", str(output.absolute())])
    args.extend(["--t", cpu])
    args.extend(["--mem", mem])

    if mode == "chr_pansn_extract":
        args.extend(["--input-fa", str(input_files[0].absolute())])
    elif mode == "extract_pattern":
        input_ptrn = params.get("input_ptrn")
        if input_ptrn:
            args.extend(["--input-ptrn", str(input_ptrn)])
        len_over = params.get("len_over")
        if len_over:
            args.extend(["--len-over", str(len_over)])
        args.extend(["--input-seq", str(input_files[0].absolute())])       
    elif mode == "id_extract_multi_location":
        input_ext = params.get("input_ext")
        if not input_ext:
            return {"status": "failed", "message": "Missing required option: 'input_ext'"}
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--input-ext", str(input_ext)])
    elif mode == "translate_dna":
        files = [str(f.absolute()) for f in input_files]
        args.extend(["--input-seq"])
        args.extend(files)

    return run_fastahandler(mode, args, output)

@mcp.tool()
def remove_and_subset(
    input_files: List[Path],
    output: Path,
    mode: Literal["subset_fa", "remove_duplicate", "find_anchor_trim", "overlap_split"],
    options: str = ""
):
    """
    A comprehensive tool for FASTA file filtration by sequence length, removal of duplicates, extraction of specific regions using anchor sequences, or splitting of long sequences into overlapping pieces.
    
    Args:
        input_files: The input file path(s).
            - Provide a SINGLE file path in a list (e.g., ["input.fa"]).
   
        output: [PATH] Path to the output file or directory.
            - For 'subset_fa' and 'remove_duplicate', 'overlap_split' : Provide an output fasta file path.
            - For 'find_anchor_trim' : Provide an output DIRECTORY path.
            - If not provided, an appropriate path must be generated based on the input filename and mode.

        mode: The specific manipulation module to execute.
            1. 'subset_fa': To filter sequences using a user-defined length threshold, streamlining the analysis of large FASTA files. The output is a FASTA file containing only the sequences from the input file that meet the specified length criteria.
            2. 'remove_duplicate': To eliminate duplicated IDs and sequences from a multi-entry FASTA input file. The output is a deduplicated FASTA file containing only unique entries, providing a reliable foundation for subsequent workflows.
            3. 'find_anchor_trim': To identify and extract genomic regions flanked by user-defined anchor sequences. Anchors are aligned to target sequences using Smith-Waterman scoring, and matches are evaluated by mismatch count and sequence identity. Regions between the anchors are extracted into a trimmed FASTA file output, with all indices and statistics.
            4. 'overlap_split': To divide long FASTA sequences into two overlapping fragments. Each sequence is split at its midpoint, with a user-defined overlap appended to the first fragment. The outputs are two FASTA files (e.g., “*_a.fa” and “*_b.fa”), each in the single-line format with preserved headers.

        options: Parameters in 'key=value' format, separated by commas. (e.g. "cpu=4, mem=16, len_over=100")
            [Common Parameters]
            - 'cpu': Specify thread numbers (integer, default: 1).
            - 'mem': Specify memory numbers in GB (integer, default: 10).

            [Mode-Specific Parameters]
            - 'filter': [Required for subset_fa] A length size to filter out.
            - 'anchor1_fa': [Required for find_anchor_trim] Path to the first anchor fasta file.
            - 'anchor2_fa': [Required for find_anchor_trim] Path to the second anchor fasta file.
            - 'overlap_size': [Required for overlap_split] A user-specified overlap added to the first half to create an overlapping region (Integer).

        Returns: The execution status and the exact CLI command used.
        - status : Execution status string.
        - command_executed: The EXACT shell command that was run.
        - output: The absolute path to the directory or file generated.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    params = parse_options(options)
    
    cpu = str(params.get("cpu", "1"))
    mem = str(params.get("mem", "10"))

    args = []

    args.extend(["--out", str(output.absolute())])
    args.extend(["--t", cpu])
    args.extend(["--mem", mem])

    if mode == "subset_fa":
        filter = params.get("filter")
        if not filter:
            return {"status": "failed", "message": "Missing required option: 'filter'"}
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--filter", str(filter)])
    elif mode == "remove_duplicate":
        args.extend(["--input-seq", str(input_files[0].absolute())])
    elif mode == "find_anchor_trim":
        anchor1_fa = params.get("anchor1_fa")
        if not anchor1_fa:
            return {"status": "failed", "message": "Missing required option: 'anchor1_fa'"}
        anchor2_fa = params.get("anchor2_fa")
        if not anchor1_fa:
            return {"status": "failed", "message": "Missing required option: 'anchor2_fa'"}
        args.extend(["--input-fa", str(input_files[0].absolute())])
        args.extend(["--anchor1-fa", str(anchor1_fa)])
        args.extend(["--anchor2-fa", str(anchor2_fa)])
    elif mode == "overlap_split":
        overlap_size = params.get("overlap_size")
        if not overlap_size:
            return {"status": "failed", "message": "Missing required option: 'overlap_size'"}
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--overlap-size", str(overlap_size)])

    return run_fastahandler(mode, args, output)

@mcp.tool()
def filter_and_sort(
    input_files: List[Path],
    output: Path,
    mode: Literal["find_count_duplicate", "id_extract", "id_extract_location", "size_pattern_search", "find_merge_fa"],
    options: str = ""
):
    """
    A comprehensive tool for FASTA sequence extraction, duplication analysis, pattern searching, and automated merging.
    
    Args:
        input_files: The input file path(s).
            - For 'find_count_duplicate' and 'id_extract', 'id_extract_location', 'size_pattern_search' : Provide a SINGLE file path in a list (e.g., ["input.fa"]).
            - For 'find_merge_fa' : Provide a list containing the path to the input folder that contains multiple fasta files (e.g., ["inputFolder"]).
   
        output: [PATH] Output file path or directory.
            - For 'find_count_duplicate' : Provide a text file path after finding and counting the duplicated IDs and sequences.
            - For 'id_extract' and 'id_extract_location' : Provide a FASTA file path (single-line format) for the extracted sequences.
            - For 'size_pattern_search' : Provide a folder path where the matched FASTA sequences and the statistical summary will be saved.
            - For 'find_merge_fa' : Provide a single merged fasta file path.
            - If not provided, an appropriate path must be generated based on the input filename and mode.

        mode: The specific manipulation module to execute.
            1. 'find_count_duplicate': To identify duplicated IDs or sequences in a FASTA dataset. The results are written to a concise output text file listing duplicated IDs and their occurrence counts. This allows the detection of repeated or redundant sequences, such as duplicated contigs or scaffolds.
            2. 'id_extract': To extract specific sequences from a FASTA file using matched IDs or headers. The user provides a target ID/header (excluding “>”). The output is a FASTA file containing only FASTA entries whose IDs matched the specified IDs/headers.
            3. 'id_extract_location': To extend id_extract by enabling sequence extraction from specific genomic coordinates. The user provides a target ID/header (excluding “>”) along with start and end positions. The output is a FASTA file that includes the extracted subsequence with its corresponding ID/header. 
            4. 'size_pattern_search': To Identify the best direct match of a target sequence within an input FASTA file and count mismatches. Unmatched regions are divided into user-defined chunks, each aligned locally against the input using Biopython's PairwiseAligner. The output is a tab-separated text file that includes global match indices, mismatch counts, and per-chunk similarity statistics. 
            5. 'find_merge_fa': To recursively search user-specified folders for FASTA files matching a user-defined pattern and merge them into a single FASTA file output. The base filename of each input file is preserved as the FASTA header in the merged output. 

        options: Parameters in 'key=value' format, separated by commas. (e.g. "cpu=4, mem=16, len_over=100")
            [Common Parameters]
            - 'cpu': Specify thread numbers (integer, default: 1).
            - 'mem': Specify memory numbers in GB (integer, default: 10).

            [Mode-Specific Parameters]
            - 'input_hdr': [Required for id_extract] Path to the input ID and header (without ">") text file.
            - 'hdr_id': [Required for id_extract_location] An input ID and header (without ">") name and pattern.
            - 'start': [Required for id_extract_location] A start position to extract (Integer).
            - 'end': [Required for id_extract_location] An end position to extract (Integer).
            - 'target_fa': [Required for size_pattern_search] Path to the target fasta file.
            - 'char_size': [Required for size_pattern_search] The chunk size (in bp) to divide unmatched regions of the input sequence for local self-alignment (Integer).
            - 'pattern_fa': [Required for find_merge_fa] A specific filename-matching pattern (e.g., '*.fasta' or '*.fasta.gz'). When providing the pattern, it must be enclosed in quotes(' or ") (e.g., pattern_fa='*.fasta').

        Returns: The execution status and the exact CLI command used.
        - status : Execution status string.
        - command_executed: The EXACT shell command that was run.
        - output: The absolute path to the directory or file generated.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    params = parse_options(options)
    
    cpu = str(params.get("cpu", "1"))
    mem = str(params.get("mem", "10"))

    args = []

    args.extend(["--out", str(output.absolute())])
    args.extend(["--t", cpu])
    args.extend(["--mem", mem])

    if mode == "find_count_duplicate":
        args.extend(["--input-seq", str(input_files[0].absolute())])
    elif mode == "id_extract":
        input_hdr = params.get("input_hdr")
        if not input_hdr:
            return {"status": "failed", "message": "Missing required option: 'input_hdr'"}
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--input-hdr", str(input_hdr)])
    elif mode == "id_extract_location":
        hdr_id = params.get("hdr_id")
        if not hdr_id:
            return {"status": "failed", "message": "Missing required option: 'hdr_id'"}
        start = params.get("start")
        if not start:
            return {"status": "failed", "message": "Missing required option: 'start'"}
        end = params.get("end")
        if not end:
            return {"status": "failed", "message": "Missing required option: 'end'"}
        args.extend(["--input-seq", str(input_files[0].absolute())])
        args.extend(["--hdr-id", str(hdr_id)])
        args.extend(["--start", str(start)])
        args.extend(["--end", str(end)])
    elif mode == "size_pattern_search":
        target_fa = params.get("target_fa")
        if not target_fa:
            return {"status": "failed", "message": "Missing required option: 'target_fa'"}
        char_size = params.get("char_size")
        if not char_size:
            return {"status": "failed", "message": "Missing required option: 'char_size'"}
        args.extend(["--input-fa", str(input_files[0].absolute())])
        args.extend(["--target-fa", str(target_fa)])
        args.extend(["--char-size", str(char_size)])
    elif mode == "find_merge_fa":
        pattern_fa = params.get("pattern_fa")
        if not pattern_fa:
            return {"status": "failed", "message": "Missing required option: 'pattern_fa'"}
        args.extend(["--input-folder", str(input_files[0].absolute())])
        args.extend(["--pattern-fa", str(pattern_fa)])

    return run_fastahandler(mode, args, output)

@mcp.tool()
def reformat(
    input_files: List[Path],
    output: Path,
    mode: Literal["multi2single", "gfa2fa", "reverse_complement", "pangenome_id_rename", "multi2each"],
    options: str = ""
):
    """
    A comprehensive tool for FASTA/GFA transformation, sequence-specific reverse complementation, and automated pangenome fasta file management.
    
    Args:
        input_files: The input file path(s).
            - For 'multi2single', and 'multi2each' : Provide a multi-line fasta path in a list (e.g., ["input.fa"]).
            - For 'gfa2fa' : Provide an input gfa file path in a list (e.g., ["input.gfa"]).
            - For 'reverse_complement' : Provide a SINGLE file path in a list (e.g., ["input.fa"]).
            - For 'pangenome_id_rename' : Provide a pangenome fasta file or a tab-separated (3 columns) text file in a list (e.g., ["input.fa"] or ["input.txt"]).

        output: [PATH] Output file path or directory.
            - For 'multi2single', 'gfa2fa', 'reverse_complement' : Provide an output fasta file path.
            - For 'pangenome_id_rename' : Provide a renamed FASTA header file path.
            - For 'multi2each' : Provide an output folder path where each FASTA header will be saved.

        mode: The specific manipulation module to execute.
            1. 'multi2single': To convert a multi-line-formatted FASTA file into a single-line-formatted FASTA output file, facilitating compatibility across a diverse range of analysis pipelines.
            2. 'gfa2fa': To convert a graphical fragment assembly (GFA) file into a single-line FASTA file output, enabling compatibility with FASTA-specific analysis pipelines. 
            3. 'reverse_complement': To generate strand-specific outputs from a multi-entry FASTA file. It converts input sequences (including ambiguous nucleotides beyond ATGC, regardless of case) into their reverse complements. Inputs are normalised to single-line FASTA format before processing and the final output FASTA file contains correctly oriented reverse-complement sequences with the original identifiers. 
            4. 'pangenome_id_rename': To allow the flexible renaming of IDs and headers in pangenome FASTA or tab-delimited text files. It processes plain or compressed input FASTA files line by line, cleans digits from the first column, and appends haplotype tags (e.g., “#1#” for h1, “#2#” for h2) to form new composite identifiers. The first three columns are joined with underscores and paired with the new ID in a tab-separated output file.
            5. 'multi2each' : To split a multi-entry FASTA file into individual FASTA output files, one per header. Each output file is converted into single-line FASTA format, facilitating use in downstream programs that require individual sequence files. 

        options: Parameters in 'key=value' format, separated by commas. (e.g. "cpu=4, mem=16, len_over=100")
            [Common Parameters]
            - 'cpu': Specify thread numbers (integer, default: 1).
            - 'mem': Specify memory numbers in GB (integer, default: 10).

        Returns: The execution status and the exact CLI command used.
        - status : Execution status string.
        - command_executed: The EXACT shell command that was run.
        - output: The absolute path to the directory or file generated.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    params = parse_options(options)
    
    cpu = str(params.get("cpu", "1"))
    mem = str(params.get("mem", "10"))

    args = []

    args.extend(["--out", str(output.absolute())])
    args.extend(["--t", cpu])
    args.extend(["--mem", mem])

    if mode in ["multi2single", "multi2each"]:
        args.extend(["--input-seq", str(input_files[0].absolute())])
    elif mode == "gfa2fa":
        args.extend(["--input-gfa", str(input_files[0].absolute())])
    elif mode == "reverse_complement":
        args.extend(["--input-seq", str(input_files[0].absolute())])
    elif mode == "pangenome_id_rename":
        args.extend(["--input", str(input_files[0].absolute())])

    return run_fastahandler(mode, args, output)





if __name__ == "__main__":
    mcp.run()