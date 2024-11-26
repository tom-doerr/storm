FROM ubuntu:22.04

WORKDIR /app

# Update GPG keys and install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gpg-agent \
    wget \
    && rm -rf /var/lib/apt/lists/* && \
    wget -O - https://archive.ubuntu.com/ubuntu/project/ubuntu-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/ubuntu-archive-keyring.gpg

# Install Python and essential system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set Python aliases
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

# Copy only necessary files first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY examples/storm_examples/run_storm_wiki_gpt.py examples/storm_examples/
COPY knowledge_storm knowledge_storm/

# Set environment variables
ENV PYTHONPATH=/app

# Create a directory for results
RUN mkdir -p /app/results

ENTRYPOINT ["python", "examples/storm_examples/run_storm_wiki_gpt.py", "--output-dir", "/app/results"]
