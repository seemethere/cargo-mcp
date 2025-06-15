# Test Project for Cargo MCP Server

This is a comprehensive test Rust project designed to demonstrate all the functionality of the cargo-mcp server. It includes multiple binaries, tests, benchmarks, and various features to test different Cargo commands.

## Project Structure

- **Main binary** (`src/main.rs`): A CLI application with multiple commands
- **Calculator binary** (`src/bin/calculator.rs`): A simple calculator for testing `cargo run --bin`
- **Library** (`src/lib.rs`): Math functions exposed as a library
- **Tests** (in `src/lib.rs`): Unit tests for the math functions
- **Benchmarks** (`benches/math_bench.rs`): Performance benchmarks using Criterion

## Features

The project includes several Cargo features:
- `json-output` (default): Enables JSON output formatting
- `verbose`: Enables verbose logging

## Usage Examples

### Building the project
```bash
cargo build
cargo build --release
cargo build --features verbose
```

### Running the main binary
```bash
# Basic run
cargo run

# With commands
cargo run -- greet "World"
cargo run -- greet "Rust" --count 3
cargo run -- math add 5.5 3.2
cargo run -- generate --count 5

# With verbose flag
cargo run -- --verbose greet "Test"
```

### Running the calculator binary
```bash
cargo run --bin calculator -- 10 + 5
cargo run --bin calculator -- 15.5 "*" 2.3
cargo run --bin calculator -- 100 / 4
```

### Running tests
```bash
cargo test
cargo test --verbose
cargo test test_add
```

### Running benchmarks
```bash
cargo bench
cargo bench -- bench_add
```

### Other useful commands
```bash
# Check for errors
cargo check

# Run Clippy linter
cargo clippy

# Format code
cargo fmt

# Generate documentation
cargo doc
cargo doc --open

# View dependency tree
cargo tree

# Clean build artifacts
cargo clean
```

## Testing the cargo-mcp server

This project is designed to test all the tools provided by the cargo-mcp server:

1. **cargo_build** - Test building in debug and release modes, with features
2. **cargo_test** - Test running all tests or specific tests
3. **cargo_run** - Test running both binaries with different arguments
4. **cargo_check** - Test checking for compilation errors
5. **cargo_clippy** - Test linting (install clippy first: `rustup component add clippy`)
6. **cargo_fmt** - Test code formatting (install rustfmt first: `rustup component add rustfmt`)
7. **cargo_doc** - Test documentation generation
8. **cargo_clean** - Test cleaning build artifacts
9. **cargo_tree** - Test dependency tree display
10. **cargo_bench** - Test benchmark execution

## Error Testing

The project includes scenarios that can generate errors for testing error handling:

- Division by zero in both the calculator and math operations
- Invalid command line arguments
- Compilation errors (if you modify the code incorrectly)

## Dependencies

- `clap` - Command line argument parsing
- `serde` and `serde_json` - Serialization (demonstrates conditional compilation)
- `criterion` - Benchmarking framework (dev dependency) 