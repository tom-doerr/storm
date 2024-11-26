#!/bin/bash

# Check if conda exists
if ! command -v conda &> /dev/null; then
    echo "conda could not be found. Please install Anaconda or Miniconda first."
    exit 1
fi

# Initialize conda for bash
CONDA_PATH=$(conda info --base)
source "${CONDA_PATH}/etc/profile.d/conda.sh"

# Remove existing storm environment if it exists
if conda env list | grep -q "^storm "; then
    echo "Removing existing storm environment..."
    conda deactivate
    conda env remove -n storm
fi

# Create fresh environment with specific dependencies
echo "Creating new storm environment..."
conda create -n storm python=3.11 -y

# Activate conda environment
conda activate storm

# Install required packages
echo "Installing required packages..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers sentence-transformers
pip install tensorflow
pip install openai together

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
