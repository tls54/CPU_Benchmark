# CPU Benchmarks
This is a collection of benchmark functions to run across my machines.

## Features

- **Interactive Menu System**: Easy-to-use interface for running benchmarks and viewing results
- **Git-Friendly Storage**: Results stored in JSONL format (JSON Lines) for clean git diffs and zero merge conflicts
- **Pretty Stats Table**: View all benchmark results in a formatted table
- **Isolated Execution**: No internet connection required - fully offline capable

## Benchmark Tests

### Prime Number Benchmark

This test counts all prime numbers up to 1,000,000 using a basic trial division algorithm. It is CPU-bound and single-threaded, making it a good indicator of raw integer performance and control flow efficiency in the interpreter.

**What It Measures:**
- Integer math performance
- Branching logic efficiency
- CPU cache/memory access under loop-heavy workloads

### Pi Estimation (Monte Carlo Method)

This benchmark uses the Monte Carlo method to estimate the value of π by randomly generating 10,000,000 points inside a unit square and checking how many fall within the unit circle. It's a good test of floating-point math performance and random number generation speed.

**What It Measures:**
- Floating-point operation throughput
- Random number generator performance
- Tight loop efficiency

### SHA-256 Hashing Benchmark

This test runs 5,000,000 rounds of SHA-256 hashing on a small data block. It's a compute-heavy task that stresses the CPU's arithmetic logic unit (ALU) and evaluates performance in workloads similar to password hashing, cryptography, or blockchain verification.

**What It Measures:**
- Byte-level computation performance
- Repetitive hash function overhead
- Interpreter and C library integration

## Usage

### Running the Benchmark Suite

Simply run the script with Python:

```bash
python Benchmark.py
```

This will launch an interactive menu with the following options:

1. **Run Benchmark** - Execute all three benchmark tests and save results
2. **View Stats** - Display all previous benchmark results in a formatted table
3. **Exit** - Close the application

### Menu Options

#### 1. Run Benchmark
When you select this option, you'll be prompted to enter a system name (e.g., "Ubuntu Desktop", "MacBook Pro", "Dell Laptop"). The script will then:
- Run all three benchmarks sequentially
- Display timing results in real-time
- Save results to `cpu_benchmark_results.jsonl`

#### 2. View Stats
Displays all benchmark runs in a formatted table showing:
- Timestamp of each run
- System name
- Platform (Linux, Darwin, Windows)
- Processor architecture
- Individual benchmark timings

#### 3. Exit
Safely closes the application

## Results Storage

Results are stored in `cpu_benchmark_results.jsonl` using JSON Lines format. Each line is a complete JSON object representing one benchmark run:

```json
{"timestamp": "2025-11-02 16:36:55", "system_name": "Ubuntu", "platform": "Linux", "processor": "x86_64", "primes_time": 2.0039, "pi_time": 1.2477, "hash_time": 1.5036}
```

### Why JSONL?

- **Git-friendly**: Each benchmark run is a single line, creating clean diffs
- **Append-only**: No merge conflicts when multiple machines add results
- **Human-readable**: Easy to inspect and parse
- **Portable**: Works across all platforms and can be committed to git

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)