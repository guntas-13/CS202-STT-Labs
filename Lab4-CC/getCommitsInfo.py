import sys
import csv
from pydriller import Repository

columns = [
    "old_file_path",
    "new_file_path",
    "commit_SHA",
    "parent_commit_SHA",
    "commit_message",
    "diff_histogram",
    "source_code_old",
    "source_code_new",
    "old_file_MCC",
    "new_file_MCC"
]

rows = []
count = 0
last_n = 500

repo_path = sys.argv[1]

commits = list(Repository(repo_path, only_no_merge=True, order='reverse', histogram_diff=True).traverse_commits())
commits = commits[:last_n][::-1]

for i, commit in enumerate(commits):
    print(f"[{i+1}/{len(commits)}] Processing commit {commit.hash}...")

    for modified_file in commit.modified_files:
        if modified_file.filename.endswith('.py') and modified_file.source_code_before:
            diff_histogram = modified_file.diff_parsed

            rows.append([
                modified_file.old_path,
                modified_file.new_path,
                commit.hash,
                commit.parents[0] if commit.parents else None,
                commit.msg,
                diff_histogram,
                modified_file.source_code_before,
                modified_file.source_code,
                modified_file.complexity,
                sum(method.complexity for method in modified_file.methods_before)
            ])

# Write to CSV
output_file = f"{repo_path}_results/commits_info.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Dataset saved to {output_file}")