import os
import json
from bs4 import BeautifulSoup
import re
import time

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def build_index(directory, output_file):
    print(f"Starting to index HTML files in {directory}...")
    start_time = time.time()
    
    index_data = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.htm') or file.endswith('.html'):
                filepath = os.path.join(root, file)
                # Skip some heavy or irrelevant directories if any, but we will index all for now
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        html_content = f.read()
                        
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Extract title
                    title = soup.title.string if soup.title else ""
                    title = clean_text(title)
                    
                    # Extract main text
                    # Remove script, style elements
                    for script in soup(["script", "style", "meta", "noscript"]):
                        script.decompose()
                        
                    text = soup.get_text(separator=' ')
                    text = clean_text(text)
                    
                    # Only add if there's meaningful text
                    if len(text) > 50:
                        # Make path relative to the misb directory
                        rel_path = os.path.relpath(filepath, start=os.path.dirname(output_file))
                        # Normalize path for web usage
                        rel_path = rel_path.replace('\\', '/')
                        
                        index_data.append({
                            "path": rel_path,
                            "title": title,
                            "content": text[:5000] # Limit to 5000 chars per file to save memory
                        })
                except Exception as e:
                    pass
                    
    print(f"Indexed {len(index_data)} files.")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False)
        
    print(f"Index saved to {output_file} in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__name__))
    arabic_web_dir = os.path.join(current_dir, "arabic_web")
    output_path = os.path.join(current_dir, "search_index.json")
    
    build_index(arabic_web_dir, output_path)
