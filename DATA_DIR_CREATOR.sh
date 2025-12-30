#!/bin/bash

# Activate the virtual environment for SOFTware-Sync
source ./venv/bin/activate

# Check if ../data exists before trying to remove it
if [ -d "../data" ]; then
    rm -r ../data
fi

# Run the Python script
python ../SOFTware-Sync/main.py --data-dir

# Check if ./data exists before trying to move it
if [ -d "./data" ]; then
    mv ./data/ ../
else
    echo "No data directory to move."
fi

# Create the pdf directory
mkdir -p ../data/pdf_files/