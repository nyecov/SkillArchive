# Security Checklist Template

When handling auth, user input, secrets, or API endpoints, the agent MUST output the completed security checklist using this exact schema to maintain deterministic safety before modifying the system or shipping code.

```markdown
# Security Checklist & Trust Boundary Audit

## 1. Secrets & Credentials
- [ ] Secrets are in environment variables (not code)
- [ ] NO secrets committed to git or exposed to frontend

## 2. Authentication & Authorization
- [ ] Auth tokens stored securely (e.g., httpOnly cookies, not localStorage)
- [ ] Permissions verified on the SERVER for every protected action
- [ ] User IDs validated against authenticated session (not trusted from client)

## 3. Data Integrity & Exposure
- [ ] User input validated and sanitized (e.g., parameterized queries)
- [ ] API responses filtered to return only necessary fields
- [ ] Error messages do not expose stack traces or internal details

## 4. Required Countermeasures (Poka-yoke)
- **Identified Hazard:** [Describe any unchecked boxes or security risks]
- **Countermeasure Action:** [Describe the Poka-yoke interlock added to prevent it]
```
