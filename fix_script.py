import os

script_path = r'c:\New folder\BestKeptSecrets\website\script.js'

with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace regex
content = content.replace(
    'const toolMatch = line.match(/^- (🟢|🟡|🔴)\\s+\\[\\*\\*([^\\*]+)\\*\\*\\]\\(([^)]+)\\)\\s+(?:—|-)\\s+(.+)$/);',
    'const toolMatch = line.match(/^- ([^\\s]+)\\s+\\[\\*\\*([^\\*]+)\\*\\*\\]\\(([^)]+)\\)\\s+(?:—|-|–)\\s+(.+)$/);'
)

# Handle mangled regex if it exists
import re
content = re.sub(
    r'const toolMatch = line\.match\(\/\^- \([^)]+\)\\s\+\\\[\\\*\\\*\(\[\^\\\*\]\+\)\\\*\\\*\\\]\\(\(\[\^)]\+\)\\)\\s\+\(\?:\—\|-\)\\s\+\(\.\+\)\$\/\);',
    r'const toolMatch = line.match(/^- ([^\\s]+)\\s+\\[\\*\\*([^\\*]+)\\*\\*\\]\\(([^)]+)\\)\\s+(?:—|-|–|—)\\s+(.+)$/);',
    content
)

# Also fix the usecase line matching which has the lightbulb emoji
content = re.sub(
    r'if \(i \+ 2 < lines\.length && lines\[i\+2\]\.startsWith\([^)]+\)\) {',
    r'if (i + 2 < lines.length && lines[i+2].trim().startsWith(">")) {',
    content
)
content = re.sub(
    r'useCase = lines\[i\+2\]\.replace\([^)]+\)\.replace\(\'\*\*Use case:\*\*\', \'\'\)\.trim\(\);',
    r'useCase = lines[i+2].replace(/^>\s*(?:💡|[^\w\s]+)?\s*/, "").replace("**Use case:**", "").trim();',
    content
)

# And fix the status icon check
content = re.sub(
    r"if \(statusIcon === '🟡'\) status = 'caution';",
    r"if (statusIcon.includes('🟡') || statusIcon.includes('Y')) status = 'caution';",
    content
)
content = re.sub(
    r"if \(statusIcon === '🔴'\) status = 'warning';",
    r"if (statusIcon.includes('🔴') || statusIcon.includes('dYY') || statusIcon.includes('O')) status = 'warning';",
    content
)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed script.js")
