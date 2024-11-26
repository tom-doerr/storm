#!/bin/bash

# Check if input file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 topics.txt"
    echo "Where topics.txt contains one topic per line"
    exit 1
fi

# Check if input file exists
if [ ! -f "$1" ]; then
    echo "Error: File $1 does not exist"
    exit 1
fi

# Process each topic
while IFS= read -r topic || [ -n "$topic" ]; do
    echo "Processing topic: $topic"
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python3 -W ignore ./examples/storm_examples/run_storm_wiki_gpt.py \
        --retriever brave \
        --do-research \
        --do-generate-outline \
        --do-generate-article \
        --do-polish-article \
        --remove-duplicate \
        "$topic"
    
    echo "Completed processing: $topic"
    echo "Waiting 3 seconds before next topic..."
    sleep 3
done < "$1"

echo "All topics processed"
