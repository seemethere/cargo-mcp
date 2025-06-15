# Cargo MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that provides tools for running Cargo commands. This server allows AI agents to interact with Rust projects through Cargo, enabling automated builds, tests, documentation generation, and more.

## Features

The server provides the following Cargo tools:

- **`cargo_build`** - Build a Rust project with Cargo
- **`cargo_test`** - Run tests for a Rust project
- **`cargo_run`** - Run a Rust binary
- **`cargo_check`** - Check a project for errors without building
- **`cargo_clippy`** - Run Clippy linter
- **`cargo_fmt`** - Format Rust code using rustfmt
- **`cargo_doc`** - Generate documentation
- **`cargo_clean`** - Clean build artifacts
- **`cargo_tree`** - Display dependency tree
- **`cargo_update`** - Update dependencies in Cargo.lock
- **`cargo_bench`** - Run benchmarks

## Installation

### Prerequisites

- Python 3.8 or higher
- Rust and Cargo installed on your system
- Access to install Python packages

### Install from source

1. Clone this repository:
```bash
git clone <repository-url>
cd cargo-mcp
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### With Claude Desktop

Add the server to your `claude_desktop_config.json`:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "cargo-mcp": {
      "command": "cargo-mcp"
    }
  }
}
```

### With other MCP clients

The server can be used with any MCP-compatible client. Start the server using:

```bash
cargo-mcp
```

### Testing with MCP Inspector

You can test the server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector cargo-mcp
```

## Tool Documentation

### cargo_build

Build a Rust project with Cargo.

**Parameters:**
- `release` (boolean, optional): Build in release mode with optimizations
- `features` (array, optional): List of features to activate
- `target` (string, optional): Build for the given target triple
- `workspace_path` (string, optional): Path to the workspace root (auto-detected if not provided)

### cargo_test

Run tests for a Rust project.

**Parameters:**
- `test_name` (string, optional): Name of specific test to run
- `release` (boolean, optional): Run tests in release mode
- `features` (array, optional): List of features to activate
- `workspace_path` (string, optional): Path to the workspace root

### cargo_run

Run a Rust binary.

**Parameters:**
- `bin_name` (string, optional): Name of the binary to run (for multi-binary projects)
- `args` (array, optional): Arguments to pass to the binary
- `release` (boolean, optional): Run in release mode
- `features` (array, optional): List of features to activate
- `workspace_path` (string, optional): Path to the workspace root

### cargo_check

Check a Rust project for errors without building it.

**Parameters:**
- `features` (array, optional): List of features to activate
- `workspace_path` (string, optional): Path to the workspace root

### cargo_clippy

Run Clippy linter on a Rust project.

**Parameters:**
- `fix` (boolean, optional): Automatically apply suggested fixes
- `features` (array, optional): List of features to activate
- `workspace_path` (string, optional): Path to the workspace root

### cargo_fmt

Format Rust code using rustfmt.

**Parameters:**
- `check` (boolean, optional): Check if files are formatted without modifying them
- `workspace_path` (string, optional): Path to the workspace root

### cargo_doc

Generate documentation for a Rust project.

**Parameters:**
- `open` (boolean, optional): Open documentation in browser after generation
- `no_deps` (boolean, optional): Don't build documentation for dependencies
- `workspace_path` (string, optional): Path to the workspace root

### cargo_clean

Clean build artifacts.

**Parameters:**
- `workspace_path` (string, optional): Path to the workspace root

### cargo_tree

Display dependency tree.

**Parameters:**
- `package` (string, optional): Package to display tree for
- `features` (array, optional): List of features to activate
- `workspace_path` (string, optional): Path to the workspace root

### cargo_update

Update dependencies in Cargo.lock.

**Parameters:**
- `package` (string, optional): Specific package to update
- `workspace_path` (string, optional): Path to the workspace root

### cargo_bench

Run benchmarks.

**Parameters:**
- `bench_name` (string, optional): Name of specific benchmark to run
- `features` (array, optional): List of features to activate
- `workspace_path` (string, optional): Path to the workspace root

## Project Structure Detection

The server automatically detects Rust projects by searching for `Cargo.toml` files. It walks up the directory tree from the current working directory to find the nearest `Cargo.toml` file and uses that directory as the workspace root.

You can override this behavior by providing the `workspace_path` parameter to any tool.

## Error Handling

The server provides detailed error messages and logs for troubleshooting:

- Checks if Cargo is installed and available in PATH
- Validates that Cargo.toml exists in the target directory
- Captures both stdout and stderr from Cargo commands
- Provides detailed command execution information

## Development

### Setup

1. Clone the repository
2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Testing

Run tests using pytest:
```bash
pytest
```

### Code Formatting

Format code using black:
```bash
black src/
```

Lint code using ruff:
```bash
ruff check src/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the [MCP documentation](https://modelcontextprotocol.io) for general MCP questions 