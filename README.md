# CPU Benchmark Suite

A lightweight Python-based CPU benchmarking tool that measures computational performance across different systems using a text-based user interface.

## Overview

This tool runs a suite of four benchmark tests to evaluate CPU and memory performance, collecting statistical data across multiple runs to ensure reliability. Results are stored in JSONL format for easy tracking and comparison between systems.

## Running the Application

```bash
python Benchmark.py
```

The TUI presents a menu with four options:
1. **Run Benchmark** - Execute all benchmark tests and save results
2. **View Stats** - Display historical benchmark results in tabular format
3. **Delete Results by System Name** - Remove specific benchmark entries
4. **Exit** - Close the application

## Benchmark Tests

### 1. Prime Number Calculation
Tests integer arithmetic and loop efficiency by finding all prime numbers up to 1,000,000 using trial division. This benchmark measures raw CPU computational throughput for integer operations.

**Theory**: Prime number calculation is CPU-bound and benefits from high clock speeds and efficient branch prediction. Expected result: 78,498 primes.

### 2. Pi Estimation (Monte Carlo Method)
Estimates π using 10,000,000 random points and the Monte Carlo method (checking if points fall within a unit circle). Tests floating-point performance and random number generation.

**Theory**: This benchmark stresses floating-point units (FPU) and measures how efficiently the CPU handles probabilistic computations. Expected result: π ≈ 3.14159.

### 3. SHA-256 Hashing
Performs 5,000,000 rounds of recursive SHA-256 hashing. Tests cryptographic performance and the CPU's ability to handle bitwise operations.

**Theory**: Hashing is CPU-intensive and benefits from specialized CPU instructions (like SHA extensions on modern processors). This benchmark measures sustained computational load.

### 4. Memory Bandwidth
Creates a list of 5,000,000 integers (~40MB) and performs 10 iterations of sequential reads (sum) and writes (reverse). Tests memory subsystem performance.

**Theory**: Unlike the other tests, this measures memory bandwidth and cache efficiency rather than pure CPU speed. Performance depends on RAM speed, cache size, and memory controller efficiency.

## Features

- **Statistical Analysis**: Each test runs 3 times, reporting median, min, max, and standard deviation
- **System Load Detection**: Warns if high system load may affect results (Unix-like systems)
- **Cross-Platform**: Supports Windows, macOS, and Linux
- **CPU Frequency Detection**: Automatically detects and logs CPU clock speed
- **Historical Tracking**: Compare results across runs and systems
- **Validation**: Verifies benchmark output correctness to detect computational errors

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Results Storage

Benchmark results are saved to `cpu_benchmark_results.jsonl` with metadata including:
- Timestamp
- System name
- Platform and processor information
- Python version
- CPU core count and frequency
- Statistical measurements for each test
