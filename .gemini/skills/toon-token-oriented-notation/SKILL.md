---
name: toon-token-oriented-notation
version: 1.1.0
description: >
  Use when serializing structured data for LLM prompts, agent tool outputs, or AI pipeline payloads.
  Handles JSON-to-TOON conversion, format selection (TOON vs JSON vs CSV), tabular schema syntax, and token-cost optimization for uniform datasets.
category: data-serialization
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
    path: ../lean-principles-muda/SKILL.md
  - name: VSM (Value Stream Mapping)
    path: ../vsm-value-stream-mapping/SKILL.md
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

## TOON Syntax Reference

### Simple Object (key-value pairs)

```toon
name: Alice
age: 30
city: Bengaluru
```

Equivalent JSON: `{"name": "Alice", "age": 30, "city": "Bengaluru"}`

### Array of Values

```toon
colors[3]: red,green,blue
```

Syntax: `fieldName[count]: value1,value2,...`

### Array of Objects (tabular — the primary TOON strength)

```toon
users[2]{id,name,role}:
1,Alice,admin
2,Bob,user
```

Syntax: `fieldName[count]{field1,field2,...}:` followed by one data row per line. The `[N]` length and `{fields}` header give the LLM a clear schema to follow, improving parsing reliability.

### Nested Objects (indentation-based)

```toon
user:
  id: 1
  name: Alice
  profile:
    age: 30
    city: Bengaluru
```

### Array of Objects With Nested Fields

```toon
teams[1]:
- name: Team Alpha
  members[2]{id,name}:
  1,Alice
  2,Bob
```

### Tab Delimiters (extra efficiency)

Use tab characters instead of commas for even fewer tokens in tabular arrays. The delimiter is auto-detected by the parser.

## Conversion Workflow

### Decision Gate

Before serializing data for an LLM:

1. **Assess tabular eligibility.** What percentage of your data is uniform arrays of objects? If >70% → **Use TOON**.
2. **Check nesting depth.** 3+ levels deep with irregular shapes? → **Keep JSON compact**.
3. **Check consumer.** Going to an LLM prompt or agent tool output? → **TOON**. REST API or config file? → **JSON**.
4. **Measure.** Use `npx @toon-format/cli data.json --stats` to compare token counts before committing.

### CLI (No Installation Required)

```bash
# JSON → TOON
npx @toon-format/cli input.json -o output.toon

# TOON → JSON
npx @toon-format/cli data.toon -o output.json

# Pipe from stdin
cat data.json | npx @toon-format/cli

# Show token savings
npx @toon-format/cli data.json --stats
```

### JavaScript / TypeScript

```bash
npm install @toon-format/toon
```

```javascript
import { encode, decode } from "@toon-format/toon";

// JSON → TOON
const toonString = encode({ users: [{ id: 1, name: "Alice" }] });

// TOON → JSON
const jsonObject = decode(toonString);
```

### Python

```bash
pip install python-toon
```

```python
from toon import encode, decode

# JSON → TOON
toon_output = encode({"name": "Alice", "age": 30})

# TOON → JSON
json_output = decode("name: Alice\nage: 30")
```

### Other Languages

Official and community implementations available for **Go, Rust, Java, Swift, .NET**, and more. See the [full list](https://toonformat.dev/ecosystem/implementations).

## Using TOON With LLMs

TOON works best when you **show** the format instead of describing it. The structure is self-documenting — models parse it naturally once they see the pattern.

**Rules:**
1. Wrap TOON data in ` ```toon ` code blocks when embedding in prompts.
2. Show the expected header template when asking models to **generate** TOON output.
3. Use tab delimiters for maximum token efficiency in large datasets.
4. For validation strategies, see the [LLM integration guide](https://toonformat.dev/guide/llm-prompts).

## Benchmarks Summary

| Data Type | vs Formatted JSON | vs JSON Compact | vs YAML | vs XML |
|---|---|---|---|---|
| E-commerce (nested, 33% tabular) | **−33.1%** | +5.5% | −14.2% | −40.5% |
| Event logs (semi-uniform, 50% tabular) | **−15.0%** | +19.9% | −0.8% | −25.2% |
| Deep config (0% tabular) | **−31.3%** | +11.9% | −6.2% | −37.4% |
| **Mixed-structure total** | **−21.8%** | +14.9% | −5.6% | −31.0% |

**Key insight:** TOON consistently beats formatted JSON, YAML, and XML. JSON compact (minified) wins on token count but sacrifices readability and LLM accuracy — TOON achieves **74% retrieval accuracy vs JSON's 70%** across 4 models.

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
