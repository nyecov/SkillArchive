# Context Heijunka (Chunker)

This tool implements the **Heijunka (Production Leveling)** and **Swarm Orchestration** principles to prevent LLM context overburden (Muri) when analyzing external repositories.

## Purpose

Instead of feeding an entire cloned repository into an agent's context window, this tool slices the repository into smaller, manageable "Swarm Mission Briefs". Each brief contains a subset of files and explicit instructions for a sub-agent to analyze them. 

This enables:
1. **Parallelization:** Multiple sub-agents can analyze different chunks simultaneously.
2. **Context Stability:** Keeps token usage well below the hallucination threshold.
3. **Muda Elimination:** Prevents the waste of repeating a massive prompt when only a small portion fails.

## Usage

```bash
python tools/context-heijunka/context_chunker.py --source <path_to_cloned_repo> --out <path_to_output_dir> [--max-chars 20000]
```

- `--source`: The directory you want to analyze (e.g., a cloned repository).
- `--out`: The directory where the `mission_brief_XXX.md` files will be saved.
- `--max-chars`: The approximate maximum character count per chunk. Defaults to 20000 (~5000 tokens).

## Agentic Workflow Integration
1. **Clone** the external repository to a temporary directory.
2. **Run** `context_chunker.py` to generate the Mission Briefs.
3. **Delegate** each Mission Brief to an analysis sub-agent using **Swarm Orchestration**.
4. **Synthesize** the resulting Hō-Ren-Sō reports into the final local Skill using **External Synthesis**.
