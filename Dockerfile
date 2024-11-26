FROM python:3.11-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only necessary files
COPY requirements.txt .
COPY examples/storm_examples/run_storm_wiki_gpt.py examples/storm_examples/
COPY knowledge_storm knowledge_storm/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONPATH=/app

CMD ["python", "examples/storm_examples/run_storm_wiki_gpt.py"]
