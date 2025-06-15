use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use test_project::math;

#[derive(Parser)]
#[command(name = "test-project")]
#[command(about = "A test Rust project for demonstrating cargo-mcp functionality")]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,
    
    #[arg(short, long)]
    verbose: bool,
}

#[derive(Subcommand)]
enum Commands {
    /// Say hello to someone
    Greet { 
        /// Name of the person to greet
        name: String,
        /// Number of times to greet
        #[arg(short, long, default_value_t = 1)]
        count: u8,
    },
    /// Perform math operations
    Math {
        #[command(subcommand)]
        operation: MathOps,
    },
    /// Generate test data
    Generate {
        /// Number of items to generate
        #[arg(short, long, default_value_t = 10)]
        count: usize,
    },
}

#[derive(Subcommand, Debug)]
enum MathOps {
    Add { a: f64, b: f64 },
    Subtract { a: f64, b: f64 },
    Multiply { a: f64, b: f64 },
    Divide { a: f64, b: f64 },
}

#[derive(Serialize, Deserialize, Debug)]
struct TestData {
    id: u32,
    name: String,
    value: f64,
}

fn main() {
    let cli = Cli::parse();
    
    if cli.verbose {
        println!("Running in verbose mode");
    }
    
    match &cli.command {
        Some(Commands::Greet { name, count }) => {
            for i in 1..=*count {
                if *count > 1 {
                    println!("{}. Hello, {}!", i, name);
                } else {
                    println!("Hello, {}!", name);
                }
            }
        }
        Some(Commands::Math { operation }) => {
            let result = match operation {
                MathOps::Add { a, b } => {
                    let result = math::add(*a, *b);
                    println!("{} + {} = {}", a, b, result);
                    result
                }
                MathOps::Subtract { a, b } => {
                    let result = math::subtract(*a, *b);
                    println!("{} - {} = {}", a, b, result);
                    result
                }
                MathOps::Multiply { a, b } => {
                    let result = math::multiply(*a, *b);
                    println!("{} * {} = {}", a, b, result);
                    result
                }
                MathOps::Divide { a, b } => {
                    if *b == 0.0 {
                        eprintln!("Error: Division by zero!");
                        std::process::exit(1);
                    }
                    let result = math::divide(*a, *b);
                    println!("{} / {} = {}", a, b, result);
                    result
                }
            };
            
            #[cfg(feature = "json-output")]
            {
                let json_result = serde_json::json!({
                    "result": result,
                    "operation": format!("{:?}", operation)
                });
                println!("JSON: {}", json_result);
            }
        }
        Some(Commands::Generate { count }) => {
            let data: Vec<TestData> = (1..=*count)
                .map(|i| TestData {
                    id: i as u32,
                    name: format!("Item {}", i),
                    value: (i as f64) * 1.5,
                })
                .collect();
                
            println!("Generated {} test items:", data.len());
            for item in &data {
                println!("  {:?}", item);
            }
            
            #[cfg(feature = "json-output")]
            if let Ok(json) = serde_json::to_string_pretty(&data) {
                println!("\nJSON output:\n{}", json);
            }
        }
        None => {
            println!("Test project is running successfully!");
            println!("Use --help for available commands.");
        }
    }
}


