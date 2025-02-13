#!/bin/bash

repo_url="https://github.com/textualize/rich"

repo_name=$(basename $repo_url .git)

echo "Cloning the repository: $repo_url"
git clone $repo_url

bash analysis.sh $repo_name
