#!/bin/bash

# ROSBag to CSV converter script
# Usage: ./convert_rosbag.sh <rosbag_directory> <output_file_prefix>

# Function to display usage
usage() {
    echo "Usage: $0 <rosbag_directory> <output_file_prefix>"
    echo "Converts ROSBag data to CSV format using two different converters"
    echo ""
    echo "Arguments:"
    echo "  rosbag_directory     Directory containing the ROSBag data"
    echo "  output_file_prefix   Prefix for output CSV files"
    echo "                       Will create: <prefix>_command.csv and <prefix>_joint_states.csv"
    exit 1
}

# Check if both arguments are provided
if [ $# -ne 2 ]; then
    echo "Error: Please provide both the ROSBag directory and output file prefix"
    usage
fi

# Check if the directory exists
if [ ! -d "$1" ]; then
    echo "Error: Directory '$1' does not exist"
    exit 1
fi

# Check if Python scripts exist
if [ ! -f "convert_rosbag2_command_to_csv.py" ]; then
    echo "Error: convert_rosbag2_command_to_csv.py not found"
    exit 1
fi

if [ ! -f "convert_rosbag2_joint_states_to_csv.py" ]; then
    echo "Error: convert_rosbag2_joint_states_to_csv.py not found"
    exit 1
fi

# Set output file names
command_output="${2}_command.csv"
joint_states_output="${2}_joint_states.csv"

# Convert the ROSBag data
echo "Converting command data to CSV..."
python3 convert_rosbag2_command_to_csv.py "$1" -o "$command_output"

echo "Converting joint states data to CSV..."
python3 convert_rosbag2_joint_states_to_csv.py "$1" -o "$joint_states_output"

echo "Conversion complete!"
echo "Output files:"
echo "  - $command_output"
echo "  - $joint_states_output"