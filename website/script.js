// Initialize Lucide icons
lucide.createIcons();

// Theme Toggle Logic
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Check saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    body.classList.replace('dark-theme', 'light-theme');
}

themeToggle.addEventListener('click', () => {
    if (body.classList.contains('dark-theme')) {
        body.classList.replace('dark-theme', 'light-theme');
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.replace('light-theme', 'dark-theme');
        localStorage.setItem('theme', 'dark');
    }
});

// Brutalist ASCII Rain Effect
function createParticles() {
    const container = document.getElementById('particles');
    container.style.position = 'fixed';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '100vw';
    container.style.height = '100vh';
    container.style.pointerEvents = 'none';
    container.style.zIndex = '-1';
    container.style.overflow = 'hidden';
    
    const chars = ['+', '-', '*', '>', '<', '/', '1', '0', '!', '#', '&', '%'];
    const particleCount = 40;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.innerText = chars[Math.floor(Math.random() * chars.length)];
        particle.style.color = 'var(--text-primary)';
        particle.style.opacity = Math.random() * 0.2 + 0.05;
        particle.style.fontSize = (Math.random() * 20 + 10) + 'px';
        particle.style.fontWeight = 'bold';
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.top = -50 + 'px';
        particle.style.animation = `fall ${Math.random() * 10 + 5}s linear infinite`;
        particle.style.animationDelay = `${Math.random() * 5}s`;
        
        container.appendChild(particle);
    }
}

const style = document.createElement('style');
style.innerHTML = `
@keyframes fall {
    0% { transform: translateY(-50px) rotate(0deg); }
    100% { transform: translateY(110vh) rotate(360deg); }
}
`;
document.head.appendChild(style);
createParticles();

// Fetch and Parse README
let allTools = [];
let categories = new Set();

async function fetchReadme() {
    try {
        // In a real deployed app, this would fetch the raw README from GitHub
        // For local development, we fetch the local file if possible, or fallback
        const response = await fetch('../README.md');
        
        if (!response.ok) {
            throw new Error('Failed to fetch README');
        }
        
        const markdown = await response.text();
        parseTools(markdown);
    } catch (error) {
        console.error('Error fetching README:', error);
        document.getElementById('loading').innerHTML = `
            <i data-lucide="alert-triangle" style="color: var(--warning)"></i>
            <p>Failed to load tools data. Are you running this via a local server?</p>
            <p style="font-size: 0.8rem; color: var(--text-secondary)">Browsers block local file fetching via JavaScript for security reasons.</p>
        `;
        lucide.createIcons();
    }
}

function parseTools(markdown) {
    const lines = markdown.replace(/\r/g, '').split('\n');
    let currentCategory = '';
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        const categoryMatch = line.match(/^##\s+(.+)$/);
        if (categoryMatch && !line.includes('How to Use') && !line.includes('Legend') && !line.includes('Star History') && !line.includes('License') && !line.includes('Contributing')) {
            currentCategory = categoryMatch[1].trim();
            categories.add(currentCategory);
        }
        
        // Match tool entry: - [ICON] [**Name**](url) - Description
        const toolMatch = line.match(/^- ([^\s]+)\s+\[\*\*([^\*]+)\*\*\]\(([^)]+)\)\s+(?:\u2014|-|\u2013)\s+(.+)$/);
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
                
                if (tagLine.includes(' \u00b7 ')) {
                    securityNote = tagLine.split(' \u00b7 ')[1].replace(/^[^a-zA-Z]+/, '').trim();
                }
            }
            
            let useCase = '';
            if (i + 2 < lines.length && lines[i+2].trim().startsWith('>')) {
                useCase = lines[i+2].replace(/^>\s*(?:💡|\?\?|[^a-zA-Z]+)?\s*/, '').replace('**Use case:**', '').trim();
            }
            
            let status = 'safe';
            if (statusIcon.includes('🟡') || statusIcon.includes('Y')) status = 'caution';
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
    
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('toolCount').textContent = `${allTools.length}+`;
    
    renderCategories();
    renderTools(allTools);
}

function renderCategories() {
    const container = document.getElementById('categoryFilters');
    
    Array.from(categories).forEach(category => {
        const btn = document.createElement('button');
        btn.className = 'filter-btn';
        btn.textContent = category.replace(/^[^\sA-Za-z]+/, '').trim(); // Remove emoji for cleaner look
        btn.dataset.filter = category;
        
        btn.addEventListener('click', () => {
            // Update active state
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            filterTools();
        });
        
        container.appendChild(container.lastElementChild); // Move "All Tools" to end, or keep at start
        container.insertBefore(btn, container.lastElementChild);
    });
    
    // Add event listener to "All Tools" button
    document.querySelector('[data-filter="all"]').addEventListener('click', (e) => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        filterTools();
    });
}

function renderTools(tools) {
    const container = document.getElementById('toolsGrid');
    const noResults = document.getElementById('noResults');
    
    container.innerHTML = '';
    
    if (tools.length === 0) {
        container.classList.add('hidden');
        noResults.classList.remove('hidden');
        return;
    }
    
    container.classList.remove('hidden');
    noResults.classList.add('hidden');
    
    tools.forEach(tool => {
        const card = document.createElement('a');
        card.href = tool.url;
        card.target = '_blank';
        card.className = 'tool-card';
        card.style.color = 'inherit'; // Prevent link styling overriding card text
        
        const tagsHtml = tool.tags.map(tag => `<span class="tag">${tag}</span>`).join('');
        
        // Clean markdown from security note (remove * and formatting)
        const cleanNote = tool.securityNote.replace(/\*/g, '').replace(/⚠️|✅/, '').trim();
        const noteIcon = tool.securityNote.includes('✅') ? 'check-circle' : 'alert-triangle';
        
        card.innerHTML = `
            <div class="tool-header">
                <div class="tool-title-group">
                    <span class="icon" style="font-size: 1.5rem">${tool.statusIcon}</span>
                    <div>
                        <div class="tool-category">${tool.category.replace(/^[^\sA-Za-z]+/, '').trim()}</div>
                        <h3 class="tool-name">${tool.name}</h3>
                    </div>
                </div>
                <i data-lucide="external-link" style="color: var(--text-secondary); width: 1.2rem; height: 1.2rem;"></i>
            </div>
            
            <p class="tool-desc">${tool.description}</p>
            
            <div class="tags">
                ${tagsHtml}
            </div>
            
            ${cleanNote ? `
            <div class="security-note ${tool.status}">
                <div style="display: flex; gap: 0.5rem; align-items: flex-start;">
                    <i data-lucide="${noteIcon}" style="width: 1rem; height: 1rem; margin-top: 0.1rem; flex-shrink: 0"></i>
                    <span>${cleanNote}</span>
                </div>
            </div>` : ''}
            
            ${tool.useCase ? `
            <div class="use-case">
                <strong>💡 Use case:</strong> ${tool.useCase}
            </div>` : ''}
        `;
        
        container.appendChild(card);
    });
    
    lucide.createIcons();
}

function filterTools() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;
    
    const filtered = allTools.filter(tool => {
        // Category match
        const categoryMatch = activeFilter === 'all' || tool.category === activeFilter;
        
        // Search match
        const searchMatch = !searchTerm || 
            tool.name.toLowerCase().includes(searchTerm) || 
            tool.description.toLowerCase().includes(searchTerm) ||
            tool.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
            tool.category.toLowerCase().includes(searchTerm);
            
        return categoryMatch && searchMatch;
    });
    
    renderTools(filtered);
}

// Search input listener
document.getElementById('searchInput').addEventListener('input', filterTools);

// Start fetching
fetchReadme();
