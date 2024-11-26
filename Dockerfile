FROM python:3.11-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

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
