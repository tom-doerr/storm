import os
import argparse
from pathlib import Path
from anthropic import Anthropic
from typing import List

def read_topics_file(topics_file: str) -> List[str]:
    """Read and return lines from the topics file."""
    with open(topics_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def find_report_files(results_dir: str, topic: str) -> List[str]:
    """Find polished report files for a given topic in results directory."""
    # Convert topic line to directory name format
    topic_dir = topic.replace(": ", ":_").replace(", ", ",_").replace(" ", "_")
    
    matches = []
    # Look in both gpt and claude subdirectories
    for model_dir in ['gpt', 'claude']:
        full_path = os.path.join(results_dir, model_dir, topic_dir, "storm_gen_article_polished.txt")
        if os.path.exists(full_path):
            matches.append(full_path)
    
    return matches

def read_report_content(file_path: str) -> str:
    """Read and return the content of a report file."""
    with open(file_path, 'r') as f:
        return f.read().strip()

def merge_reports(client: Anthropic, reports: List[str]) -> str:
    """Use Claude to merge multiple report sections into one coherent document."""
    
    prompt = """You are a skilled technical writer and researcher. Please merge these research report sections into one cohesive document that maintains academic rigor while being engaging and clear.

Key requirements:
1. Maintain consistent academic tone and technical precision
2. Ensure logical flow between sections with smooth transitions
3. Eliminate redundancies while preserving all unique information
4. Add clear section headings and structure
5. Preserve all technical details and citations
6. Conclude with a synthesis that ties the sections together

Here are the sections to merge:

{reports}

Please provide a single, well-structured academic report that integrates all this information effectively."""

    formatted_reports = "\n\n=== NEW SECTION ===\n\n".join(reports)
    
    print(f"\nSending merge request to Claude API...")
    print(f"Number of sections to merge: {len(reports)}")
    print(f"Total input length: {len(formatted_reports)} characters")
    
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229-v3:5",
            max_tokens=100000,  # Increased token limit
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt.format(reports=formatted_reports)
                }
            ]
        )
        print(f"Received response from Claude API")
        print(f"Response length: {len(response.content[0].text)} characters")
        return response.content[0].text
        
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Merge research reports using Claude Sonnet')
    parser.add_argument('--output', default='results/merged_report.md', 
                       help='Path for the merged report output (default: results/merged_report.md)')
    
    args = parser.parse_args()
    
    # Get API key from environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")
    
    # Initialize Anthropic client
    client = Anthropic(api_key=api_key)
    
    # Use fixed paths
    topics_file = Path("storm_topics.txt")
    results_dir = Path("results")
    
    if not topics_file.exists():
        raise FileNotFoundError(f"Topics file not found: {topics_file}")
    if not results_dir.exists():
        raise FileNotFoundError(f"Results directory not found: {results_dir}")
    
    # Read topics and collect reports
    topics = read_topics_file(str(topics_file))
    print(f"Found {len(topics)} topics in topics file")
    
    all_reports = []
    for topic in topics:
        report_files = find_report_files(str(results_dir), topic)
        print(f"Found {len(report_files)} report files for topic: {topic}")
        for file_path in report_files:
            try:
                content = read_report_content(file_path)
                if content:
                    all_reports.append(content)
                    print(f"Added content from: {file_path}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    if not all_reports:
        print("No report files found!")
        return
    
    print(f"\nMerging {len(all_reports)} reports...")
    merged_report = merge_reports(client, all_reports)
    
    # Ensure results directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Save merged report
    with open(args.output, 'w') as f:
        f.write(merged_report)
    
    print(f"\nMerged report saved to: {args.output}")

if __name__ == "__main__":
    main()
