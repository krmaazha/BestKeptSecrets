import json
import re

transcript_path = r'C:\Users\hp\.gemini\antigravity-ide\brain\bd21be6f-d462-4ad6-8b3a-8e7715b24648\.system_generated\logs\transcript_full.jsonl'

# Find the user's message containing the 79 entries
content = ""
with open(transcript_path, 'r', encoding='utf-8') as f:
    lines = [json.loads(l) for l in f]
    for line in reversed(lines):
        if line.get('type') == 'USER_INPUT' and 'TradingAgents' in str(line.get('content', '')):
            content = line['content']
            break

# Extract the table
table_lines = []
in_table = False
for line in content.split('\n'):
    if '| Sr. No. | Resource |' in line:
        in_table = True
        continue
    if in_table and line.startswith('|---'):
        continue
    if in_table and line.startswith('|'):
        table_lines.append(line)
    elif in_table and not line.strip():
        in_table = False

# Parse the table and format
formatted_entries = []
for line in table_lines:
    parts = [p.strip() for p in line.split('|')][1:-1]
    if len(parts) >= 5:
        sr, resource, url_raw, analysis, purpose = parts[:5]
        
        # Extract URL
        url_match = re.search(r'`([^`]+)`', url_raw)
        url = url_match.group(1) if url_match else url_raw
        
        # Determine status/icon based on analysis
        icon = '🟡'
        tag = '`Uncategorized`'
        if 'caution' in analysis.lower() or 'pwned' in url.lower() or 'breach' in analysis.lower():
            icon = '🔴'
        elif 'free' in analysis.lower():
            tag = '`Free`'
            icon = '🟢'
            
        formatted_entry = f"- {icon} [**{resource}**]({url}) — {analysis}\n  {tag} · ⚠️ *Review before use.*\n  > 💡 **Use case:** {purpose}\n"
        formatted_entries.append(formatted_entry)

# Also add Intelbase
intelbase = "- 🔴 [**Intelbase**](https://intelbase.is) — A website flagged as a scam with a 10/100 trust score.\n  `Scam` · ⚠️ *High Security Risk. Blacklisted for social engineering and data theft.*\n  > 💡 **Use case:** Avoid. Believed to be a fraudulent platform.\n"

readme_path = r'c:\New folder\BestKeptSecrets\README.md'
with open(readme_path, 'a', encoding='utf-8') as f:
    f.write('\n## 📦 Master List & Community Contributions\n\n')
    f.write('This section contains a massive backlog of resources currently being categorized.\n\n')
    f.write(intelbase + '\n')
    for entry in formatted_entries:
        f.write(entry + '\n')

print(f"Added {len(formatted_entries)} entries and Intelbase.")
