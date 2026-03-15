document.addEventListener('DOMContentLoaded', () => {
    init();
});

let network = null;
let nodes = new vis.DataSet([]);
let edges = new vis.DataSet([]);

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
        network.fit();
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
    const data = { nodes, edges };
    const options = {
        nodes: {
            shape: 'dot',
            size: 16,
            font: { color: '#ffffff', size: 12, face: 'Inter' },
            borderWidth: 2,
            shadow: true
        },
        edges: {
            width: 2,
            color: { inherit: 'from' },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
            smooth: { type: 'continuous' }
        },
        physics: {
            stabilization: true,
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.3,
                springLength: 95,
                springConstant: 0.04,
                damping: 0.09,
                avoidOverlap: 0.1
            }
        },
        groups: {
            REQUIRES: { color: { background: '#00d2ff', border: '#00aed4' } },
            IMPLEMENTS: { color: { background: '#00ff88', border: '#00cc6a' } },
            DEPENDS_ON: { color: { background: '#9d50bb', border: '#7e3e96' } },
            OWNS: { color: { background: '#ff9d00', border: '#cc7e00' } },
            REFERENCES: { color: { background: '#666666', border: '#444444' } }
        }
    };
    network = new vis.Network(container, data, options);
    loadGraph();
}

async function loadGraph() {
    try {
        const response = await fetch('/api/graph');
        const data = await response.json();

        if (!data) return;

        const currentNodes = nodes.getIds();
        const currentEdges = edges.getIds();
        const newNodeIds = new Set();
        const newEdgeIds = new Set();

        const updates_nodes = [];
        const updates_edges = [];

        data.forEach(edge => {
            const edgeId = `${edge.from}-${edge.to}-${edge.type}`;
            newEdgeIds.add(edgeId);

            if (!nodes.get(edge.from)) {
                updates_nodes.push({ id: edge.from, label: edge.from, group: edge.type });
            }
            newNodeIds.add(edge.from);

            if (!nodes.get(edge.to)) {
                updates_nodes.push({ id: edge.to, label: edge.to });
            }
            newNodeIds.add(edge.to);

            if (!edges.get(edgeId)) {
                updates_edges.push({ id: edgeId, from: edge.from, to: edge.to, label: edge.type });
            }
        });

        // Remove stale nodes/edges
        const nodesToRemove = currentNodes.filter(id => !newNodeIds.has(id));
        const edgesToRemove = currentEdges.filter(id => !newEdgeIds.has(id));

        if (nodesToRemove.length > 0) nodes.remove(nodesToRemove);
        if (edgesToRemove.length > 0) edges.remove(edgesToRemove);

        // Batch updates
        if (updates_nodes.length > 0) nodes.update(updates_nodes);
        if (updates_edges.length > 0) edges.update(updates_edges);

    } catch (err) {
        console.error('Failed to load graph:', err);
    }
}
