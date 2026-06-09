import os
import re
import urllib.parse

def get_actual_case_path(path):
    """
    Given an absolute path, returns the actual case-sensitive path on Windows.
    Returns None if the file/folder does not actually exist.
    """
    # Split the path into parts
    drive, tail = os.path.splitdrive(path)
    parts = []
    while True:
        tail, part = os.path.split(tail)
        if part:
            parts.append(part)
        else:
            if tail:
                parts.append(tail)
            break
    parts.reverse()
    
    current = drive + '\\'
    if not os.path.exists(current):
        return None
        
    for part in parts:
        if part == '\\' or part == '/':
            continue
        try:
            entries = os.listdir(current)
            # Find a case-insensitive match
            match = None
            for e in entries:
                if e.lower() == part.lower():
                    match = e
                    break
            if match:
                current = os.path.join(current, match)
            else:
                return None # Path doesn't exist
        except:
            return None
            
    return current

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
updated_files = 0

for root, dirs, files in os.walk(base_dir):
    if 'scratch' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith('.htm') or f.endswith('.html'):
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='windows-1256') as file:
                        content = file.read()
                except: continue
                
            original_content = content
            
            # Find all href="..."
            # Use a regex that allows replacing the exact matched link
            def replacer(match):
                prefix = match.group(1) # href="
                link = match.group(2)
                suffix = match.group(3) # "
                
                if link.startswith('http') or link.startswith('mailto:') or link.startswith('#') or link == '':
                    return match.group(0)
                    
                # Parse link (remove anchors for path resolution)
                url_parts = urllib.parse.urlsplit(link)
                link_path = urllib.parse.unquote(url_parts.path)
                
                if not link_path:
                    return match.group(0)
                    
                # Get absolute path based on current file location
                link_path_win = link_path.replace('/', '\\')
                full_target_path = os.path.normpath(os.path.join(root, link_path_win))
                
                actual_path = get_actual_case_path(full_target_path)
                
                if actual_path and actual_path != full_target_path:
                    # There is a case mismatch!
                    # We need to reconstruct the relative link with the correct casing
                    rel_actual = os.path.relpath(actual_path, root)
                    rel_actual_posix = rel_actual.replace('\\', '/')
                    
                    # Encode spaces and special chars, but keep the structure
                    new_url_path = urllib.parse.quote(rel_actual_posix)
                    
                    # Reattach query or fragment if they existed
                    new_link = urllib.parse.urlunsplit(('', '', new_url_path, url_parts.query, url_parts.fragment))
                    
                    return prefix + new_link + suffix
                
                return match.group(0)

            # We use re.sub with a function to replace only the link part
            # Regex captures: (href=['"])([^'"]*)(['"])
            new_content = re.sub(r'(href=[\'\"])(.*?)([\'\"])', replacer, content, flags=re.IGNORECASE)
            
            if new_content != original_content:
                # Try to write back with utf-8
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                updated_files += 1
                print(f"Fixed links in: {os.path.relpath(filepath, base_dir)}")

print(f"Total files updated: {updated_files}")
