---
name: toon-token-oriented-notation
version: 1.1.0
level: technical
description: >
  Use when serializing structured data for LLM prompts, agent tool outputs, or AI pipeline payloads.
  Handles JSON-to-TOON conversion, format selection (TOON vs JSON vs CSV), tabular schema syntax, and token-cost optimization for uniform datasets.
category: architecture
tags: [toon, token-optimization, data-format, json-alternative, llm-efficiency]
references:
  - name: TOON Official Repository
    url: https://github.com/toon-format/toon
  - name: TOON Format Specification
    url: https://github.com/toon-format/spec/blob/main/SPEC.md
  - name: TOON Documentation Site
    url: https://toonformat.dev
  - name: TOON Explained (freeCodeCamp)
    url: https://www.freecodecamp.org/news/what-is-toon-how-token-oriented-object-notation-could-change-how-ai-sees-data/
  - name: Lean Principles (Muda Eradication)
    path: ../muda/SKILL.md
  - name: VSM (Value Stream Mapping)
    path: ../vsm/SKILL.md
---

# TOON Data Serialization

TOON (Token-Oriented Object Notation) is a compact, schema-aware data serialization format built for LLM contexts. It combines YAML-like indentation with CSV-style tabular arrays to achieve **~40% fewer tokens** than formatted JSON while reaching **74% retrieval accuracy** (vs JSON's 70%) across mixed-structure benchmarks. TOON encodes the same JSON data model — objects, arrays, and primitives — with deterministic, lossless round-trips.

**File extension:** `.toon` · **Media type:** `text/toon` · **Encoding:** UTF-8

## Format Selection: TOON vs JSON vs CSV

Evaluate format by **tabular eligibility** — the percentage of data that fits uniform-array-of-objects shape:

| Tabular Eligibility | Recommended Format | Rationale |
|---|---|---|
| **High (70–100%)** | **TOON** | Maximum token savings; tabular headers declare fields once |
| **Medium (40–60%)** | **JSON** or TOON with caution | Savings diminish; use JSON if pipelines already rely on it |
| **Low (0–30%)** | **JSON compact** | Deeply nested/irregular data; JSON compact often wins on tokens |
| **100% flat, no nesting** | **CSV** | CSV is smaller than TOON for pure flat tables (~5–10% less) |

### When NOT to Use TOON

- **Deeply nested or non-uniform structures** (tabular eligibility ≈ 0%) — JSON compact often uses fewer tokens.
- **Semi-uniform arrays** (~40–60% tabular) — savings diminish; prefer JSON if pipelines already use it.
- **Pure flat tabular data** — CSV is smaller. TOON adds ~5–10% overhead for structure (lengths, field headers).
- **Latency-critical applications** — some local/quantized models (e.g., Ollama) process compact JSON faster despite higher token counts. Benchmark TTFT, tokens/sec, and total time before committing.
- **Non-AI use cases** — JSON remains the standard for REST APIs, config files, and external system interoperability.

**Hybrid approach:** Keep JSON for application-level APIs, convert to TOON at the LLM boundary.

## Technical Reference

For detailed syntax examples, tab-delimiter rules, and benchmark data, refer to:
- **Syntax & Benchmarks**: `./references/syntax-and-benchmarks.md`

## Core Mandates

### 1. Tabular Eligibility Assessment
Before serializing data, assess if it is "Tabular Eligible" (>70% uniform arrays of objects) to ensure maximum token savings.
- **Action:** Use JSON compact if the data is irregular or >2 levels deep; use TOON for uniform tabular sets.
- **Constraint:** NEVER use TOON for non-AI use cases (REST APIs, config files); keep JSON as the standard for interoperability.
- **Integration:** Directly reduces "Transportation" waste as defined in **Lean Principles (Muda)**.

### 2. Tabular Schema Enforcement
Use the `[N]{fields}` header syntax to provide the LLM with a clear schema for tabular arrays.
- **Action:** Encode arrays of objects using the tabular format with clear field headers.
- **Constraint:** Do not omit the `[count]` or `{fields}` headers, as they are critical for LLM retrieval accuracy.
- **Integration:** Acts as a structural **Poka-yoke** for data retrieval.

### 3. Boundary Conversion
Maintain JSON as the internal application standard and convert to TOON only at the LLM prompt/output boundary.
- **Action:** Use library `encode()`/`decode()` or the TOON CLI to handle conversions.
- **Constraint:** NEVER manually author TOON for complex datasets to avoid syntax errors.
- **Integration:** Part of the "Orderly Workspace" (Seiton) in **Lean Foundations**.

## Escalation & Halting

- **Jidoka:** If TOON serialization results in unexpected data loss or parser errors, trigger a Jidoka halt to revert to compact JSON.
- **Hō-Ren-Sō:** Use the Hōkoku (Report) protocol to quantify token savings (via `--stats`) for the user.

## Implementation Workflow

1. **Trigger:** Structured data needs to be serialized for an LLM prompt or tool output.
2. **Execute:** Assess tabular eligibility, choose the format (TOON vs JSON), and perform the conversion.
3. **Verify:** Use `--stats` to confirm token savings and ensure retrieval accuracy is maintained.
4. **Output:** A token-optimized, high-accuracy data payload for the agentic pipeline.

## Integration Points

| Context | Action |
|---------|--------|
| **LLM prompt construction** | Encode data payloads as TOON in ` ```toon ` blocks before inserting into prompt |
| **Agent tool results** | Return TOON from tools when output is tabular |
| **MCP resource content** | Serve TOON with `text/toon` media type for uniform datasets |
| **Fine-tuning data** | Convert training datasets from JSON to TOON to reduce token overhead |
| **Cost monitoring** | Use `--stats` CLI flag to quantify per-file savings |

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **TOON for everything** | Loss of schema validation, broken parsers | Use TOON only at the LLM boundary; keep JSON for APIs |
| **TOON for irregular data** | Messy syntax, no token savings | Check tabular eligibility first; fall back to JSON compact |
| **Manual TOON authoring** | Syntax errors, wasted time | Always use library `encode()` or CLI — TOON is machine-generated |
| **TOON without measurement** | Unknown savings | Use `--stats` to verify savings apply to your data shape |
| **Deep nesting in TOON** | Readability collapse, minimal savings | If nesting exceeds 2 levels, flatten or use JSON compact |
| **Ignoring accuracy** | Optimizing tokens at expense of correctness | Benchmark retrieval accuracy on your task — token savings mean nothing if accuracy drops |
