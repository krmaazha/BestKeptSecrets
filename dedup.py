import os

readme_path = r'c:\New folder\BestKeptSecrets\README.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('## 📦 Master List & Community Contributions')
if len(parts) >= 2:
    base_readme = parts[0].rstrip()
    
    # Combine all master list sections
    master_text = "\n\n".join(parts[1:])
    blocks = master_text.strip().split('\n\n')
    
    unique_blocks = []
    seen = set()
    for block in blocks:
        clean_block = block.strip()
        # Ignore sub-header duplicates or boilerplate text
        if clean_block == "This section contains a massive backlog of resources currently being categorized.":
            continue
        if clean_block and clean_block not in seen:
            seen.add(clean_block)
            unique_blocks.append(clean_block)
            
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(base_readme)
        f.write('\n\n## 📦 Master List & Community Contributions\n\n')
        f.write('This section contains a massive backlog of resources currently being categorized.\n\n')
        f.write('\n\n'.join(unique_blocks))
        f.write('\n')
