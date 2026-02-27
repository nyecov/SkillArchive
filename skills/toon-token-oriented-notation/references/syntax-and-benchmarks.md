# TOON Syntax & Benchmarks

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

## Benchmarks Summary

| Data Type | vs Formatted JSON | vs JSON Compact | vs YAML | vs XML |
|---|---|---|---|---|
| E-commerce (nested, 33% tabular) | **−33.1%** | +5.5% | −14.2% | −40.5% |
| Event logs (semi-uniform, 50% tabular) | **−15.0%** | +19.9% | −0.8% | −25.2% |
| Deep config (0% tabular) | **−31.3%** | +11.9% | −6.2% | −37.4% |
| **Mixed-structure total** | **−21.8%** | +14.9% | −5.6% | −31.0% |

**Key insight:** TOON consistently beats formatted JSON, YAML, and XML. JSON compact (minified) wins on token count but sacrifices readability and LLM accuracy — TOON achieves **74% retrieval accuracy vs JSON's 70%** across 4 models.
