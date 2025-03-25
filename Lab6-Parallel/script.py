import subprocess
import time
import csv
import os

CSV_FILE = "pytest_sequential_1.csv"
NUM_RUNS = 5

def run_pytest():
    start_time = time.time()
    result = subprocess.run(["python3", "-m", "pytest", "--tb=short", "tests"], capture_output=True, text=True)
    end_time = time.time()
    
    execution_time = end_time - start_time
    return execution_time, result.stdout

def main():
    os.chdir("algorithms")
    
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Run Number", "Execution Time (s)", "Summary"])
        
        for i in range(1, NUM_RUNS + 1):
            execution_time, output = run_pytest()
            # the last line of the output looks like this:
            # ======================== 2 failed, 414 passed in 4.29s =========================
            # parsing out the middle text
            lastLine = " ".join(output.split("\n")[-2].split(" ")[1:-1])
            print(f"Run {i}: {execution_time} seconds")
            writer.writerow([i, execution_time, lastLine])
    
    print(f"Execution times saved to {CSV_FILE}")

if __name__ == "__main__":
    main()
