import os
import argparse
from anthropic import Anthropic
from typing import List

def read_topics_file(topics_file: str) -> List[str]:
    """Read and return lines from the topics file."""
    with open(topics_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def find_report_files(results_dir: str, topic: str) -> List[str]:
    """Find polished report files for a given topic in results directory."""
    topic_safe = topic.replace(" ", "_").lower()
    matches = []
    for root, _, files in os.walk(results_dir):
        for file in files:
            if topic_safe in file.lower() and "polished_report" in file.lower():
                matches.append(os.path.join(root, file))
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
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        temperature=0.3,
        messages=[
            {
                "role": "user",
                "content": prompt.format(reports=formatted_reports)
            }
        ]
    )
    
    return response.content[0].text

def main():
    parser = argparse.ArgumentParser(description='Merge research reports using Claude Sonnet')
    parser.add_argument('--topics-file', required=True, help='Path to the storm topics file')
    parser.add_argument('--results-dir', required=True, help='Path to the results directory')
    parser.add_argument('--output', required=True, help='Path for the merged report output')
    parser.add_argument('--api-key', required=True, help='Anthropic API key')
    
    args = parser.parse_args()
    
    # Initialize Anthropic client
    client = Anthropic(api_key=args.api_key)
    
    # Read topics and collect reports
    topics = read_topics_file(args.topics_file)
    print(f"Found {len(topics)} topics in topics file")
    
    all_reports = []
    for topic in topics:
        report_files = find_report_files(args.results_dir, topic)
        print(f"Found {len(report_files)} report files for topic: {topic}")
        for file_path in report_files:
            content = read_report_content(file_path)
            if content:
                all_reports.append(content)
                print(f"Added content from: {file_path}")
    
    if not all_reports:
        print("No report files found!")
        return
    
    print(f"\nMerging {len(all_reports)} reports...")
    merged_report = merge_reports(client, all_reports)
    
    # Save merged report
    with open(args.output, 'w') as f:
        f.write(merged_report)
    
    print(f"\nMerged report saved to: {args.output}")

if __name__ == "__main__":
    main()
