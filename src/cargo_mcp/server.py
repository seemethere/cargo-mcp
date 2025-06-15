#!/usr/bin/env python3
"""
Cargo MCP Server

A Model Context Protocol server that provides tools for running Cargo commands.
This allows AI agents to interact with Rust projects through Cargo.
"""

import asyncio
import json
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.server.lowlevel import NotificationOptions
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cargo-mcp")

# Initialize the MCP server
server = Server("cargo-mcp")


class CargoError(Exception):
    """Custom exception for Cargo-related errors."""
    pass


def find_cargo_toml(start_path: str = ".") -> Optional[Path]:
    """Find the nearest Cargo.toml file by walking up the directory tree."""
    current_path = Path(start_path).resolve()
    
    while current_path != current_path.parent:
        cargo_toml = current_path / "Cargo.toml"
        if cargo_toml.exists():
            return cargo_toml
        current_path = current_path.parent
    
    return None


async def run_cargo_command(
    args: List[str], 
    cwd: Optional[str] = None,
    capture_output: bool = True
) -> Dict[str, Any]:
    """Run a cargo command and return the result."""
    # Check if cargo is available
    if not shutil.which("cargo"):
        raise CargoError("Cargo is not installed or not in PATH")
    
    # Find working directory with Cargo.toml if not specified
    if cwd is None:
        cargo_toml = find_cargo_toml()
        if cargo_toml:
            cwd = str(cargo_toml.parent)
        else:
            cwd = "."
    
    # Construct the full command
    cmd = ["cargo"] + args
    
    try:
        if capture_output:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            # Decode bytes to string
            stdout_str = stdout.decode('utf-8', errors='replace').strip() if stdout else ""
            stderr_str = stderr.decode('utf-8', errors='replace').strip() if stderr else ""
            
            return {
                "command": " ".join(cmd),
                "exit_code": process.returncode,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "success": process.returncode == 0,
                "working_directory": cwd
            }
        else:
            # For interactive commands, just return the exit code
            process = await asyncio.create_subprocess_exec(*cmd, cwd=cwd)
            exit_code = await process.wait()
            
            return {
                "command": " ".join(cmd),
                "exit_code": exit_code,
                "success": exit_code == 0,
                "working_directory": cwd
            }
    
    except Exception as e:
        raise CargoError(f"Failed to run cargo command: {e}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available Cargo tools."""
    return [
        Tool(
            name="cargo_build",
            description="Build a Rust project with Cargo. Compiles the project and its dependencies.",
            inputSchema={
                "type": "object",
                "properties": {
                    "release": {
                        "type": "boolean",
                        "description": "Build in release mode with optimizations",
                        "default": False
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of features to activate"
                    },
                    "target": {
                        "type": "string",
                        "description": "Build for the given target triple"
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        ),
        Tool(
            name="cargo_test",
            description="Run tests for a Rust project with Cargo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "test_name": {
                        "type": "string",
                        "description": "Name of specific test to run (optional)"
                    },
                    "release": {
                        "type": "boolean",
                        "description": "Run tests in release mode",
                        "default": False
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of features to activate"
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        ),
        Tool(
            name="cargo_run",
            description="Run a Rust binary with Cargo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "bin_name": {
                        "type": "string",
                        "description": "Name of the binary to run (optional for single-binary projects)"
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Arguments to pass to the binary"
                    },
                    "release": {
                        "type": "boolean",
                        "description": "Run in release mode",
                        "default": False
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of features to activate"
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        ),
        Tool(
            name="cargo_check",
            description="Check a Rust project for errors without building it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of features to activate"
                    }
                }
            }
        ),
        Tool(
            name="cargo_clippy",
            description="Run Clippy linter on a Rust project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "fix": {
                        "type": "boolean",
                        "description": "Automatically apply suggested fixes",
                        "default": False
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of features to activate"
                    }
                }
            }
        ),
        Tool(
            name="cargo_fmt",
            description="Format Rust code using rustfmt.",
            inputSchema={
                "type": "object",
                "properties": {
                    "check": {
                        "type": "boolean",
                        "description": "Check if files are formatted without modifying them",
                        "default": False
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        ),
        Tool(
            name="cargo_doc",
            description="Generate documentation for a Rust project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "open": {
                        "type": "boolean",
                        "description": "Open documentation in browser after generation",
                        "default": False
                    },
                    "no_deps": {
                        "type": "boolean",
                        "description": "Don't build documentation for dependencies",
                        "default": False
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        ),
        Tool(
            name="cargo_clean",
            description="Clean build artifacts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        ),
        Tool(
            name="cargo_tree",
            description="Display dependency tree.",
            inputSchema={
                "type": "object",
                "properties": {
                    "package": {
                        "type": "string",
                        "description": "Package to display tree for (optional)"
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of features to activate"
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        ),
        Tool(
            name="cargo_update",
            description="Update dependencies in Cargo.lock.",
            inputSchema={
                "type": "object",
                "properties": {
                    "package": {
                        "type": "string",
                        "description": "Specific package to update (optional)"
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        ),
        Tool(
            name="cargo_bench",
            description="Run benchmarks.",
            inputSchema={
                "type": "object",
                "properties": {
                    "bench_name": {
                        "type": "string",
                        "description": "Name of specific benchmark to run (optional)"
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of features to activate"
                    },
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace root (optional, will auto-detect)"
                    }
                }
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for Cargo commands."""
    
    try:
        workspace_path = arguments.get("workspace_path")
        
        if name == "cargo_build":
            args = ["build"]
            if arguments.get("release"):
                args.append("--release")
            if arguments.get("features"):
                args.extend(["--features", ",".join(arguments["features"])])
            if arguments.get("target"):
                args.extend(["--target", arguments["target"]])
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_test":
            args = ["test"]
            if arguments.get("test_name"):
                args.append(arguments["test_name"])
            if arguments.get("release"):
                args.append("--release")
            if arguments.get("features"):
                args.extend(["--features", ",".join(arguments["features"])])
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_run":
            args = ["run"]
            if arguments.get("bin_name"):
                args.extend(["--bin", arguments["bin_name"]])
            if arguments.get("release"):
                args.append("--release")
            if arguments.get("features"):
                args.extend(["--features", ",".join(arguments["features"])])
            if arguments.get("args"):
                args.append("--")
                args.extend(arguments["args"])
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_check":
            args = ["check"]
            if arguments.get("features"):
                args.extend(["--features", ",".join(arguments["features"])])
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_clippy":
            args = ["clippy"]
            if arguments.get("fix"):
                args.append("--fix")
            if arguments.get("features"):
                args.extend(["--features", ",".join(arguments["features"])])
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_fmt":
            args = ["fmt"]
            if arguments.get("check"):
                args.append("--check")
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_doc":
            args = ["doc"]
            if arguments.get("open"):
                args.append("--open")
            if arguments.get("no_deps"):
                args.append("--no-deps")
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_clean":
            args = ["clean"]
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_tree":
            args = ["tree"]
            if arguments.get("package"):
                args.extend(["--package", arguments["package"]])
            if arguments.get("features"):
                args.extend(["--features", ",".join(arguments["features"])])
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_update":
            args = ["update"]
            if arguments.get("package"):
                args.extend(["--package", arguments["package"]])
            
            result = await run_cargo_command(args, workspace_path)
            
        elif name == "cargo_bench":
            args = ["bench"]
            if arguments.get("bench_name"):
                args.append(arguments["bench_name"])
            if arguments.get("features"):
                args.extend(["--features", ",".join(arguments["features"])])
            
            result = await run_cargo_command(args, workspace_path)
            
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        # Format the output
        output_lines = [f"Command: {result['command']}"]
        output_lines.append(f"Working Directory: {result['working_directory']}")
        output_lines.append(f"Exit Code: {result['exit_code']}")
        output_lines.append(f"Success: {result['success']}")
        
        if result.get('stdout'):
            output_lines.append("\n--- STDOUT ---")
            output_lines.append(result['stdout'])
        
        if result.get('stderr'):
            output_lines.append("\n--- STDERR ---")
            output_lines.append(result['stderr'])
        
        return [TextContent(type="text", text="\n".join(output_lines))]
        
    except CargoError as e:
        logger.error(f"Cargo error in {name}: {e}")
        return [TextContent(type="text", text=f"Error: {e}")]
    except Exception as e:
        logger.error(f"Unexpected error in {name}: {e}")
        return [TextContent(type="text", text=f"Unexpected error: {e}")]


async def main():
    """Main entry point for the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cargo-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


def cli_main():
    """CLI entry point that properly runs the async main function."""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main() 