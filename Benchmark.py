from time import perf_counter
import hashlib
import random
import platform
import json
from datetime import datetime
from pathlib import Path

RESULTS_FILE = "cpu_benchmark_results.jsonl"

def benchmark_primes(limit):
    for num in range(2, 500):  # warmup
        _ = all(num % i != 0 for i in range(2, int(num ** 0.5) + 1))
    start = perf_counter()
    primes = []
    for num in range(2, limit):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    duration = perf_counter() - start
    return duration, len(primes)

def benchmark_pi_estimation(iterations):
    for _ in range(1000):  # warmup
        x, y = random.random(), random.random()
        _ = x*x + y*y <= 1
    start = perf_counter()
    inside_circle = 0
    for _ in range(iterations):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            inside_circle += 1
    pi_estimate = (4.0 * inside_circle) / iterations
    duration = perf_counter() - start
    return duration, pi_estimate

def benchmark_hashing(rounds):
    data = "benchmarking_is_fun!".encode()
    for _ in range(10000):  # warmup
        data = hashlib.sha256(data).digest()

    start = perf_counter()
    for _ in range(rounds):
        data = hashlib.sha256(data).digest()
    duration = perf_counter() - start
    return duration, data.hex()[:10]

def log_results(system_name, primes_time, pi_time, hash_time):
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_name": system_name,
        "platform": platform.system(),
        "processor": platform.machine(),
        "primes_time": round(primes_time, 4),
        "pi_time": round(pi_time, 4),
        "hash_time": round(hash_time, 4)
    }

    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(result) + "\n")

def load_results():
    """Load all benchmark results from the JSONL file."""
    results = []
    if Path(RESULTS_FILE).exists():
        with open(RESULTS_FILE, "r") as f:
            for line in f:
                if line.strip():
                    results.append(json.loads(line))
    return results

def display_stats():
    """Display benchmark results in a formatted table."""
    results = load_results()

    if not results:
        print("\nNo benchmark results found. Run a benchmark first!\n")
        return

    print("\n" + "=" * 120)
    print("CPU BENCHMARK RESULTS")
    print("=" * 120)

    # Header
    header = f"{'Timestamp':<20} {'System':<20} {'Platform':<10} {'Processor':<15} {'Primes (s)':<12} {'Pi (s)':<12} {'Hash (s)':<12}"
    print(header)
    print("-" * 120)

    # Data rows
    for result in results:
        row = f"{result['timestamp']:<20} {result['system_name']:<20} {result['platform']:<10} {result['processor']:<15} {result['primes_time']:<12.4f} {result['pi_time']:<12.4f} {result['hash_time']:<12.4f}"
        print(row)

    print("=" * 120)
    print(f"Total benchmark runs: {len(results)}\n")

def run_benchmark():
    """Run the benchmark suite."""
    system_name = input("Enter system name: ").strip()

    if not system_name:
        print("System name cannot be empty!")
        return

    print(f"\nRunning CPU Benchmark on: {system_name}")
    print("=" * 40)

    primes_time, prime_count = benchmark_primes(1_000_000)
    print(f"Primes up to 1,000,000: {prime_count} primes in {primes_time:.4f} seconds")

    pi_time, pi_val = benchmark_pi_estimation(10_000_000)
    print(f"Pi estimation: {pi_val:.5f} in {pi_time:.4f} seconds")

    hash_time, hash_sample = benchmark_hashing(5_000_000)
    print(f"Hashing: 5M rounds in {hash_time:.4f} seconds (sample: {hash_sample})")

    log_results(system_name, primes_time, pi_time, hash_time)
    print(f"\nResults saved to {RESULTS_FILE}\n")

def show_menu():
    """Display the main menu and handle user input."""
    while True:
        print("\n" + "=" * 40)
        print("CPU BENCHMARK SUITE")
        print("=" * 40)
        print("1. Run Benchmark")
        print("2. View Stats")
        print("3. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            run_benchmark()
        elif choice == "2":
            display_stats()
        elif choice == "3":
            print("\nGoodbye!\n")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.\n")

def main():
    show_menu()

if __name__ == "__main__":
    main()
