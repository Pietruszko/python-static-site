#!/bin/bash
# build.sh - Build the site for GitHub Pages deployment

set -e  # Exit on error

echo "Building site for GitHub Pages..."
REPO_NAME="python-static-site"
python3 src/main.py "/$REPO_NAME/"

echo "Build completed! Site is in the docs/ directory."
