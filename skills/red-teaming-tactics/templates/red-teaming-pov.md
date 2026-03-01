# Red-Teaming PoV Template

When performing an adversarial stress-test (Red-Teaming), the agent MUST output the results of the bypass attempts using this exact schema to maintain deterministic safety and prove the logic is robust.

```markdown
# Red-Teaming PoV Report

## 1. Attack Surface
- **Crown Jewels:** [The sensitive data or critical action being protected]
- **Target Logic:** [The specific function or endpoint being tested]

## 2. Attack Vectors (The Red Pass)
- **Vector 1:** [Describe the attack, e.g., "Attempt to modify `user_id` in the POST body to target another user's data."]
  - **Result:** [Blocked / Bypassed]
- **Vector 2:** [Describe the attack, e.g., "Attempt to inject `<script>` tags into the description field."]
  - **Result:** [Blocked / Bypassed]

## 3. Proof of Vulnerability (If Bypassed)
- **PoV Reproduction:** [Exact steps, curl command, or script to reproduce the failure]
- **Mitigation Applied:** [The specific code change or Poka-yoke interlock added to block the PoV]

## 4. Final Verification
- [ ] All Attack Vectors are now BLOCKED.
- [ ] PoV reproduction script fails as expected.
```
