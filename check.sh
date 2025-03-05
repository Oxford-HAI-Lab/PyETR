#!/bin/bash
output=$(git diff --name-only 2>&1)

if [ -n "$output" ]; then
    echo "Error: Uncommitted changes detected after gen-all command." >&2
    echo "$output" >&2
    exit 1
fi

exit 0
