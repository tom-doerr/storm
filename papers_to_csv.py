import os
import pandas as pd
import glob

def create_papers_csv(papers_dir, output_csv):
    papers = []
    
    # Get all PDF files
    for filepath in glob.glob(os.path.join(papers_dir, "*.pdf")):
        filename = os.path.basename(filepath)
        
        # Read text file with same name as PDF if it exists
        txt_path = filepath.replace('.pdf', '.txt')
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = f"Content from {filename}"
            
        papers.append({
            'content': content,
            'title': filename.replace('.pdf', ''),
            'url': f'paper-{len(papers)}',
            'description': f'Paper extracted from {filename}'
        })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(papers)
    df.to_csv(output_csv, index=False)
    print(f"Created CSV with {len(papers)} papers")

if __name__ == '__main__':
    papers_dir = '/home/tom/git/cf_agent_report_3/downloaded_papers'
    output_csv = 'research_papers.csv'
    create_papers_csv(papers_dir, output_csv)
