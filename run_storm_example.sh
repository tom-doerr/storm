#!/bin/bash

# Exit on error
set -e

# Initialize conda for bash
echo "Initializing conda..."
source ~/miniconda3/etc/profile.d/conda.sh

# Create and activate conda environment
echo "Creating conda environment..."
conda create -n storm python=3.11 --yes
conda activate storm

# Install required packages
echo "Installing packages..."
pip install knowledge-storm

# Create secrets.toml if it doesn't exist
if [ ! -f secrets.toml ]; then
    echo "Creating secrets.toml..."
    cat > secrets.toml << EOL
# Set up OpenAI API key
OPENAI_API_KEY="your_openai_api_key"
# If using OpenAI directly
OPENAI_API_TYPE="openai"

# If using Azure OpenAI, uncomment and fill these:
# OPENAI_API_TYPE="azure"
# AZURE_API_BASE="your_azure_api_base_url"
# AZURE_API_VERSION="your_azure_api_version"

# Set up You.com search API key
YDC_API_KEY="your_youcom_api_key"
EOL
    echo "Please edit secrets.toml with your actual API keys before running the example"
    exit 1
fi

# Run the example
echo "Running STORM example..."
python examples/storm_examples/run_storm_wiki_serper.py
