 
#!/bin/bash

# Set the target directory where you want to clone the repository
target_dir="/home/peerapuns/Documents/ai"

# Set the repository URL
repo_url="https://github.com/snpeerapun/Maxia.git"

# Step 1: Clone the repository if it doesn't exist, or pull if it exists
if [ ! -d "$target_dir" ]; then
    mkdir -p "$target_dir"
    git clone "$repo_url" "$target_dir/Maxia"
else
    cd "$target_dir/Maxia" || exit
    git pull
fi

# Set screen resolution to match the Raspberry Pi's display dimensions
xrandr --output HDMI-1 --mode 1920x1080  # Replace with your actual output and resolution

# Run the Python script
python3 main.py

# Reset the screen resolution to the default after the script finishes
xrandr --output HDMI-1 --auto