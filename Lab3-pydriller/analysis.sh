#!/bin/bash

repo=$1
result_dir="${repo}_results"

# Pre-clean and setup
echo "Setting up the results directory..."
rm -rf $result_dir
mkdir $result_dir

# Collect last 500 non-merge commits and extract commit information
echo "Extracting commit data..."
python3 getCommits.py $repo > $result_dir/$repo.commits
python3 getCommitsInfo.py $repo

echo "Analysis complete. Results are stored in the '$result_dir' directory."
