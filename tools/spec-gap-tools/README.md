# spec-gap-tools

Tools for the `spec-mapping` skill — finding unmapped spec files and checking coverage ledger health.

## Scripts

### Find-SpecGaps.ps1

Lists spec files that have no corresponding ledger entry in `.map-spec/`.

```powershell
# Auto-detects spec dir (obsidian/ > spec/ > docs/specs/ > docs/)
.\Find-SpecGaps.ps1

# Custom paths
.\Find-SpecGaps.ps1 -SpecDir ".\docs\specs" -LedgerDir ".\.map-spec"
```

**Exit codes:**
- `0` — all spec files have a ledger entry
- `1` — one or more unmapped spec files found

## Expected Structure

```
<repo-root>/
  obsidian/         (or spec/ or docs/)
    *.md            <- spec source files
  .map-spec/
    <slug>/
      coverage.md
      SPEC-GAPS.md  <- must contain "SPEC-GAPS: <filename>.md"
```
