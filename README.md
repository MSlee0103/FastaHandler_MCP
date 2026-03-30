# An MCP Server for FastaHandler

A [Model Context Protocol (MCP)](https://www.anthropic.com/news/model-context-protocol) server that exposes all 26 **FastaHandler** modules as natural language–accessible tools for LLM clients such as Claude Desktop and Cursor.

> **FastaHandler** is a lightweight, Python-based toolkit for FASTA file manipulation in genomic and pangenome research.  
> Main repository: [https://github.com/OZTaekOppa/FASTAhandler](https://github.com/OZTaekOppa/FASTAhandler)

### Requirements

- Python 3.9+
- [FastaHandler](https://github.com/OZTaekOppa/FASTAhandler)
- [FastMCP](https://github.com/jlowin/fastmcp)
- An MCP-compatible client (e.g., [Claude Desktop](https://claude.ai/download), [Cursor](https://www.cursor.com/))

### Additional Dependencies

```bash
pip install fastmcp
```

### Setup

The `server.py` must be placed in the **same directory** as `fastahandler.py` and the `scripts` folder:

```
FastaHandler/
├── scripts/
├── example_data/
├── fastahandler.py
├── server.py        ← place here
└── README.md
```

### Configuration (Claude Desktop)

Edit your `claude_desktop_config.json`:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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
        "/path/to/FastaHandler/server.py"
      ]
    }
  }
}
```

> **Tip:** Register both the `filesystem` and `fastahandler` MCP servers simultaneously so the LLM can access your local files and execute modules in the same session.

### MCP Tool Functions

The MCP server wraps all 26 modules into 6 grouped tool functions:

| MCP Tool Function | FastaHandler Modules |
|---|---|
| `assembly_stats` | `all_fa_stats`, `each_fa_stats`, `asm_stats_unlimit` |
| `concat_and_edit` | `concatenate_fa`, `rename_id`, `prefix_pattern_replace`, `prefix_rename`, `prefix_select_rename` |
| `extract_and_translate` | `chr_pansn_extract`, `extract_pattern`, `id_extract_multi_location`, `translate_dna` |
| `remove_and_subset` | `subset_fa`, `remove_duplicate`, `find_anchor_trim`, `overlap_split` |
| `filter_and_sort` | `find_count_duplicate`, `id_extract`, `id_extract_location`, `size_pattern_search`, `find_merge_fa` |
| `reformat` | `multi2single`, `gfa2fa`, `reverse_complement`, `pangenome_id_rename`, `multi2each` |

Each tool accepts a `mode` parameter (module name), input/output paths, and optional `key=value` arguments that are resolved into CLI commands and executed via subprocess.

### Usage Examples

Once configured, simply describe what you want in natural language:

```
"Generate assembly statistics for /path/to/asm.fa/"
→ Executes: all_fa_stats

"Rename the FASTA headers of /path/to/file.fa/ using my mapping file /path/to/rename_map.txt/"
→ Executes: prefix_rename

"Filter sequences shorter than 100 bp from /path/to/geneme.fa/, then calculate assembly statistics"
→ subset_fa → all_fa_stats (automated two-step pipeline)
```

### Notes on Large Files

Processing large genome datasets may exceed the MCP client's default timeout threshold. Adjust the client-side timeout settings when handling large-scale inputs (e.g., `asm_stats_unlimit`, `size_pattern_search`).
