#!/bin/bash

# Set the target directory where you want to clone the repository
target_dir="/home/peerapuns/Documents/ai/Maxia"

# Set the repository URL
repo_url="https://github.com/snpeerapun/Maxia.git"

# Step 1: Clone the repository
if [ ! -d "$target_dir" ]; then
    mkdir -p "$target_dir"
fi

cd "$target_dir" || exit
git clone "$repo_url"

# Step 2: Navigate to the repository directory and run Python script
#cd "yourrepository" || exit
python3 main.py
