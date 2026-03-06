#!/bin/bash

# This script is a GIT_ASKPASS helper. It simply outputs the GitHub token
# passed via an environment variable, preventing it from being stored in files
# or command history.

if [ "$1" == "Username for 'https://github.com':" ]; then
    echo "x-oauth-basic"
elif [ "$1" == "Password for 'https://x-oauth-basic@github.com':" ]; then
    echo "$GITHUB_TOKEN"
fi