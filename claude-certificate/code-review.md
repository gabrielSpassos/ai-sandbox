### Code Review

- Review the code produced by claude on a fresh new session without the context from the one that created the code
- Check changes that was not asked
- Tests getting worse
- New packages/dependencies
- Hardcoded values

#### Commands

- `/code-review`
- `/diff` -> opens way to see the changes
- `/rewind`

- both `/diff` and `/code-review` read git's record of what changed
- `/code-review low` reports only the findings it's most confident about
- `/code-review high` casts a wider net and may include findings it's less sure of. 
- This code review level is reused on future uses