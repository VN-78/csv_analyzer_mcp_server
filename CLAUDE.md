# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CSV analyzer MCP (Model Context Protocol) server built using FastMCP. The project implements an MCP server that can be consumed by MCP clients to provide tools, resources, and prompts for working with CSV data analysis.

## Architecture

The project follows a modular structure:

- `main/mcp_server.py`: Contains the MCP server implementation using FastMCP framework. This is where tools (functions), resources (data endpoints), and prompts are registered.
- `main/mcp_client.py`: Client implementation for connecting to and testing the MCP server.
- `main.py`: Entry point placeholder (currently minimal).

The server uses FastMCP's decorator-based API:
- `@mcp.tool()` - Registers callable functions as MCP tools
- `@mcp.resource()` - Registers dynamic resources with URI patterns
- `@mcp.prompt()` - Registers prompt templates

The current implementation (main/mcp_server.py:13-17) runs on localhost:8050 using streamable-http transport.

## Development Commands

### Environment Setup
```bash
# Python 3.14 is required (specified in .python-version and pyproject.toml:6)
# Use uv for dependency management
uv sync
```

### Running the MCP Server
```bash
# Run the server with streamable-http transport
uv run python main/mcp_server.py

# Alternative: Run via MCP CLI (as shown in main/mcp_server.py:8-9)
cd main
uv run server fastmcp_quickstart stdio
```

### Testing with MCP Inspector
The project is configured with VS Code MCP settings in `.vscode/mcp.json` for testing with the MCP inspector tool.

## Key Dependencies

- `fastmcp>=2.13.0.2` - FastMCP framework for building MCP servers
- `mcp[cli]>=1.21.0` - MCP protocol implementation with CLI tools
- `pandas>=2.3.3` - CSV/data analysis (core functionality)
- `fastapi>=0.121.1` - Web framework (used by FastMCP)
- `nest-asyncio>=1.6.0` - Async event loop support

## Transport Modes

The MCP server supports multiple transport modes (configured in main/mcp_server.py:48):
- `streamable-http` - Current default, requires host/port configuration
- `stdio` - Standard input/output for CLI integration
- `sse` - Server-Sent Events

When changing transport modes, ensure the FastMCP initialization (main/mcp_server.py:13-17) includes appropriate host/port settings for HTTP-based transports.
