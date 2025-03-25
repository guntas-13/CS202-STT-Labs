import subprocess
import time
import csv
import os

CSV_FILE = "pytest_parallel_results.csv"
NUM_RUNS = 3
WORKERS = ["1", "auto"]
THREADS = ["1", "auto"]
DIST_MODES = ["load", "no"]

def run_pytest(num_workers, num_threads, dist_mode):
    """Runs pytest with given parallelization settings and records execution time."""
    command = [
        "python3", "-m", "pytest", 
        f"-n={num_workers}", f"--dist={dist_mode}", 
        f"--parallel-threads={num_threads}", "--tb=short", "tests"
    ]
    
    execution_times = []
    summaries = []

    for _ in range(NUM_RUNS):
        start_time = time.time()
        result = subprocess.run(command, capture_output=True, text=True)
        end_time = time.time()

        execution_time = end_time - start_time
        execution_times.append(execution_time)

        # Extracting the last line with test results
        last_line = " ".join(result.stdout.split("\n")[-2].split(" ")[1:-1])
        summaries.append(last_line)

    avg_time = sum(execution_times) / NUM_RUNS
    return execution_times, summaries, avg_time

def main():
    os.chdir("algorithms")

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Workers", "Threads", "Dist", "Run 1 (s)", "Run 2 (s)", "Run 3 (s)", "Avg Time (s)", "Summary 1", "Summary 2", "Summary 3"])

        for workers in WORKERS:
            for threads in THREADS:
                for dist in DIST_MODES:
                    exec_times, summaries, avg_time = run_pytest(workers, threads, dist)
                    print(f"Workers={workers}, Threads={threads}, Dist={dist} -> {exec_times} (Avg: {avg_time:.4f}s)\nSummaries: {summaries}\n")
                    writer.writerow([workers, threads, dist, *exec_times, avg_time, *summaries])

    print(f"Results saved to {CSV_FILE}")

if __name__ == "__main__":
    main()