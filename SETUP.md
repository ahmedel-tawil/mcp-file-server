# Setup & Troubleshooting

Complements the quick start in [README.md](README.md). This file covers verifying an
install and diagnosing a server that will not connect.

## Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

uv manages the Python interpreter too — `.python-version` pins 3.12, and `uv sync` will
download that interpreter automatically if it is missing. No system Python setup required.

## Verify the install

```bash
uv sync
uv run python -c "import mcp_file_server; print(mcp_file_server.__version__)"
```

Then confirm the server answers a real MCP handshake:

```bash
MCP_BASE_DIR=/tmp uv run mcp-file-server
```

The process should start, log `Server ready and listening` to stderr, and then block waiting
for a client on stdin. That is correct behaviour — press Ctrl+C to stop. If it exits
immediately, the traceback on stderr is the real error.

## Connecting a client

The server communicates over **stdio**, so the client launches the process; you do not run it
yourself in normal use. See the Claude Desktop config in [README.md](README.md).

Point `MCP_BASE_DIR` at the narrowest directory that covers your use case. It is the only
thing standing between a client and the rest of your disk.

## Troubleshooting

**Tools do not appear in the client**

Check the client's own logs first — the server's stderr is captured there:

```bash
tail -f ~/Library/Logs/Claude/mcp-server-file-system.log
```

**`spawn uv ENOENT`**

The client cannot find `uv` on its `PATH`. GUI apps do not inherit your shell `PATH`. Use the
absolute path from `which uv` as the `command` value.

**`Base directory does not exist`**

`MCP_BASE_DIR` points at a missing path. The server validates this at startup and refuses to
run rather than silently falling back.

**`ModuleNotFoundError: No module named 'mcp_file_server'`**

The environment is stale. Rebuild it:

```bash
rm -rf .venv && uv sync
```

**Dependency resolution differs from a teammate's**

`uv.lock` is committed and is the source of truth. Use `uv sync` (which respects the lock),
not `uv pip install`. To intentionally update pins, run `uv lock --upgrade` and commit the
result.

## Manual smoke test

With a client attached, exercise each tool:

1. "List the files in my base directory" → `list_files`
2. "Create a file called `test.txt` containing hello" → `create_file`
3. "Read `test.txt`" → `read_file`
4. "Find all PDF files" → `search_files`
5. "Overwrite `test.txt` with new content" → `write_file`

Then confirm the sandbox holds: ask it to read `../../../../etc/passwd`. It must fail with a
`SecurityError`, not return content.
