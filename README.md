# CPU Benchmarks
This is a collection of benchmark functions to run across my machines.  

## Prime Number Benchmark


This test counts all prime numbers up to 1,000,000 using a basic trial division algorithm. It is CPU-bound and single-threaded, making it a good indicator of raw integer performance and control flow efficiency in the interpreter.

### What It Measures:

- Integer math performance

- Branching logic efficiency

- CPU cache/memory access under loop-heavy workloads

## Pi Estimation (Monte Carlo Method)

This benchmark uses the Monte Carlo method to estimate the value of π by randomly generating 1,000,000 points inside a unit square and checking how many fall within the unit circle. It’s a good test of floating-point math performance and random number generation speed.

### What It Measures:

- Floating-point operation throughput

- Random number generator performance

- Tight loop efficiency

## SHA-256 Hashing Benchmark

This test runs 5,000,000 rounds of SHA-256 hashing on a small data block. It's a compute-heavy task that stresses the CPU's arithmetic logic unit (ALU) and evaluates performance in workloads similar to password hashing, cryptography, or blockchain verification.

### What It Measures:

- Byte-level computation performance

- Repetitive hash function overhead

- Interpreter and C library integration

## Run instructions
Full Run command: C:\msys64\mingw64\bin\python.exe Benchmark.py --system-name "Name of Machine"

Compressed Run command: python Benchmark.py --system-name "Name of Machine"