import asyncio
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

from cargo_mcp.server import (
    CargoError,
    find_cargo_toml,
    run_cargo_command,
    handle_list_tools,
    handle_call_tool,
)


class TestCargoTomlFinding:
    """Test the Cargo.toml finding functionality."""
    
    def test_find_cargo_toml_current_dir(self):
        """Test finding Cargo.toml in current directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cargo_toml = Path(temp_dir) / "Cargo.toml"
            cargo_toml.write_text("[package]\nname = \"test\"\nversion = \"0.1.0\"")
            
            result = find_cargo_toml(temp_dir)
            assert result == cargo_toml.resolve()
    
    def test_find_cargo_toml_parent_dir(self):
        """Test finding Cargo.toml in parent directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cargo_toml = Path(temp_dir) / "Cargo.toml"
            cargo_toml.write_text("[package]\nname = \"test\"\nversion = \"0.1.0\"")
            
            sub_dir = Path(temp_dir) / "src"
            sub_dir.mkdir()
            
            result = find_cargo_toml(str(sub_dir))
            assert result == cargo_toml.resolve()
    
    def test_find_cargo_toml_not_found(self):
        """Test when Cargo.toml is not found."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = find_cargo_toml(temp_dir)
            assert result is None


class TestCargoCommands:
    """Test cargo command execution."""
    
    @pytest.mark.asyncio
    async def test_run_cargo_command_no_cargo(self):
        """Test error when cargo is not available."""
        with patch('shutil.which', return_value=None):
            with pytest.raises(CargoError, match="Cargo is not installed"):
                await run_cargo_command(["--version"])
    
    @pytest.mark.asyncio
    async def test_run_cargo_command_success(self):
        """Test successful cargo command."""
        with patch('shutil.which', return_value='/usr/bin/cargo'):
            mock_process = AsyncMock()
            mock_process.returncode = 0
            mock_process.communicate.return_value = ("cargo 1.70.0", "")
            
            with patch('asyncio.create_subprocess_exec', return_value=mock_process):
                result = await run_cargo_command(["--version"])
                
                assert result['success'] is True
                assert result['exit_code'] == 0
                assert result['stdout'] == "cargo 1.70.0"
                assert result['command'] == "cargo --version"
    
    @pytest.mark.asyncio
    async def test_run_cargo_command_failure(self):
        """Test failed cargo command."""
        with patch('shutil.which', return_value='/usr/bin/cargo'):
            mock_process = AsyncMock()
            mock_process.returncode = 1
            mock_process.communicate.return_value = ("", "error: could not find Cargo.toml")
            
            with patch('asyncio.create_subprocess_exec', return_value=mock_process):
                result = await run_cargo_command(["build"])
                
                assert result['success'] is False
                assert result['exit_code'] == 1
                assert result['stderr'] == "error: could not find Cargo.toml"


class TestToolHandlers:
    """Test MCP tool handlers."""
    
    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test listing available tools."""
        tools = await handle_list_tools()
        
        assert len(tools) == 11  # We have 11 tools defined
        tool_names = [tool.name for tool in tools]
        
        expected_tools = [
            "cargo_build", "cargo_test", "cargo_run", "cargo_check",
            "cargo_clippy", "cargo_fmt", "cargo_doc", "cargo_clean",
            "cargo_tree", "cargo_update", "cargo_bench"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
    
    @pytest.mark.asyncio
    async def test_call_tool_build(self):
        """Test calling cargo_build tool."""
        with patch('cargo_mcp.server.run_cargo_command') as mock_run:
            mock_run.return_value = {
                'command': 'cargo build',
                'exit_code': 0,
                'stdout': 'Finished dev [unoptimized + debuginfo] target(s)',
                'stderr': '',
                'success': True,
                'working_directory': '/test'
            }
            
            result = await handle_call_tool("cargo_build", {})
            
            assert len(result) == 1
            assert "Command: cargo build" in result[0].text
            assert "Success: True" in result[0].text
            mock_run.assert_called_once_with(['build'], None)
    
    @pytest.mark.asyncio
    async def test_call_tool_build_with_options(self):
        """Test calling cargo_build tool with options."""
        with patch('cargo_mcp.server.run_cargo_command') as mock_run:
            mock_run.return_value = {
                'command': 'cargo build --release --features serde',
                'exit_code': 0,
                'stdout': 'Finished release [optimized] target(s)',
                'stderr': '',
                'success': True,
                'working_directory': '/test'
            }
            
            result = await handle_call_tool("cargo_build", {
                "release": True,
                "features": ["serde"]
            })
            
            mock_run.assert_called_once_with(
                ['build', '--release', '--features', 'serde'], 
                None
            )
    
    @pytest.mark.asyncio
    async def test_call_tool_unknown(self):
        """Test calling unknown tool."""
        result = await handle_call_tool("unknown_tool", {})
        
        assert len(result) == 1
        assert "Unknown tool" in result[0].text
    
    @pytest.mark.asyncio
    async def test_call_tool_error_handling(self):
        """Test error handling in tool calls."""
        with patch('cargo_mcp.server.run_cargo_command') as mock_run:
            mock_run.side_effect = CargoError("Test error")
            
            result = await handle_call_tool("cargo_build", {})
            
            assert len(result) == 1
            assert "Error: Test error" in result[0].text


@pytest.mark.asyncio
async def test_integration_with_temp_project():
    """Integration test with a temporary Rust project."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a minimal Cargo.toml
        cargo_toml = Path(temp_dir) / "Cargo.toml"
        cargo_toml.write_text("""
[package]
name = "test-project"
version = "0.1.0"
edition = "2021"

[dependencies]
""")
        
        # Create src directory and main.rs
        src_dir = Path(temp_dir) / "src"
        src_dir.mkdir()
        main_rs = src_dir / "main.rs"
        main_rs.write_text("""
fn main() {
    println!("Hello, world!");
}
""")
        
        # Test finding Cargo.toml
        result = find_cargo_toml(str(src_dir))
        assert result == cargo_toml.resolve()
        
        # Test that the project structure is correct
        assert cargo_toml.exists()
        assert main_rs.exists() 