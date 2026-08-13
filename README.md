# MCP File Server

An MCP (Model Context Protocol) server exposing sandboxed file system operations to LLM clients.

> **Status:** working prototype, pre-1.0 in practice. Pinned to the `mcp` 1.x SDK.
> A migration to the `mcp` 2.x `MCPServer` API is planned — see [Roadmap](#roadmap).

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) for dependency and environment management

## Quick start

```bash
git clone https://github.com/ahmedel-tawil/mcp-file-server.git
cd mcp-file-server
uv sync
```

`uv sync` creates `.venv/`, resolves from `uv.lock`, and installs the project in editable mode.
There is no `requirements.txt` and no manual `venv` step — `uv.lock` is the source of truth.

Run the server:

```bash
uv run mcp-file-server
```

It speaks MCP over stdio, so it will sit and wait for a client — that is expected.

## Configuration

All configuration is read from the environment at startup:

| Variable | Default | Meaning |
| --- | --- | --- |
| `MCP_BASE_DIR` | `~/Documents` | Sandbox root. Every path is resolved and must stay inside it. |
| `MCP_LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Logs go to stderr. |
| `MCP_MAX_FILE_SIZE` | `10485760` | Max file size in bytes. **Not yet enforced** — see Roadmap. |

## Tools

| Tool | Description |
| --- | --- |
| `read_file` | Read a text or PDF file |
| `write_file` | Write content, creating or overwriting |
| `create_file` | Create a new file, failing if it exists |
| `list_files` | List a directory's contents |
| `search_files` | Recursive glob search by name pattern |

Text formats are matched by extension (`.txt`, `.md`, `.py`, `.json`, `.yaml`, and ~30 more);
PDFs are read via `pypdf`.

## Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "file-system": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/mcp-file-server", "run", "mcp-file-server"],
      "env": {
        "MCP_BASE_DIR": "/Users/you/Documents"
      }
    }
  }
}
```

Replace both paths with your own, then fully quit and reopen Claude Desktop.

## Development

```bash
uv sync              # install project + dev group
uv run ruff check .  # lint
uv run ruff format . # format
uv run mypy src      # type check
uv run pytest        # tests (none yet — see Roadmap)
```

Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>`); this updates
`pyproject.toml` and `uv.lock` together. Never edit `uv.lock` by hand.

## Architecture

```
src/mcp_file_server/
├── server.py         # MCP protocol wiring + entry point
├── config.py         # Environment-driven configuration
├── tools/            # One class per tool, all extending BaseTool
├── handlers/         # Per-format I/O (text, PDF)
├── utils/            # Path validation, logging, response formatting
└── exceptions/       # Typed exception hierarchy
```

`BaseTool.execute()` is a template method: it logs the call, delegates to the subclass's
`_execute_impl()`, and converts any exception into a formatted error response. Adding a tool
means subclassing `BaseTool`, implementing `get_definition()` and `_execute_impl()`, and
registering it in `MCPFileServer._initialize_tools()`.

Security is enforced by `PathValidator`, which resolves every path and rejects anything that
escapes `MCP_BASE_DIR`.

## Roadmap

- [x] Core file operations (read, write, create, list, search)
- [x] PDF support
- [x] `uv` packaging, installable console script
- [ ] Migrate to the `mcp` 2.x `MCPServer` API
- [ ] Test suite
- [ ] Enforce `MCP_MAX_FILE_SIZE`
- [ ] Harden `PathValidator` against symlink escapes
- [ ] Run blocking file I/O off the event loop
- [ ] Publish to PyPI

## License

MIT
