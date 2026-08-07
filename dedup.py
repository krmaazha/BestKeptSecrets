import os

readme_path = r'c:\New folder\BestKeptSecrets\README.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The script appended the master list starting with "## 📦 Master List & Community Contributions"
parts = content.split('## 📦 Master List & Community Contributions')
if len(parts) == 2:
    base_readme = parts[0]
    master_list = parts[1].strip().split('\n\n')
    
    unique_blocks = []
    seen = set()
    for block in master_list:
        clean_block = block.strip()
        if clean_block and clean_block not in seen:
            seen.add(clean_block)
            unique_blocks.append(clean_block)
            
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(base_readme)
        f.write('## 📦 Master List & Community Contributions\n\n')
        f.write('\n\n'.join(unique_blocks))
        f.write('\n')
