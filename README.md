# FastaHandler
A collection of Python scripts designed for the efficient management of various FASTA file formats.

![FASTAhandler Logo](https://github.com/OZTaekOppa/FastaHandler/blob/main/images/FASTAhandler_Logo.png)


## Brief Background
**FastaHandler**, developed by Hyungtaek Jung, is a Python toolkit for efficient FASTA file management. It provides 26 dedicated modules to streamline input/output handling, post-processing, and format conversion for FASTA data. Optimised for life science applications, **FastaHandler** is a command-line tool tested across multiple FASTA formats and validated on large datasets (up to 3 Gb human, plant, and animal genomes) using 2 CPUs and 10 GB RAM. For larger datasets, higher computational resources may be required on Linux, HPC, or cloud platforms.


## Objectives
**FastaHandler** enables researchers to perform FASTA manipulations quickly, reproducibly, and at scale, complementing existing bioinformatics tools and supporting high standards of reproducibility in the Next-Generation Sequencing (NGS) era. Although primarily focused on FASTA file manipulation, several modules are also tailored for pangenome input file preparation, expanding its utility in genome assembly and comparative genomics.

## Citation
Hyungtaek Jung. 2025: **FastaHandler**: An easy Python-based toolset for handling fasta files, [TBA](https://www.biorxiv.org/XXXX).


## Contents:
+ [STABLE](https://github.com/OZTaekOppa/FASTAhandler/blob/main/README.md#stable-version-101)
+ [INSTALLATION](https://github.com/OZTaekOppa/FASTAhandler/blob/main/README.md#installation)
+ [LICENSE](https://github.com/OZTaekOppa/FASTAhandler/blob/main/README.md#license) 
+ [GETTING STARTED](https://github.com/OZTaekOppa/FASTAhandler/blob/main/README.md#getting-started)
+ [FAQ](https://github.com/OZTaekOppa/FASTAhandler/blob/main/README.md#faq)
+ [WIKI PAGE](https://github.com/OZTaekOppa/FASTAhandler/blob/main/README.md#wiki-page)
+ [AUTHORS](https://github.com/OZTaekOppa/FASTAhandler/blob/main/README.md#authors)
+ [COPYRIGHT](https://github.com/OZTaekOppa/FASTAhandler/blob/main/README.md#copyright)


## STABLE (version 1.0.1)
- Release date: January 2024
- **FastaHandler** is a standalone Python application equipped with 26 sub-modules for interactive FASTA file manipulation, available as open-source (see [LICENSE](https://github.com/OZTaekOppa/FastaHandler/blob/main/README.md#license)).


## INSTALLATION
- Access the program via [GitHub](https://github.com/OZTaekOppa/FASTAhandler)
- Installation options include Bioconda or Python pip. For support, refer to [Issues on GitHub](https://github.com/OZTaekOppa/FastaHandler/issues).
- **FastaHandler** requires no separate installation process.
- Just clone this repository, and run
```
git clone https://github.com/OZTaekOppa/FASTAhandler/
python3 {path}/fastahandler.py
```

## LICENSE
**FastaHandler** is available under the MIT license and incorporates various open-source software. For detailed information on the integrated Python packages, modules, and libraries, and their specific applications within **FastaHandler**, please refer to the [manuscript](https://www.biorxiv.org/XXXX)


### Tested Datasets
Please refer to the example dataset folder for sample data and usage demonstrations.

### Optional Parameters
		--t: Default is 1 CPU
		--mem: Default is 10 Gb

## GETTING STARTED
**FastaHandler** is developed primarily in Python 3.9+ and Biopython and features 26 modules. It facilitates data input and output through a Command-Line Interface (CLI), ensuring smooth end-to-end file handling. To optimise the use of **FastaHandler**, users should prepare all necessary input files, such as FASTA and TXT formats, in advance.

![FASTAhandler Workflow](https://github.com/OZTaekOppa/FastaHandler/blob/main/images/FASTAhandler_Workflow.png)

### General Usage
```
FastaHandler: Fasta File Manipulation Toolkit
version 1.0.1

Usage: python3 fastahandler.py <module> <parameters>

Modules:
AllFastaStats	|	 all_fa_stats	|	Generate a summary of multi-line fasta statistics.
AssemblyStatsUnlimit	|	 asm_stats_unlimit	|	Generate a summary of multi-line fasta statistics (Multiple).
ChrPanSpecNameExtract	|	 chr_pansn_extract	|	Make sequence partition based on the name of prefix (CL) in the fasta header.
ConcatenateFasta	|	 concatenate_fa	|	Make a concatenated fasta file (Multiple).
EachFastaStats	|	 each_fa_stats	|	Generate each line fasta statistic for a multi-line fasta.
ExtractPattern	|	 extract_pattern	|	Make a subset of data with find, filter and extract.
FindAnchorTrim	|	 find_anchor_trim	|	Make a subset of fasta with find, anchor, trim, and extract.
FindCountDuplication	|	 find_count_duplicate	|	Find and count the duplicated IDs and sequences.
FindMergeFasta	|	 find_merge_fa	|	Find and merge fasta files if they match a certain pattern.
Gfa2Fasta	|	 gfa2fa	|	Convert a gfa into a single-line fasta.
IdExtractLocation	|	 id_extract_location	|	Extract matched IDs, locations and their corresponding sequences.
IdExtractLocationMultiple	|	 id_extract_multi_location	|	Extract matched IDs, locations and their corresponding sequences (Multiple).
IdExtract	|	 id_extract	|	Extract matched IDs and their corresponding sequences.
Multiple2Each	|	 multi2each	|	Convert a multi-fasta file to a each (split) fasta.
Multiple2Single	|	 multi2single	|	Convert a multi-fasta (multiline) file to a single-line fasta.
OverlapSplit	|	 overlap_split	|	Convert a multi-fasta (multiline) file to a single-line fasta.
PangenomeIdRename	|	 pangenome_id_rename	|	Rename prefix IDs and headers for a Pangenome format.
PrefixPatternReplace	|	 prefix_pattern_replace	|	Replace and rename prefix IDs and headers with a user’s input (Only).
PrefixRename	|	 prefix_rename	|	Rename prefix IDs and headers with a user’s input.
PrefixSelectRename	|	 prefix_select_rename	|	Rename prefix IDs and headers with a user’s input (Only).
RemoveDuplication	|	 remove_duplicate	|	Remove the duplicated IDs and sequences.
RenameId	|	 rename_id	|	Rename prefix IDs and headers.
ReverseComplement	|	 reverse_complement	|	Make a reverse complement sequence.
SizePatternSearch	|	 size_pattern_search	|	Find unique and similar sequences against its own input sequence
SubsetFasta	|	 subset_fa	|	Make a subset of data with a sequence length filter.
TranslateSequence	|	 translate_dna	|	Find the translated sequences as a protein and open reading frames (ORFs).


Use <module> --help for module usage.
```

### all_fa_stats
- To generate a summary of multi-line fasta statistics. 
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A multi-line fasta file.
	+ Output: A summary of multi-line fasta with its diverse statistics (e.g. sequence length, GC content, N50, L90, and more).
  	+ Example file: [all_stat_asm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/all_stat_asm.fa) and [stat_asm_mlt_unlm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/stat_asm_mlt_unlm.fa) in the "example_data" folder.

Example usage
```
python3 all_fa_stats.py --input-seq test_dna.fasta --out output_dna.txt --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).
+ Both eachfastats and allfastasts modules use the same multi-line FASTA input. Eachfastats focuses on individual FASTA lines and their sequence lengths, while allfastasts provides a summary of assembly statistics, such as for genomes or transcriptomes.

- Parameter explanation
	1. Python 3: Call Python 3
	1. all_fa_stats.py:  Call the all_fa_stats module
	1. python3 all_fa_stats.py --help: Check help menu
		+ --input-seq: Indicate an input multi-line fasta file and its path
		+ --out: Indicate an output text file with the summary of statistics
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### asm_stats_unlimit
- To generate a summary of multi-line fasta statistics for unlimited fasta files. An extended version of all_fa_stats for multiple FASTA files. 
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: Unlimited multi-line fasta files.
	+ Output: A summary of multi-line fasta with its diverse statistics (e.g. sequence length, GC content, N50, and more).
  	+ Example file: [all_stat_asm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/all_stat_asm.fa) and [stat_asm_mlt_unlm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/stat_asm_mlt_unlm.fa) in the "example_data" folder.

Example usage
```
python3 asm_stats_unlimit.py --input-seqs test_dna1.fasta test_dna2.fasta test_dna3.fasta test_dna4.fasta test_dna5.fasta --out output_dna.txt --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).
+ Both all_fa_stats and asm_stats_unlimit modules take the same multi-line FASTA files. all_fa_stats generates a summary of assembly statistics from a single FASTA file, while asm_stats_unlimit does so for multiple FASTA files, useful for genome or transcriptome analysis.

- Parameter explanation
	1. Python 3: Call Python 3
	1. asm_stats_unlimit.py:  Call the asm_stats_unlimit module
	1. python3 asm_stats_unlimit.py --help: Check help menu
		+ --input-seqs: Indicate an input multi-line fasta file and its path (Separated by a space for each new fasta file)
		+ --out: Indicate an output text file with the summary of statistics
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### chr_pansn_extract
- To make a sequence partition based on the name of a prefix (e.g. CL:) in the fasta header, especially for pangenome spec names. 
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: Pangenome spec named multi-line fasta files.
	+ Output: A clean set of per-group FASTA files for downstream pangenome or chromosome-level analyses.
  	+ Example file: [chr_pansn_asm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/chr_pansn_asm.fa) in the "example_data" folder.

Example usage
```
python3 chr_pansn_extract.py --input-fa test_asm.fasta --output Outfolder --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).
+ Please note that the chr_pansn_extract module groups sequences by CL prefix. While it is useful for pangenome, genome and transcriptome analyses, users need to modify the prefix name based on their requirement. 

- Parameter explanation
	1. Python 3: Call Python 3
	1. chr_pansn_extract.py:  Call the chr_pansn_extract module
	1. python3 chr_pansn_extract.py --help: Check help menu
		+ --input-fa: Indicate an input multi-line fasta file and its path (Separated by a space for each new fasta file)
		+ --out: A clean set of per-group fasta with extracted IDs and their corresponding sequences.
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### concatenate_fa
- To make a concatenated fasta file for unlimited fasta files. 
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: Multiple fasta files with the same prefix IDs.
	+ Output: A single-line fasta with concatenated IDs and their corresponding sequences.
  	+ Example file: [concat_seq1.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/concat_seq1.fa), [concat_seq2.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/concat_seq2.fa), [concat_seq3.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/concat_seq3.fa), [concat_seq4.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/concat_seq4.fa), and [concat_seq1.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/concat_seq5.fa) in the "example_data" folder.

Example usage
```
python concatenate_fa.py --input-seqs test_dna1.fasta test_dna2.fasta test_dna3.fasta test_dna4.fasta test_dna5.fasta --out output_concat.fasta --t 1 --mem 10
```
+ For the best use of this module, please make sure that all input FASTA files have matching prefix IDs and headers and are formatted as single-line FASTA before concatenation.
+ Before using the concatenate module, ensure your FASTA files are in single-line format by using the renameid and multi2singleline modules, even though the pipeline automatically converts multi-line FASTA files.

- Parameter explanation
	1. Python 3: Call Python 3
	1. concatenate_fa.py:  Call the concatenate_fa module
	1. python3 concatenate_fa.py --help: Check help menu
		+ --input-seqs: Indicate input multiple single-line fasta files and their path (Separated by a space for each new fasta file)
		+ --out: Indicate a concatenated output fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### each_fa_stats
- To generate each line fasta statistics for each line of a multi-line fasta
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A multi-line fasta file.
	+ Output: A summary of single-line fasta with its corresponding sequence length.
	+ Example file: [all_stat_asm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/all_stat_asm.fa) and [stat_asm_mlt_unlm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/stat_asm_mlt_unlm.fa) in the "example_data" folder.

Example usage
```
python3 each_fa_stats.py --input-seq test_dna.fasta --out output_dna.txt --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. each_fa_stats.py:  Call the each_fa_stats module
	1. python3 each_fa_stats.py --help: Check help menu
		+ --input-seq: Indicate an input multi-line fasta file and its path
		+ --out: Indicate an output text file with the sequence length
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### extract_pattern
- To make a subset of data with find, filter and extract options
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file and a list of patterns.
	+ Output: A extracted single-line fasta with IDs and their corresponding sequences.
 	+ Example file: [find_ptrn.txt](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/find_ptrn.txt), [find_ptrn_mlt.txt
](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/find_ptrn_mlt.txt), [find_ptrn_mlt_seq.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/find_ptrn_mlt_seq.fa), and [find_ptrn_seq.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/find_ptrn_seq.fa) in the "example_data" folder.

Example usage
```
python3 extract_pattern.py --input-seq test_dna1.fasta --input-ptrn seq_pattern.txt --len-over 45 --out output_pattern.fasta --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. extract_pattern.py:  Call the extract_pattern module
	1. python3 extract_pattern.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path (accept reverse complement sequences)
		+ --input-ptrn: Indicate an input text file and its path to find and filter a specific sequence pattern (accept reverse complement sequences)
		+ --len-over: Indicate a length size to filter out
		+ --out: Indicate an output fasta file after filtering the length size (integer only)
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### find_anchor_trim
- To generate a trimmed sequence from two anchor sequences and positions, considering mismatches, identity and alignment statistics. 
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A single-line reference fasta file and two anchor fasta sequences. 
	+ Output: A trimmed sequence along with its summary text file (e.g. indexes, mismatches, identity and alignment statistics).
  	+ Example file: [anchor_ref_asm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/anchor_ref_asm.fa), [find_anchor1.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/find_anchor1.fa), and [find_anchor2.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/find_anchor2.fa) in the "example_data" folder.

Example usage
```
python3 find_anchor_trim.py --input-fa ref_seq.fa --anchor1-fa anchor1_seq.fa --anchor2-fa anchor2_seq.fa --out ./ --t 1 --mem 10
```
+ If your input reference and anchor FASTA files are in multi-line format, the script will automatically convert them to single-line format for processing (embedded pipeline).
+ A trimmed sequence and its summary of anchor-defined genomic regions for downstream analyses will be saved.

- Parameter explanation
	1. Python 3: Call Python 3
	1. find_anchor_trim.py:  Call the find_anchor_trim module
	1. python3 find_anchor_trim.py --help: Check help menu
		+ --input-fa: Indicate a reference input fasta file and its path
  		+ --anchor1-fa: Indicate the first anchor fasta file and its path
    	+ --anchor2-fa: Indicate the second anchor fasta file and its path
		+ --out: Indicate an output folder (a trimmed sequence with the summary of statistics)
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### find_count_duplicate
- To find and count the duplicated IDs and sequences from a multi-fasta file
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file.
	+ Output: A text with a duplication number.
	+ Example file: [dupids.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/dupids.fa) in the "example_data" folder.

Example usage
```
python3 find_count_duplicate.py --input-seq test_dna2.fasta --out output_files.txt --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. find_count_duplicate.py:  Call the find_count_duplicate module
	1. python3 find_count_duplicate.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path (accept reverse complement sequences)
		+ --out: Indicate an output text file after finding and counting the duplicated IDs and sequences (only for both matched IDs and their corresponding sequences)
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### find_merge_fa
- To generate a merged fasta file from multiple fasta files in the same folder with a specific filename-matching pattern (*asm_chr1.fa in the --pattern-fa). 
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A folder that contains multiple fasta files 
	+ Output: A clean merged fasta file grouping by the specific file-name matching patterns (e.g. prefix name of the file: *asm_chr1.fa).
  	+ Example file: An indication of the specific filename-matching pattern in the --pattern-fa (e.g. *asm_chr1.fa) is required.

Example usage
```
python3 find_merge_fa.py --input-folder ./ --pattern-fa "*asm_chr1.fasta" --out ./output_merge_files.fa --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. find_merge_fa.py:  Call the find_merge_fa module
	1. python3 find_merge_fa.py --help: Check help menu
		+ --input-folder: Indicate an input folder that contains multiple fasta files
        + --pattern-fa: Indicate a specific filename-matching pattern
		+ --out: Indicate an output merged fasta file
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### gfa2fa
- To convert a gfa (Graphical Fragment Assembly) into a single-line fasta.
	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A gfa file.
	+ Output: A single-line fasta.
	+ Example file: [gfa2fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/gfa2fa.gfa) in the "example_data" folder. 

Example usage
```
python3 gfa2fa.py --input-gfa test_dna.gfa --out test_output_sl.fasta --t 1 --mem 10
```

- Parameter explanation
	1. Python 3: Call Python 3
	1. gfa2fa.py:  Call the gfa2fa module
	1. python3 gfa2fa.py --help: Check help menu
		+ --input-gfa: Indicate an input gfa file and its path
		+ --out: Indicate an output single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### id_extract_location
- To extract matched IDs, locations and their corresponding sequences (focused on a single ID)
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file and a list of IDs.
	+ Output: A single-line fasta with extracted IDs and their corresponding sequences.
	+ Example file: [header_id.txt](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/header_id.txt) and [idextloct.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/idextloct.fa) in the "example_data" folder.

Example usage
```
python3 id_extract_location.py --input-seq test_dna.fasta --header-id test3_3%week --start 2 --end 10 --out output_test.fasta --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. id_extract_location.py:  Call the id_extract_location module
	1. python3 id_extract_location.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path
		+ --header-id: Indicate an input ID and header (without ">") name and pattern
		+ --start: Indicate a start position to extract (please use -1 value due to the Python index)
		+ --end: Indicate an end position to extract (please use -1 value due to the Python index)
		+ --out: Indicate an output ID matched and extracted single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)
	

### id_extract_multi_location
- To extract matched IDs, locations and their corresponding sequences (focused on multiple IDs)
  	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file and a list of IDs.
	+ Output: A single-line fasta with extracted IDs and their corresponding sequences.
 	+ Example file: [hdrmulti_id.txt](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/hdrmulti_id.txt), [idextract.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/idextract.fa) and [idextloct.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/idextloct.fa) in the "example_data" folder.

Example usage
```
python3 id_extract_multi_location.py --input-seq test_dna.fasta --input-extract input_ext.txt --out output_extest.fasta --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. id_extract_multi_location.py:  Call the id_extract_multi_location module
	1. python3 id_extract_multi_location.py --help: Check help menu
	--input-seq: Indicate an input single-line fasta file and its path
	--input-ext: Indicate an input ID and header (without ">") text file (a tab-separated) and its path, including start and end positions (please use -1 value due to the Python index)
	--out: Indicate an output ID matched and extracted single-line fasta file and its path
	--t: Specify thread numbers (integer only)
	--mem: Specify memory numbers (integer only with Gb size)


### id_extract
- To extract matched IDs and their corresponding sequences.
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file and a list of IDs.
	+ Output: A single-line fasta with extracted IDs and their corresponding sequences.
 	+ Example file: [header_id.txt](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/header_id.txt) and [idextract.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/idextract.fa) in the "example_data" folder.

Example usage
```
python3 id_extract.py --input-seq test_dna.fasta --input-hdr header_id.txt --out output_extracted.fasta --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).
	
- Parameter explanation
	1. Python 3: Call Python 3
	1. id_extract.py:  Call the id_extract module
	1. python3 id_extract.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path
		+ --input-hdr: Indicate an input ID and header (without ">") text file and its path
		+ --out: Indicate an output ID matched and extracted single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### multi2each
- To convert a multi-line FASTA into a single-line format with each FASTA header.
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A multi-line fasta file.
	+ Output: A single-line format for each FASTA header.
  	+ Example file: [all_stat_asm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/all_stat_asm.fa) and [stat_asm_mlt_unlm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/stat_asm_mlt_unlm.fa) in the "example_data" folder.

Example usage
```
python3 multi2each.py --input-seq test.fa --out output_dir --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. multi2each.py:  Call the multi2each module
	1. python3 multi2each.py --help: Check help menu
		+ --input-seqs: Indicate an input multi-line fasta file and its path
		+ --out: Indicate an output folder with each FASTA header
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### multi2single
- To convert a multi-fasta (multiline) into a single-line fasta.
	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A multiline fasta file.
	+ Output: A single-line fasta.
	+ Example file: [mltseq2sl](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/mltseq2sl.fa) in the "example_data" folder. 

Example usage
```
python3 multi2single.py --input-seq test_dna.fasta --out test_output_sl.fasta --t 1 --mem 10
```

- Parameter explanation
	1. Python 3: Call Python 3
	1. multi2single.py:  Call the multi2single module
	1. python3 multi2singleline.py --help: Check help menu
		+ --input-seq: Indicate an input multi-fasta (multiline) fasta file and its path
		+ --out: Indicate an output single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### overlap_split
- To generate split overlapping fragments from a long single-FASTA sequence, with a user-specified overlapping size.
- Two new FASTA files (e.g. *_a.fa and *_b.fa) are generated for every sequence, preserving safe, clean versions of the original headers.
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A long single-FASTA sequence file.
	+ Output: Paired FASTA files by overlapping size, with a summary of index and overlapping statistics.
  	+ Example file: [anchor_ref_asm.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/anchor_ref_asm.fa) in the "example_data" folder.

Example usage
```
python3 overlap_split.py --input-seq test.fa --overlap-size 1000 --out output_dir --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).
+ Please note that the --overlap-size should be >= 0.

- Parameter explanation
	1. Python 3: Call Python 3
	1. overlap_split.py:  Call the aoverlap_split module
	1. python3 overlap_split.py --help: Check help menu
		+ --input-seqs: Indicate an input long single-FASTA sequence file
        + --overlap-size: A user-specified overlap added to the first half to create an overlapping region
		+ --out: Indicate an output folder with the summary of overlap statistics
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### pangenome_id_rename
- To generate a pangenome fasta header (re)name (#1# for “h1”, #2# for “h2”) using a tab-delimited text file and underscores to satisfy the [panSN-spec](https://github.com/pangenome/PanSN-spec).
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A tab-separated (3 columns) text file.
	+ Output: A renamed FASTA header file for pangnome.
  	+ Example file: [pangenome_id_rename.txt](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/pangenome_id_rename.txt) in the "example_data" folder.

Example usage
```
python3 pangenome_id_rename.py --input test.txt --out output_dir --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).
+ This module is to rename the fasta header text file for pangenome, then as an input for prefix_slect_rename.py.

- Parameter explanation
	1. Python 3: Call Python 3
	1. pangenome_id_rename.py:  Call the pangenome_id_rename module
	1. python3 pangenome_id_rename.py --help: Check help menu
		+ --input: Indicate a tab-separated (3 columns) text file.
		+ --out: Indicate an output folder with the renamed fasta headers
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### prefix_pattern_replace
- To rename prefix IDs and headers from a single-line fasta with a user's input text file.
	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file and a find and replace pattern (e.g. old_IDs	new_IDs)
	+ Output: A single-line fasta with a new prefix ID name based on the user's input text file. Worked as the "sed" command.
 	+ Example file: [header_id_only.txt](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/header_id_only.txt) in the "example_data" folder.

Example usage
```
python3 prefix_pattern_replace.py --input-seq --find-ptrn hifiasm --replace Assembly --out output_reN.fasta --t 1 --mem 10
```
+ Although the script can process multiline FASTA files, if you're unsure about your input FASTA file format, it's recommended to first convert it to single-line format using the multi2single module.
+ The script is effective for selectively renaming IDs/headers in FASTA files (with a user's specific input), such as genome assemblies from databases, where you want to exclude and not rename certain elements like scaffolds.

- Parameter explanation
	1. Python 3: Call Python 3
	1. prefix_pattern_replace.py:  Call the prefix_pattern_replace module
	1. python3 prefix_pattern_replace.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path
		+ --find-ptrn: Indicate a pattern in prefix ID/header name file (accept both integer and strings, but no space)
  		+ --replace: Indicate a new prefix ID/header name for replacement
		+ --out: Indicate an output renamed single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### prefix_rename
- To rename prefix IDs and headers from a single-line fasta with a user's input text file.
	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file and a tab-separated text file (e.g. old_IDs	new_IDs)
	+ Output: A single-line fasta with a new prefix ID name based on the user's input text file. Unmatched IDs will also be produced with their original IDs.
	+ Example file: [header_id_only.txt](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/header_id_only.txt) in the "example_data" folder.

Example usage
```
python3 prefix_rename.py --input-seq test_dna.fasta --input-id new_ids.txt --out output_reN.fasta --t 1 --mem 10
```
+ Although the script can process multiline FASTA files, if you're unsure about your input FASTA file format, it's recommended to first convert it to single-line format using the multi2single module.
+ The script is ideal for renaming specific parts of IDs/headers in FASTA files, such as those from genome assemblies acquired from public databases like NCBI and EBI, based on user input.

- Parameter explanation
	1. Python 3: Call Python 3
	1. prefix_rename.py:  Call the prefix_rename module
	1. python3 prefix_rename.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path
		+ --input-id: Indicate a new tap-separated prefix ID/header name file (accept both integers and strings, but no space)
		+ --out: Indicate an output renamed single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)

### prefix_select_rename
- To rename prefix IDs and headers from a single-line fasta with a user's input text file.
	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file and a tab-separated text file (e.g. old_IDs	new_IDs)
	+ Output: A single-line fasta with a new prefix ID name based on the user's input text file. Unmatched IDs will be discarded.
 	+ Example file: [header_id_only.txt](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/header_id_only.txt) in the "example_data" folder.

Example usage
```
python3 prefix_select_rename.py --input-seq test_dna.fasta --input-id new_ids.txt --out output_reN.fasta --t 1 --mem 10
```
+ Although the script can process multiline FASTA files, if you're unsure about your input FASTA file format, it's recommended to first convert it to single-line format using the multi2single module.
+ The script is effective for selectively renaming IDs/headers in FASTA files (with a user's specific input), such as genome assemblies from databases, where you want to exclude and not rename certain elements like scaffolds.

- Parameter explanation
	1. Python 3: Call Python 3
	1. prefix_select_rename.py:  Call the prefix_select_rename module
	1. python3 prefix_select_rename.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path
		+ --input-id: Indicate a new tap-separated prefix ID/header name file (accept both integers and strings, but no space)
		+ --out: Indicate an output renamed single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### remove_duplicate
- To remove the duplicated IDs and sequences from a multi-fasta file
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file.
	+ Output: A single-line fasta after removing updated IDs and sequences.
 	+ Example file: [rmvdup.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/rmvdup.fa) in the "example_data" folder.

Example usage
```
python3 remove_duplicate.py --input-seq test_dna2.fasta --out output_testdupl.fasta --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. remove_duplicate.py:  Call the remove_duplicate module
	1. python3 remove_duplicate.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path (accept reverse complement sequences)
		+ --out: Indicate an output fasta file after removing the duplicated IDs and sequences (only for both matched IDs and their corresponding sequences)
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)
  
### rename_id
- To rename prefix IDs and headers from a single-line fasta.
	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file.
	+ Output: A single-line fasta with a new prefix ID name.
 	+ Example file: [renameid_seq.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/renameid_seq.fa) in the "example_data" folder. 


Example usage
```
python3 rename_id.py --input-seq test_dna.fasta --new-name FunNGS --out output_reN.fasta --t 1 --mem 10
```
+ Use the multi2single module first if your input FASTA file isn't in single-line format.

- Parameter explanation
	1. Python 3: Call Python 3
	1. rename_id.py:  Call the rename_id module
	1. python3 rename_id.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path
		+ --new-name: Indicate a new prefix ID/header name (accept both integer and strings, but no space)
		+ --out: Indicate an output renamed single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### reverse_complement
- To make a reverse complement sequence
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file.
	+ Output: A reverse complement single-line fasta.
 	+ Example file: [revscomplt.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/revscomplt.fa) in the "example_data" folder.

Example usage
```
python3 reverse_complement.py --input-seq test_dna.fasta --out output_revctest.fasta --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. reverse_complement.py:  Call the reverse_complement module
	1. python3 reverse_complement.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path
		+ --out: Indicate a reverse complement converted output single-line fasta file and its path
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### size_pattern_search
- To detect the best match of a target (unique pattern or character) in an input FASTA, split unmatched regions into chunks, and use local alignment with parallel processing to compute mismatches and identity.
- To produce tab-separated outputs of match indices, mismatch counts, and similarity stats—supporting probe/primer design, structural-variant detection, repeat analysis, and downstream genomics workflows.
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A multi-line fasta file.
	+ Output: A matched fasta sequence with a summary of match indices, mismatch counts, and similarity. 
  	+ Example file: [size_ptrn_full_seq.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/size_ptrn_full_seq.fa) and [size_ptrn_target_seq.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/size_ptrn_target_seq.fa) in the "example_data" folder.

Example usage
```
python3 size_pattern_search.py --input-fa input.fa.gz --target-fa target.fa.gz --char-size 100 --out output.txt --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. size_pattern_search.py:  Call the size_pattern_search module
	1. python3 size_pattern_search.py --help: Check help menu
		+ --input-fa: Indicate an input multi-line fasta file and its path
        + --target-fa: Indicate a target fasta file
        + --char-size: Indicate a character size for searching between input and target fasta files
		+ --out: Indicate an output folder of matched fasta sequence with a summary of statistics. 
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### subset_fa
- To make a subset of data with a sequence length filter option
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: A fasta file.
	+ Output: A subsetted single-line fasta.
 	+ Example file: [subsetfa.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/subsetfa.fa) in the "example_data" folder.

Example usage
```
python3 subset_fa.py --input-seq test_mRNA1.fasta --filter 50 --out output_subset.fasta --t 1 --mem 10
```
+ If your input FASTA file is in multi-line format, the script will automatically convert it to single-line format for processing (embedded pipeline).

- Parameter explanation
	1. Python 3: Call Python 3
	1. subset_fa.py:  Call the subset_fa module
	1. python3 subset_fa.py --help: Check help menu
		+ --input-seq: Indicate an input single-line fasta file and its path (accept reverse complement sequences)
		+ --filter: Indicate a length size to filter out
		+ --out: Indicate an output fasta file after filtering the length size (integer only)
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


### translate_dna
- To find the translated sequences as a protein, including the open reading frames (ORFs)
 	+ Requirement: The Python/bash script requires a Python library.
	+ Input: Multiline fasta files.
	+ Output: A single-line fasta with translation and selected ORFs (nucleotide and protein sequences).
	+ Example file: [trnsldna.fa](https://github.com/OZTaekOppa/FastaHandler/blob/main/example_data/trnsldna.fa) in the "example_data" folder.

Example usage
```
python translate_dna.py --input-seq test_dna.fasta --out output/folder --t 1 --mem 10
```
+ For optimal use of this module, ensure that all input FASTA files have matching prefix IDs and headers and are formatted as single-line FASTA before concatenation.
+ Before using the translatedna module, ensure your FASTA files are in single-line format by using the renameid and multi2singleline modules, even though the pipeline automatically converts multi-line FASTA files.

- Parameter explanation
	1. Python 3: Call Python 3
	1. translate_dna.py:  Call the translate_dna module
	1. python3 translate_dna.py --help: Check help menu
		+ --input-seq: Indicate input single-line fasta files and their path
		+ --out: Indicate a translated output fasta file and its path (a total of four fasta files for both nucleotide and protein sequences)
		+ --t: Specify thread numbers (integer only)
		+ --mem: Specify memory numbers (integer only with Gb size)


## FAQ

We encourage users to use the [Issues](https://github.com/OZTaekOppa/FastaHandler/issues).


## WIKI PAGE

Please see the GitHub page.


## AUTHOR(S)

**Hyungtaek Jung**.


## COPYRIGHT

The full **FastaHandler** is distributed under the MIT license. 
