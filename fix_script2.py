import os

script_path = r'c:\New folder\BestKeptSecrets\website\script.js'

with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re

# We want to replace the body of parseTools
# Find the start of the function
start_idx = content.find('function parseTools(markdown) {')
end_idx = content.find("document.getElementById('loading').classList.add('hidden');")

if start_idx != -1 and end_idx != -1:
    new_parse_tools = """function parseTools(markdown) {
    const lines = markdown.split('\\n');
    let currentCategory = '';
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        const categoryMatch = line.match(/^##\\s+(.+)$/);
        if (categoryMatch && !line.includes('How to Use') && !line.includes('Legend') && !line.includes('Star History') && !line.includes('License') && !line.includes('Contributing')) {
            currentCategory = categoryMatch[1].trim();
            categories.add(currentCategory);
        }
        
        // Match tool entry: - [ICON] [**Name**](url) - Description
        const toolMatch = line.match(/^- ([^\\s]+)\\s+\\[\\*\\*([^\\*]+)\\*\\*\\]\\(([^)]+)\\)\\s+(?:—|-|–|?")\\s+(.+)$/);
        if (toolMatch) {
            const statusIcon = toolMatch[1];
            const name = toolMatch[2];
            const url = toolMatch[3];
            const description = toolMatch[4];
            
            let tags = [];
            let securityNote = '';
            if (i + 1 < lines.length && lines[i+1].includes('`')) {
                const tagLine = lines[i+1];
                const tagMatches = [...tagLine.matchAll(/`([^`]+)`/g)];
                tags = tagMatches.map(m => m[1]);
                
                if (tagLine.includes('·') || tagLine.includes('')) {
                    const splitChar = tagLine.includes('·') ? '·' : (tagLine.includes('') ? '' : '');
                    if (splitChar) securityNote = tagLine.split(splitChar)[1].replace(/^[^a-zA-Z]+/, '').trim();
                }
            }
            
            let useCase = '';
            if (i + 2 < lines.length && lines[i+2].trim().startsWith('>')) {
                useCase = lines[i+2].replace(/^>\\s*(?:💡|\\?\\?|[^a-zA-Z]+)?\\s*/, '').replace('**Use case:**', '').trim();
            }
            
            let status = 'safe';
            if (statusIcon.includes('🟡') || statusIcon.includes('Y') || statusIcon.includes('')) status = 'caution';
            if (statusIcon.includes('🔴') || statusIcon.includes('dYY') || statusIcon.includes('O')) status = 'warning';
            if (statusIcon.includes('🟢')) status = 'safe';
            
            allTools.push({
                name,
                url,
                description,
                category: currentCategory,
                status,
                statusIcon,
                tags,
                securityNote,
                useCase
            });
        }
    }
    
    """
    
    new_content = content[:start_idx] + new_parse_tools + content[end_idx:]
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed script.js")
else:
    print("Could not find start or end index.")
