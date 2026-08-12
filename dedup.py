import re

readme_path = r'c:\New folder\BestKeptSecrets\README.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Separate base content (categorized sections up to ## 📦 Master List)
master_header = '## 📦 Master List & Community Contributions'
parts = content.split(master_header)

base_content = parts[0].rstrip()

# 2. Extract tools from base_content to avoid duplicating them in master list
base_tools = set()
base_matches = re.findall(r'^- [^\s]+\s+\[\*\*([^\*]+)\*\*\]\(([^)]+)\)', base_content, re.MULTILINE)
for name, url in base_matches:
    base_tools.add(name.strip().lower())
    base_tools.add(url.strip().lower())

# 3. Parse all tool entries across all master list sections
master_text = "\n\n".join(parts[1:])
lines = master_text.split('\n')

entries = []
current_entry = []

for line in lines:
    if re.match(r'^- [^\s]+\s+\[\*\*([^\*]+)\*\*\]', line):
        if current_entry:
            entries.append("\n".join(current_entry))
            current_entry = []
    if current_entry or re.match(r'^- [^\s]+\s+\[\*\*([^\*]+)\*\*\]', line):
        current_entry.append(line)

if current_entry:
    entries.append("\n".join(current_entry))

# 4. Deduplicate master entries
seen = set()
unique_entries = []

for entry in entries:
    m = re.search(r'^- [^\s]+\s+\[\*\*([^\*]+)\*\*\]\(([^)]+)\)', entry)
    if m:
        name = m.group(1).strip().lower()
        url = m.group(2).strip().lower()
        if name not in seen and url not in seen and name not in base_tools and url not in base_tools:
            seen.add(name)
            seen.add(url)
            unique_entries.append(entry.strip())

# 5. Reconstruct README.md cleanly
new_readme = base_content + "\n\n" + master_header + "\n\nThis section contains a backlog of resources currently being categorized.\n\n" + "\n\n".join(unique_entries) + "\n"

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(new_readme)

print(f"Deduplicated successfully! Retained {len(unique_entries)} unique backlog entries.")
