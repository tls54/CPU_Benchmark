from time import perf_counter
import hashlib
import random
import platform
import json
from datetime import datetime
from pathlib import Path
import statistics
import sys
import multiprocessing
import subprocess

RESULTS_FILE = "cpu_benchmark_results.jsonl"

def get_cpu_frequency():
    """Get CPU frequency in MHz. Returns None if detection fails."""
    try:
        system = platform.system()

        if system == "Linux":
            # Try reading from /proc/cpuinfo
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if line.startswith("cpu MHz"):
                            freq_str = line.split(":")[1].strip()
                            return float(freq_str)
            except (FileNotFoundError, ValueError, IndexError):
                pass

        elif system == "Darwin":  # macOS
            # Try sysctl command
            try:
                result = subprocess.run(
                    ['sysctl', 'hw.cpufrequency'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    # Output format: hw.cpufrequency: 2400000000
                    freq_hz = int(result.stdout.split(":")[1].strip())
                    return freq_hz / 1_000_000  # Convert to MHz
            except (subprocess.TimeoutExpired, ValueError, IndexError, FileNotFoundError):
                pass

        elif system == "Windows":
            # Try wmic command
            try:
                result = subprocess.run(
                    ['wmic', 'cpu', 'get', 'MaxClockSpeed'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) >= 2:
                        return float(lines[1].strip())
            except (subprocess.TimeoutExpired, ValueError, IndexError, FileNotFoundError):
                pass

    except Exception:
        pass

    return None

def check_system_load():
    """Check system load and warn if high. Returns True to continue, False to abort."""
    try:
        # getloadavg() is available on Unix-like systems
        if hasattr(platform.os, 'getloadavg'):
            load_avg = platform.os.getloadavg()[0]  # 1-minute load average
            cpu_count = multiprocessing.cpu_count()

            if load_avg > cpu_count:
                print(f"\n⚠ Warning: System load is high ({load_avg:.2f}), results may be affected")
                print(f"   (Load average: {load_avg:.2f}, CPU cores: {cpu_count})")
                response = input("   Continue anyway? (y/n): ").strip().lower()
                return response == 'y'
    except Exception:
        # Fail gracefully on Windows or if getloadavg() is not available
        pass

    return True

def benchmark_primes(limit, runs=3):
    """Run prime number benchmark multiple times and return statistics."""
    # Warmup
    for num in range(2, 500):
        _ = all(num % i != 0 for i in range(2, int(num ** 0.5) + 1))

    times = []
    prime_count = 0

    for run in range(runs):
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
        times.append(duration)
        prime_count = len(primes)

    return {
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'stddev': statistics.stdev(times) if len(times) > 1 else 0.0,
        'result': prime_count
    }

def benchmark_pi_estimation(iterations, runs=3):
    """Run pi estimation benchmark multiple times and return statistics."""
    # Warmup
    for _ in range(1000):
        x, y = random.random(), random.random()
        _ = x*x + y*y <= 1

    times = []
    pi_estimate = 0.0

    for run in range(runs):
        start = perf_counter()
        inside_circle = 0
        for _ in range(iterations):
            x, y = random.random(), random.random()
            if x*x + y*y <= 1:
                inside_circle += 1
        pi_estimate = (4.0 * inside_circle) / iterations
        duration = perf_counter() - start
        times.append(duration)

    return {
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'stddev': statistics.stdev(times) if len(times) > 1 else 0.0,
        'result': pi_estimate
    }

def benchmark_hashing(rounds, runs=5):
    """Run hashing benchmark multiple times and return statistics."""
    # Warmup
    data = "benchmarking_is_fun!".encode()
    for _ in range(10000):
        data = hashlib.sha256(data).digest()

    times = []
    hash_result = ""

    for run in range(runs):
        data = "benchmarking_is_fun!".encode()
        start = perf_counter()
        for _ in range(rounds):
            data = hashlib.sha256(data).digest()
        duration = perf_counter() - start
        times.append(duration)
        hash_result = data.hex()[:10]

    return {
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'stddev': statistics.stdev(times) if len(times) > 1 else 0.0,
        'result': hash_result
    }

def benchmark_memory(runs=3):
    """Run memory bandwidth benchmark multiple times and return statistics."""
    # Warmup phase
    warmup_data = list(range(1_000_000))
    _ = sum(warmup_data)

    times = []
    result_sum = 0

    for run in range(runs):
        # Create a list of 5,000,000 integers (approximately 40MB)
        data = list(range(5_000_000))

        start = perf_counter()
        for _ in range(10):
            result_sum = sum(data)  # Sequential read
            data.reverse()  # Write operations
        duration = perf_counter() - start
        times.append(duration)

    return {
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'stddev': statistics.stdev(times) if len(times) > 1 else 0.0,
        'result': result_sum
    }

def log_results(system_name, primes_stats, pi_stats, hash_stats, memory_stats=None):
    """Log benchmark results with statistics and enhanced metadata."""
    cpu_freq = get_cpu_frequency()

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_name": system_name,
        "platform": platform.system(),
        "processor": platform.machine(),
        "python_version": sys.version.split()[0],
        "python_implementation": sys.implementation.name,
        "cpu_cores": multiprocessing.cpu_count(),
        "cpu_freq_mhz": round(cpu_freq, 2) if cpu_freq else None,
        "primes_median": round(primes_stats['median'], 4),
        "primes_min": round(primes_stats['min'], 4),
        "primes_max": round(primes_stats['max'], 4),
        "primes_stddev": round(primes_stats['stddev'], 4),
        "pi_median": round(pi_stats['median'], 4),
        "pi_min": round(pi_stats['min'], 4),
        "pi_max": round(pi_stats['max'], 4),
        "pi_stddev": round(pi_stats['stddev'], 4),
        "hash_median": round(hash_stats['median'], 4),
        "hash_min": round(hash_stats['min'], 4),
        "hash_max": round(hash_stats['max'], 4),
        "hash_stddev": round(hash_stats['stddev'], 4)
    }

    # Add memory stats if provided
    if memory_stats:
        result["memory_median"] = round(memory_stats['median'], 4)
        result["memory_min"] = round(memory_stats['min'], 4)
        result["memory_max"] = round(memory_stats['max'], 4)
        result["memory_stddev"] = round(memory_stats['stddev'], 4)

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

def get_unique_system_name(base_name):
    """Generate a unique system name by appending an integer if the name already exists."""
    results = load_results()
    existing_names = {r['system_name'] for r in results}

    if base_name not in existing_names:
        return base_name

    # Find the next available number
    counter = 2
    while f"{base_name}_{counter}" in existing_names:
        counter += 1

    return f"{base_name}_{counter}"

def display_stats():
    """Display benchmark results in a formatted table with backward compatibility."""
    results = load_results()

    if not results:
        print("\nNo benchmark results found. Run a benchmark first!\n")
        return

    print("\n" + "=" * 140)
    print("CPU BENCHMARK RESULTS")
    print("=" * 140)

    # Check if we have new format results
    has_new_format = any('primes_median' in r for r in results)
    has_memory = any('memory_median' in r for r in results)

    if has_new_format:
        # Enhanced header with statistics
        if has_memory:
            header = f"{'Timestamp':<20} {'System':<15} {'Plat':<8} {'CPU':<5} {'Primes':<10} {'Pi':<10} {'Hash':<10} {'Memory':<10} {'P_SD':<8} {'Pi_SD':<8} {'H_SD':<8} {'M_SD':<8}"
            print(header)
            print("-" * 140)
        else:
            header = f"{'Timestamp':<20} {'System':<15} {'Platform':<10} {'CPU':<5} {'Primes Med':<12} {'Pi Med':<12} {'Hash Med':<12} {'P StdDev':<10} {'Pi StdDev':<10} {'H StdDev':<10}"
            print(header)
            print("-" * 140)

        for result in results:
            # Handle both old and new formats
            if 'primes_median' in result:
                if has_memory and 'memory_median' in result:
                    row = f"{result['timestamp']:<20} {result['system_name']:<15} {result['platform']:<8} {result.get('cpu_cores', 'N/A'):<5} {result['primes_median']:<10.4f} {result['pi_median']:<10.4f} {result['hash_median']:<10.4f} {result['memory_median']:<10.4f} {result['primes_stddev']:<8.4f} {result['pi_stddev']:<8.4f} {result['hash_stddev']:<8.4f} {result['memory_stddev']:<8.4f}"
                elif has_memory:
                    row = f"{result['timestamp']:<20} {result['system_name']:<15} {result['platform']:<8} {result.get('cpu_cores', 'N/A'):<5} {result['primes_median']:<10.4f} {result['pi_median']:<10.4f} {result['hash_median']:<10.4f} {'N/A':<10} {result['primes_stddev']:<8.4f} {result['pi_stddev']:<8.4f} {result['hash_stddev']:<8.4f} {'N/A':<8}"
                else:
                    row = f"{result['timestamp']:<20} {result['system_name']:<15} {result['platform']:<10} {result.get('cpu_cores', 'N/A'):<5} {result['primes_median']:<12.4f} {result['pi_median']:<12.4f} {result['hash_median']:<12.4f} {result['primes_stddev']:<10.4f} {result['pi_stddev']:<10.4f} {result['hash_stddev']:<10.4f}"
            else:
                # Old format fallback
                if has_memory:
                    row = f"{result['timestamp']:<20} {result['system_name']:<15} {result['platform']:<8} {'N/A':<5} {result.get('primes_time', 0):<10.4f} {result.get('pi_time', 0):<10.4f} {result.get('hash_time', 0):<10.4f} {'N/A':<10} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8}"
                else:
                    row = f"{result['timestamp']:<20} {result['system_name']:<15} {result['platform']:<10} {'N/A':<5} {result.get('primes_time', 0):<12.4f} {result.get('pi_time', 0):<12.4f} {result.get('hash_time', 0):<12.4f} {'N/A':<10} {'N/A':<10} {'N/A':<10}"
            print(row)
    else:
        # Old format display
        header = f"{'Timestamp':<20} {'System':<20} {'Platform':<10} {'Processor':<15} {'Primes (s)':<12} {'Pi (s)':<12} {'Hash (s)':<12}"
        print(header)
        print("-" * 120)

        for result in results:
            row = f"{result['timestamp']:<20} {result['system_name']:<20} {result['platform']:<10} {result['processor']:<15} {result.get('primes_time', 0):<12.4f} {result.get('pi_time', 0):<12.4f} {result.get('hash_time', 0):<12.4f}"
            print(row)

    print("=" * 140)
    print(f"Total benchmark runs: {len(results)}\n")

def delete_by_system_name():
    """Delete all benchmark entries for a given system name."""
    results = load_results()

    if not results:
        print("\nNo benchmark results found.\n")
        return

    # Show available system names
    system_names = sorted(set(r['system_name'] for r in results))
    print("\n" + "=" * 60)
    print("AVAILABLE SYSTEM NAMES")
    print("=" * 60)
    for idx, name in enumerate(system_names, 1):
        count = sum(1 for r in results if r['system_name'] == name)
        print(f"{idx}. {name} ({count} entries)")
    print("=" * 60)

    system_name = input("\nEnter system name to delete (or 'cancel' to abort): ").strip()

    if system_name.lower() == 'cancel':
        print("\nDeletion cancelled.\n")
        return

    # Filter out entries with the specified system name
    filtered_results = [r for r in results if r['system_name'] != system_name]

    if len(filtered_results) == len(results):
        print(f"\nNo entries found for system name '{system_name}'.\n")
        return

    deleted_count = len(results) - len(filtered_results)

    # Confirm deletion
    confirm = input(f"\nThis will delete {deleted_count} entries for '{system_name}'. Continue? (y/n): ").strip().lower()

    if confirm != 'y':
        print("\nDeletion cancelled.\n")
        return

    # Write the filtered results back to the file
    with open(RESULTS_FILE, "w") as f:
        for result in filtered_results:
            f.write(json.dumps(result) + "\n")

    print(f"\n✓ Successfully deleted {deleted_count} entries for '{system_name}'.\n")

def show_comparison_and_history(primes_stats, pi_stats, hash_stats, memory_stats):
    """Show comparison to previous run and historical statistics."""
    results = load_results()

    if len(results) < 2:
        print("\nNo previous runs to compare.\n")
        return

    # Get the last two entries (previous and current)
    previous = results[-2]
    current = results[-1]

    print("\n" + "=" * 60)
    print("COMPARISON TO PREVIOUS RUN")
    print("=" * 60)

    # Compare each benchmark if previous run has the new format
    if 'primes_median' in previous:
        # Primes comparison
        primes_diff = ((current['primes_median'] - previous['primes_median']) / previous['primes_median']) * 100
        if primes_diff < 0:
            status = "faster"
            color = ""
        else:
            status = "slower"
            color = ""
        print(f"Primes:  {current['primes_median']:.4f}s ({abs(primes_diff):.1f}% {status})")

        # Pi comparison
        pi_diff = ((current['pi_median'] - previous['pi_median']) / previous['pi_median']) * 100
        if pi_diff < 0:
            status = "faster"
        else:
            status = "slower"
        print(f"Pi:      {current['pi_median']:.4f}s ({abs(pi_diff):.1f}% {status})")

        # Hash comparison
        hash_diff = ((current['hash_median'] - previous['hash_median']) / previous['hash_median']) * 100
        if hash_diff < 0:
            status = "faster"
        else:
            status = "slower"
        print(f"Hash:    {current['hash_median']:.4f}s ({abs(hash_diff):.1f}% {status})")

        # Memory comparison if available
        if 'memory_median' in previous and 'memory_median' in current:
            memory_diff = ((current['memory_median'] - previous['memory_median']) / previous['memory_median']) * 100
            if memory_diff < 0:
                status = "faster"
            else:
                status = "slower"
            print(f"Memory:  {current['memory_median']:.4f}s ({abs(memory_diff):.1f}% {status})")

    print("=" * 60)

    # Historical statistics
    print("\nHISTORICAL STATISTICS")
    print("=" * 60)
    print(f"Total runs: {len(results)}")

    # Calculate percentile rank for current run
    if 'primes_median' in current:
        # Collect all median times for primes
        all_primes_times = [r['primes_median'] for r in results if 'primes_median' in r]
        all_primes_times.sort()
        rank = all_primes_times.index(current['primes_median']) + 1
        print(f"Current run rank: #{rank} out of {len(all_primes_times)} runs (based on primes benchmark)")

        # Consistency indicator
        avg_stddev = (primes_stats['stddev'] + pi_stats['stddev'] + hash_stats['stddev']) / 3
        avg_median = (primes_stats['median'] + pi_stats['median'] + hash_stats['median']) / 3
        variance_pct = (avg_stddev / avg_median) * 100 if avg_median > 0 else 0

        if variance_pct < 5:
            print(f"Consistency: ✓ Results are consistent (variance: {variance_pct:.1f}%)")
        elif variance_pct > 10:
            print(f"Consistency: ⚠ High variance detected (variance: {variance_pct:.1f}%)")
        else:
            print(f"Consistency: Results are acceptable (variance: {variance_pct:.1f}%)")

    print("=" * 60 + "\n")

def run_benchmark():
    """Run the benchmark suite with multiple runs and validation."""
    system_name = input("Enter system name: ").strip()

    if not system_name:
        print("System name cannot be empty!")
        return

    # Generate unique system name if duplicate exists
    unique_name = get_unique_system_name(system_name)
    if unique_name != system_name:
        print(f"Note: System name '{system_name}' already exists. Using '{unique_name}' instead.")
        system_name = unique_name

    # Check system load before running benchmarks
    if not check_system_load():
        print("\nBenchmark aborted.\n")
        return

    print(f"\nRunning CPU Benchmark on: {system_name}")
    print("=" * 40)
    print("Running 3 iterations of each benchmark...")
    print()

    # Prime number benchmark
    print("Running prime number benchmark...")
    primes_stats = benchmark_primes(1_000_000)
    prime_count = primes_stats['result']

    # Validate prime count
    try:
        assert prime_count == 78498, f"Prime count validation failed: expected 78498, got {prime_count}"
        print(f"✓ Primes up to 1,000,000: {prime_count} primes found")
    except AssertionError as e:
        print(f"✗ Validation error: {e}")

    print(f"  Median: {primes_stats['median']:.4f}s | Min: {primes_stats['min']:.4f}s | Max: {primes_stats['max']:.4f}s | StdDev: {primes_stats['stddev']:.4f}s")
    print()

    # Pi estimation benchmark
    print("Running pi estimation benchmark...")
    pi_stats = benchmark_pi_estimation(10_000_000)
    pi_val = pi_stats['result']

    # Validate pi estimation
    try:
        assert 3.13 <= pi_val <= 3.15, f"Pi estimation validation failed: expected 3.13-3.15, got {pi_val:.5f}"
        print(f"✓ Pi estimation: {pi_val:.5f}")
    except AssertionError as e:
        print(f"✗ Validation error: {e}")

    print(f"  Median: {pi_stats['median']:.4f}s | Min: {pi_stats['min']:.4f}s | Max: {pi_stats['max']:.4f}s | StdDev: {pi_stats['stddev']:.4f}s")
    print()

    # Hashing benchmark
    print("Running hashing benchmark...")
    hash_stats = benchmark_hashing(5_000_000)
    hash_sample = hash_stats['result']

    # Validate hash result
    try:
        assert len(hash_sample) == 10 and all(c in '0123456789abcdef' for c in hash_sample), f"Hash validation failed: invalid hex string"
        print(f"✓ Hashing: 5M rounds completed (sample: {hash_sample})")
    except AssertionError as e:
        print(f"✗ Validation error: {e}")

    print(f"  Median: {hash_stats['median']:.4f}s | Min: {hash_stats['min']:.4f}s | Max: {hash_stats['max']:.4f}s | StdDev: {hash_stats['stddev']:.4f}s")
    print()

    # Memory bandwidth benchmark
    print("Running memory bandwidth benchmark...")
    memory_stats = benchmark_memory()
    memory_sum = memory_stats['result']

    # Validate memory result
    try:
        assert memory_sum > 0, f"Memory benchmark validation failed: invalid sum result"
        print(f"✓ Memory bandwidth: 5M elements, 10 iterations completed")
    except AssertionError as e:
        print(f"✗ Validation error: {e}")

    print(f"  Median: {memory_stats['median']:.4f}s | Min: {memory_stats['min']:.4f}s | Max: {memory_stats['max']:.4f}s | StdDev: {memory_stats['stddev']:.4f}s")
    print()

    log_results(system_name, primes_stats, pi_stats, hash_stats, memory_stats)
    print(f"Results saved to {RESULTS_FILE}")

    # Show comparison to previous run and historical statistics
    show_comparison_and_history(primes_stats, pi_stats, hash_stats, memory_stats)

def show_menu():
    """Display the main menu and handle user input."""
    while True:
        print("\n" + "=" * 40)
        print("CPU BENCHMARK SUITE")
        print("=" * 40)
        print("1. Run Benchmark")
        print("2. View Stats")
        print("3. Delete Results by System Name")
        print("4. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            run_benchmark()
        elif choice == "2":
            display_stats()
        elif choice == "3":
            delete_by_system_name()
        elif choice == "4":
            print("\nGoodbye!\n")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.\n")

def main():
    show_menu()

if __name__ == "__main__":
    main()
