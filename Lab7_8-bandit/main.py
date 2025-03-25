import sys
import os
import json
import subprocess
from pydriller import Repository
import csv

columns = [
    "commit",
    "sev_high",
    "sev_med",
    "sev_low",
    "conf_high",
    "conf_med",
    "conf_low",
    "cwe"
]

def get_commits(repo_path, output_file, num_commits):
    print(f"Extracting last {num_commits} non-merge commits...")
    
    commits = [commit.hash for commit in Repository(repo_path, only_no_merge=True, order='reverse').traverse_commits() if commit.in_main_branch][:num_commits]
    
    with open(output_file, 'w') as f:
        for commit in commits:
            f.write(commit + "\n")
    
    print(f"Commits saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    repo_name = os.path.basename(repo_url)
    repo_path = os.path.join('./repositories', repo_name)

    os.makedirs("repositories", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    print(f"Cloning repository {repo_url}...")

    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        print(f"Repository cloned to {repo_path}")
    else:
        print(f"Repository {repo_name} already exists, skipping clone.")

    output_dir = os.path.join("results", repo_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory created at {output_dir}")

    commits_file = os.path.join(output_dir, "commits.txt")
    get_commits(repo_path, commits_file, num_commits=100)
    
    with open(commits_file, "r") as f:
        commits = [line.strip() for line in f.readlines()]
    
    results = []
    
    for i, commit_hash in enumerate(commits):
        print(f"Checking out commit {commit_hash}...")
        subprocess.run(["git", "-C", repo_path, "checkout", commit_hash, "-q"], check=True, timeout=300)
        
        result_file = os.path.join(output_dir, f"Commit{i}.json")
        print(f"Running Bandit on commit {commit_hash}...")
        
        try:
            cmd = ["bandit", "-r", repo_path, "-f", "json", "-o", result_file, "-q"]
            subprocess.run(cmd, check=True, timeout=300)
        except subprocess.CalledProcessError as e:
            print(f"Bandit failed on commit {commit_hash}: {e}")
            print("-" * 50)
            print()
            

        with open(result_file, "r") as f:
            data = json.load(f)

        sev_high, sev_med, sev_low = 0, 0, 0
        conf_high, conf_med, conf_low = 0, 0, 0
        cwe = set()

        for item in data["results"]:
            if item["issue_severity"] == "HIGH":
                sev_high += 1
            elif item["issue_severity"] == "MEDIUM":
                sev_med += 1
            elif item["issue_severity"] == "LOW":
                sev_low += 1

            if item["issue_confidence"] == "HIGH":
                conf_high += 1
            elif item["issue_confidence"] == "MEDIUM":
                conf_med += 1
            elif item["issue_confidence"] == "LOW":
                conf_low += 1

            if "issue_cwe" in item and isinstance(item["issue_cwe"], dict) and "id" in item["issue_cwe"]:
                cwe.add(str(item["issue_cwe"]["id"]))

        data = [
            commit_hash,
            sev_high,
            sev_med,
            sev_low,
            conf_high,
            conf_med,
            conf_low,
            ",".join(cwe)
        ]
        results.append(data)
        print(columns)
        print(data)
        print(f"Analysis saved to {result_file}")
        print("-" * 50)
        print()

    csv_file = os.path.join(output_dir, "results.csv")
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)

    print(f"CSV file created at {csv_file}")