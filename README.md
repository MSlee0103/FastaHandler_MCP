# FastaHandler MCP Server

A [Model Context Protocol (MCP)](https://www.anthropic.com/news/model-context-protocol) server that exposes all 26 **FastaHandler** modules as natural language–accessible tools for LLM clients such as Claude Desktop and Cursor.

> **FastaHandler** is a lightweight, Python-based toolkit for FASTA file manipulation in genomic and pangenome research.  
> Main repository: [https://github.com/OZTaekOppa/FASTAhandler](https://github.com/OZTaekOppa/FASTAhandler)

---

## Overview

The FastaHandler MCP server wraps all 26 CLI modules into **6 grouped tool functions**, allowing users to execute any module through natural language prompts — no command-line expertise required.

| MCP Tool Function | FastaHandler Modules |
|---|---|
| `assembly_stats` | `all_fa_stats`, `each_fa_stats`, `asm_stats_unlimit` |
| `concat_and_edit` | `concatenate_fa`, `rename_id`, `prefix_pattern_replace`, `prefix_rename`, `prefix_select_rename`, `pangenome_id_rename` |
| `extract_and_translate` | `chr_pansn_extract`, `extract_pattern`, `id_extract`, `id_extract_location`, `id_extract_multi_location`, `translate_dna` |
| `remove_and_subset` | `find_count_duplicate`, `remove_duplicate`, `subset_fa`, `multi2each`, `multi2single` |
| `filter_and_sort` | `find_anchor_trim`, `find_merge_fa`, `size_pattern_search`, `overlap_split`, `gfa2fa` |
| `reformat` | `reverse_complement` |

Each tool accepts a `mode` parameter (module name), input/output paths, and optional `key=value` arguments that are resolved into CLI commands and executed via subprocess.

---

## Requirements

- Python 3.9+
- [FastaHandler](https://github.com/OZTaekOppa/FASTAhandler)
- [FastMCP](https://github.com/jlowin/fastmcp)
- An MCP-compatible client (e.g., [Claude Desktop](https://claude.ai/download), [Cursor](https://www.cursor.com/))

### Python dependencies

```bash
pip install fastmcp biopython numpy pandas parasail
```

---

## Installation

### 1. Clone FastaHandler

```bash
git clone https://github.com/OZTaekOppa/FASTAhandler.git
```

### 2. Place the MCP server
The `server.py` must be placed in the **same directory** as FastaHandler's `scripts` folder:
```
FASTAhandler/
├── scripts/
├── fastahandler.py
├── server.py        ← place here
└── ...
```

### 3. Clone this MCP server

```bash
git clone https://github.com/<your-username>/fastahandler-mcp.git
cd fastahandler-mcp
pip install fastmcp
```

---

## Configuration

### Claude Desktop

Edit your `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/your/data"
      ]
    },
    "fastahandler": {
      "command": "python",
      "args": [
        "/path/to/fastahandler-mcp/server.py"
      ],
      "env": {
        "FASTAHANDLER_PATH": "/path/to/FASTAhandler/fastahandler.py"
      }
    }
  }
}
```

> **Tip:** Register both the `filesystem` MCP server and the `fastahandler` MCP server simultaneously so the LLM can analyze your local files and execute modules in the same session.


## Usage

Once configured, simply describe what you want in natural language. The LLM will automatically select the appropriate module and execute it.


```
"Generate assembly statistics for HG002#1#chr1.fa"
→ Executes: all_fa_stats

"Rename FASTA headers using my mapping file rename_map.txt"
→ Executes: prefix_rename

"Extract sequences longer than 500 bp from genome.fa"
→ Executes: subset_fa

"Translate the DNA sequences in coding_seqs.fa to protein"
→ Executes: translate_dna
```


## Notes on Large Files

Processing large genome datasets may exceed the MCP client's default timeout threshold. If this occurs, adjust the client-side timeout settings before running computationally intensive modules (e.g., `asm_stats_unlimit`, `size_pattern_search`).