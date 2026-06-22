## Description
<!-- What does this PR do? Why? -->

## Type of Change
- [ ] Feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Security fix (`security`)
- [ ] Documentation (`docs`)
- [ ] Tests (`test`)
- [ ] Refactor (`refactor`)

## Branch
- [ ] I branched off `dev`, not `main`
- [ ] This PR targets `dev`, not `main`

## Testing
- [ ] `pytest tests/ -v --tb=short` passes
- [ ] New tests added for new functionality

## Clinical Safety (if AI output is touched)
- [ ] All AI output passes through `src/core/safety.py`
- [ ] No diagnostic claims introduced
- [ ] No dose change recommendations introduced
- [ ] Safety disclaimer still appended to all outputs

## Security
- [ ] No secrets or API keys in code
- [ ] No raw SQL introduced
- [ ] `bandit -r src/ -ll` passes with no new high-severity findings
- [ ] Input validation present on any new endpoints

## Related Issues
Closes #
