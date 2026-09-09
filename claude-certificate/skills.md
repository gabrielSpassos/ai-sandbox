### Skills

- It has to have a name and a description
- instructions, scripts, resources that agents can discover and use
- claude based on the prompt check if should use one of the skill
- load on demand
- location
    - user
        - `~/.claude/skills/$skill-name/SKILL.md`
    - project
        - `.claude/skill/$skill-name/SKILL.md`
- specific tasks
    - commit 
    - pr-review
- `reference.md` for detail material and link it from that skill
    - claude will read only when needed the depth
- Claude execute scripts in the folder, rather than loading it
- Keep the claude skill lean, push the hard material to `reference.md` or a script

### Golden Rule

- `CLAUDE.md` -> Conventions 
- `SKILL.md` -> Procedures, reference material tied to task -> 
- Hooks -> rule that Claude can NOT skip