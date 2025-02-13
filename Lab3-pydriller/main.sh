#!/bin/bash

# Clone the specified repository
# repo_url="https://github.com/JakeWharton/butterknife"
repo_url="https://github.com/ChatGPTNextWeb/NextChat"

repo_name=$(basename $repo_url .git)

echo "Cloning the repository: $repo_url"
git clone $repo_url

# Execute the analysis for the repository
bash analysis.sh $repo_name
