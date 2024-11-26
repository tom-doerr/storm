#!/bin/bash

# Check if conda exists
if ! command -v conda &> /dev/null; then
    echo "conda could not be found. Please install Anaconda or Miniconda first."
    exit 1
fi

# Initialize conda for bash
CONDA_PATH=$(conda info --base)
source "${CONDA_PATH}/etc/profile.d/conda.sh"

# Check if storm environment exists
if ! conda env list | grep -q "^storm "; then
    echo "storm environment not found. Please create it first with: conda create -n storm python=3.11"
    exit 1
fi

# Activate conda environment
conda activate storm

# Set and create output directory if it doesn't exist
OUTPUT_DIR="./results"
mkdir -p "$OUTPUT_DIR"

# Run the storm script
python examples/storm_examples/run_storm_wiki_gpt.py \
    --output-dir "$OUTPUT_DIR" \
    --retriever you \
    --do-research \
    --do-generate-outline \
    --do-generate-article \
    --do-polish-article
