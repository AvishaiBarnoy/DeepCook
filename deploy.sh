 #!/bin/sh

# If a command fails then the deploy stops
set -e

printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

# Go To Public folder
pwd

# Add changes to git.
git add .

# Commit changes.
msg="rebuilding numeric caveoling package $(date)"
if [ -n "$*" ]; then
		msg="$*"
	fi
	git commit -m "$msg"

	# Push source and build repos.
	git push origin `git branch --show-current`
