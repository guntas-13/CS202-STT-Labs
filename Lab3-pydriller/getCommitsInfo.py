import sys
import csv
from pydriller import Repository

columns = [
    "old_file_path",
    "new_file_path",
    "commit_SHA",
    "parent_commit_SHA",
    "commit_message",
    "diff_myers",
    "diff_histogram",
    "diff_match"
]

rows = []
count = 0
last_n = 500

repo_path = sys.argv[1]

commits = list(Repository(repo_path, only_no_merge = True, order = 'reverse').traverse_commits())
commits_histogram = list(Repository(repo_path, only_no_merge = True, order = 'reverse', histogram_diff = True).traverse_commits())
commits_histogram = commits_histogram[:last_n][::-1]
commits = commits[:last_n][::-1]

for i, (commit, commit_histogram) in enumerate(zip(commits, commits_histogram)):
    print(f"[{i+1}/{len(commits)}] Processing commit {commit.hash}...")

    for modified_file, modified_file_histogram in zip(commit.modified_files, commit_histogram.modified_files):

        diff_histogram = modified_file_histogram.diff_parsed
        diff_myers = modified_file.diff_parsed
        
        diff_match = "Yes" if diff_histogram == diff_myers else "No"
        
        rows.append([
            modified_file.old_path,
            modified_file.new_path,
            commit.hash,
            commit.parents[0] if commit.parents else None,
            commit.msg,
            diff_myers,
            diff_histogram,
            diff_match
        ])

# Write to CSV
output_file = f"{repo_path}_results/commits_info.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Dataset saved to {output_file}")