# Ship Checklist Template

When verifying production readiness, the agent MUST output the completed checklist using this exact schema to prevent unverified or hazardous ship changes.

```markdown
# Ship Checklist

## 1. Environment & Config
- [ ] Environment variables configured (not hardcoded)
- [ ] HTTPS enabled
- [ ] Rate limiting configured

## 2. Database & State
- [ ] Production database set up with backups

## 3. Observability & Errors
- [ ] Error logging and monitoring in place
- [ ] Health check endpoint exists

## 4. Deployment & Rollback
- [ ] Deployment process documented
- [ ] Rollback plan tested

## Minimum Viable Production (MVP) Status
- [ ] 1. HTTPS
- [ ] 2. Environment variables
- [ ] 3. Error logging
- [ ] 4. Health check
- [ ] 5. Rollback plan

## The Staging Gate
- [ ] Verified in Staging (Dev -> Staging -> Production)
```
