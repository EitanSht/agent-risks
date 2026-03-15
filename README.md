<div align="center">

# 📰 research-helper

**A fast, lightweight MCP server that fetches web articles and returns clean,
readable text — ready for summarization, analysis, or research workflows.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)

</div>

---

## Why research-helper?

AI agents are great at analysis, but fetching and cleaning web content is
messy — scripts, ads, navigation chrome, cookie banners. **research-helper**
handles all of that so your agent gets clean text every time.

- 🚀 **Zero dependencies** — Python standard library only, nothing to install
- 🧹 **Smart HTML cleaning** — strips scripts, styles, nav, ads automatically
- ⚡ **Fast** — lightweight stdio transport, no HTTP overhead
- 🔌 **Universal** — works with VS Code Copilot, Claude Desktop, Cursor, or
  any MCP-compatible client

## Quick Start

### Installation

```bash
pip install git+https://github.com/EitanSht/research-helper.git
```

### VS Code Copilot

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "research-helper": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "research_helper"]
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "research-helper": {
      "command": "python",
      "args": ["-m", "research_helper"]
    }
  }
}
```

### Cursor

Add to your MCP config:

```json
{
  "research-helper": {
    "command": "python",
    "args": ["-m", "research_helper"]
  }
}
```

Then ask your agent: *"Use research-helper to fetch and summarize this article:
https://example.com/interesting-article"*

## Tool Reference

### `fetch_article`

Fetches a web page and returns its text content with all HTML markup removed.

| Parameter | Type     | Required | Description                     |
|-----------|----------|----------|---------------------------------|
| `url`     | `string` | Yes      | The URL of the article to fetch |

**Returns:** Clean text content of the page, with scripts, styles, and
non-content elements stripped.

**Example response:**
```
Large language model
A large language model (LLM) is a type of computational model designed for
natural language processing tasks such as language generation...
```

## Installation

```bash
pip install git+https://github.com/EitanSht/research-helper.git
```

No extra dependencies — uses Python standard library only.

## How It Works

research-helper implements the [Model Context Protocol](https://modelcontextprotocol.io/)
over stdio. When your AI agent calls `fetch_article`:

1. Fetches the URL with a standard HTTP request
2. Parses the HTML and strips non-content elements (scripts, styles, nav)
3. Extracts clean, readable text
4. Returns the text to the agent via MCP

The server runs as a local subprocess managed by your MCP client — no separate
process to manage, no ports to configure, no API keys needed.

## Requirements

- Python 3.10+
- That's it

## Contributing

PRs welcome! Please keep the zero-dependency philosophy — stdlib only.

## License

MIT

