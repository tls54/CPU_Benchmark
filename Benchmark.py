from time import perf_counter
import hashlib
import random
import platform
import argparse
import csv
from datetime import datetime
from pathlib import Path

CSV_FILE = "cpu_benchmark_results.csv"

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
    fields = [
        "timestamp", "system_name", "platform", "processor",
        "primes_time", "pi_time", "hash_time"
    ]
    data = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        system_name,
        platform.system(),
        platform.processor(),
        f"{primes_time:.4f}",
        f"{pi_time:.4f}",
        f"{hash_time:.4f}"
    ]
    file_exists = Path(CSV_FILE).exists()

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        writer.writerow(data)

def main():
    parser = argparse.ArgumentParser(description="CPU Benchmarking Script")
    parser.add_argument("--system-name", type=str, required=True, help="Custom name for this system")
    args = parser.parse_args()

    print(f"Running CPU Benchmark on: {args.system_name}")
    print("=" * 40)

    primes_time, prime_count = benchmark_primes(1_000_000)
    print(f"Primes up to 1,000,000: {prime_count} primes in {primes_time:.4f} seconds")

    pi_time, pi_val = benchmark_pi_estimation(10_000_000)
    print(f"Pi estimation: {pi_val:.5f} in {pi_time:.4f} seconds")

    hash_time, hash_sample = benchmark_hashing(5_000_000)
    print(f"Hashing: 5M rounds in {hash_time:.4f} seconds (sample: {hash_sample})")

    log_results(args.system_name, primes_time, pi_time, hash_time)

if __name__ == "__main__":
    main()
