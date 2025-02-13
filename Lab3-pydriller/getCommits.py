import sys
from pydriller import Repository

# Variables
count = 0
last_n = 500  # Number of commits to extract
commit_reverse = []

# Traverse commits in reverse order
for commit in Repository(sys.argv[1], only_no_merge=True, order='reverse').traverse_commits():
    if commit.in_main_branch:
        commit_reverse.append(commit.hash)
        count += 1
        if count == last_n:
            break

# Print commits in chronological order
commit_reverse.reverse()
print('\n'.join(commit_reverse))
