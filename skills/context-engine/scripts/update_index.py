import os

index_path = r'G:\Skill Archive\.gemini\skills\context-engine\webui\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace main content with 3 columns
main_content = '''
    <main>
        <!-- Column 1: Short-term (Scratchpad) -->
        <section id="scratchpad-panel" class="glass-panel">
            <div class="panel-header">
                <h2>Short-Term: Scratchpad</h2>
            </div>
            <div id="scratchpad-list" class="scroll-area">
                <div class="loader">Loading session findings...</div>
            </div>
        </section>

        <!-- Column 2: Middle-term (Ontology) -->
        <section id="graph-panel" class="glass-panel">
            <div class="panel-header">
                <h2>Middle-Term: Brainmap</h2>
                <button id="reset-view" class="btn-secondary">Reset View</button>
            </div>
            <div id="mynetwork"></div>
        </section>

        <!-- Column 3: Long-term (Ingestion) -->
        <section id="ingestion-panel" class="glass-panel">
            <div class="panel-header">
                <h2>Long-Term: Ingestion History</h2>
            </div>
            <div id="ingestion-list" class="scroll-area">
                <div class="loader">Loading ground-truth context...</div>
            </div>
        </section>
    </main>
'''

import re
content = re.sub(r'<main>.*?</main>', main_content, content, flags=re.DOTALL)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated index.html.')
