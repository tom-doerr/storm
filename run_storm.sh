#!/bin/bash

# Initialize conda
eval "$(conda init bash)"
source ~/.bashrc

# Activate conda environment
conda activate storm

# Set output directory
export OUTPUT_DIR="./results"

# Run the storm script
python examples/storm_examples/run_storm_wiki_gpt.py \
    --output-dir $OUTPUT_DIR \
    --retriever you \
    --do-research \
    --do-generate-outline \
    --do-generate-article \
    --do-polish-article
