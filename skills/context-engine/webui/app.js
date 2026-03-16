document.addEventListener('DOMContentLoaded', () => {
    init();
});

let Graph = null;
let graphData = { nodes: [], links: [] };

async function init() {
    updateStatus();
    loadScratchpad();
    loadIngestion();
    initGraph();

    // Refresh loop
    setInterval(updateStatus, 5000);
    setInterval(loadScratchpad, 10000);
    setInterval(loadIngestion, 10000);
    setInterval(loadGraph, 10000);

    document.getElementById('reset-view').addEventListener('click', () => {
        if (Graph) {
            Graph.cameraPosition({ x: 0, y: 0, z: 250 }, { x: 0, y: 0, z: 0 }, 1000);
        }
    });
}

async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        const statusEl = document.getElementById('status-text');

        if (data.status === 'online') {
            statusEl.innerText = 'ONLINE';
            statusEl.className = 'status-online';
        } else {
            statusEl.innerText = 'OFFLINE';
            statusEl.className = 'status-offline';
        }
    } catch (err) {
        document.getElementById('status-text').innerText = 'ERROR';
        document.getElementById('status-text').className = 'status-offline';
    }
}

async function loadScratchpad() {
    try {
        const response = await fetch('/api/scratchpad');
        const data = await response.json();
        renderScratchpad(data);
    } catch (err) {
        console.error('Failed to load scratchpad:', err);
    }
}

function renderScratchpad(items) {
    const listEl = document.getElementById('scratchpad-list');
    if (!items || items.length === 0) {
        listEl.innerHTML = '<div class="qa-card">No session findings recorded.</div>';
        return;
    }

    listEl.innerHTML = items.map(item => `
        <div class="qa-card">
            <div class="date">${new Date(item.date).toLocaleString()} <span class="badge phase-${item.phase}">${item.phase}</span></div>
            <pre>${item.content}</pre>
        </div>
    `).join('');
}

async function loadIngestion() {
    try {
        const response = await fetch('/api/ingestion');
        const data = await response.json();
        renderIngestion(data);
    } catch (err) {
        console.error('Failed to load ingestion history:', err);
    }
}

function renderIngestion(items) {
    const listEl = document.getElementById('ingestion-list');
    if (!items || items.length === 0) {
        listEl.innerHTML = '<div class="qa-card">No ingestion history found.</div>';
        return;
    }

    listEl.innerHTML = items.map(item => `
        <div class="qa-card">
            <div class="date">${new Date(item.date).toLocaleString()}</div>
            <div class="path"><strong>File:</strong> ${item.target_path}</div>
            ${item.query_filter ? `<div class="filter"><strong>Query:</strong> ${item.query_filter}</div>` : ''}
        </div>
    `).join('');
}

function initGraph() {
    const container = document.getElementById('mynetwork');
    Graph = ForceGraph3D()(container)
        .backgroundColor('#0d0f14')
        .nodeLabel('id')
        .nodeColor(() => '#0055ff')
        .nodeRelSize(6)
        .nodeThreeObjectExtend(true)
        .nodeThreeObject(node => {
            try {
                const sprite = new SpriteText(node.id);
                sprite.color = '#ffffff';
                sprite.textHeight = 4;
                sprite.position.y = -10;
                return sprite;
            } catch (e) {
                console.error("SpriteText error:", e);
                return null;
            }
        })
        .linkColor(link => link.color)
        .linkWidth(1.5)
        .linkDirectionalArrowLength(3.5)
        .linkDirectionalArrowRelPos(1)
        .linkLabel('type');

    loadGraph();
    
    // Auto-resize the graph using ResizeObserver for flex layouts
    new ResizeObserver(entries => {
        for (let entry of entries) {
            const width = entry.contentRect.width;
            const height = entry.contentRect.height;
            if (width > 0 && height > 0) {
                Graph.width(width);
                Graph.height(height);
            }
        }
    }).observe(container);
}

async function loadGraph() {
    try {
        const response = await fetch('/api/graph');
        const data = await response.json();

        if (!data) return;

        const edgeColors = {
            REQUIRES: '#00d2ff',
            IMPLEMENTS: '#00ff88',
            DEPENDS_ON: '#9d50bb',
            OWNS: '#ff9d00',
            REFERENCES: '#ff3366'
        };

        const { nodes: currentNodes, links: currentLinks } = Graph.graphData();
        const existingNodes = new Map(currentNodes.map(n => [n.id, n]));

        const newNodesMap = new Map();
        const newLinks = [];

        data.forEach(edge => {
            if (!newNodesMap.has(edge.from)) {
                newNodesMap.set(edge.from, existingNodes.get(edge.from) || { id: edge.from });
            }
            if (!newNodesMap.has(edge.to)) {
                newNodesMap.set(edge.to, existingNodes.get(edge.to) || { id: edge.to });
            }

            newLinks.push({
                source: edge.from,
                target: edge.to,
                type: edge.type,
                color: edgeColors[edge.type] || '#888888'
            });
        });

        // Avoid continuous simulation resets by checking if the graph size actually changed
        if (currentNodes.length === newNodesMap.size && currentLinks.length === newLinks.length) {
            return; 
        }

        const newNodes = Array.from(newNodesMap.values());

        // Update the graph data
        Graph.graphData({ nodes: newNodes, links: newLinks });

    } catch (err) {
        console.error('Failed to load graph:', err);
    }
}
