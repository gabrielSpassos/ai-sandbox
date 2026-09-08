### CLAUDE.md

- claude code persistent memory about the project
- include on version control (git)
- user can have a project and/or user level CLAUDE.md
- start a project without CLAUDE.md and include on it what the model keeps asking
- Include stack, commands, preferences
- reefer project docs with `@`
- check if the rule that you will right belongs to the CLAUDE.md
    - "never push to main" -> this should be pre-tool-use hook 
    - move hard rules to hooks, leave CLAUDE.md with softer conventions
- split big file with path-to-file imports
    ```md
    @.claude/conventions/code-style.md
    @.claude/conventions/testing.md
    @.claude/conventions/workflow.md
    ```
    - The data still is loaded up front, so do NOT reduce the context usage, is just for organization
- be specific and checkable
    - "follow best practices" -> vague
    - "Put new API routes in src/api/handlers, one per file" -> specific
- when you tell Claude don't do something, tell what to do instead
    - "Don't use default exports." -> leaves what to do open
    - "Use named exports, not default exports." -> clarify what should do
- Only emphasis 2/3 things that really hurts when get broken, if everything is "IMPORTANT" or "YOU MUST" than nothing stands out and the emphasis means nothing.

#### Locations for CLAUDE.md
- Managed Policy 
    - org-level file, can't exclude it, so will always play.
- User
    - your personal preferences that will be executed to all the projects
- Project
    - file shared with the team, checked into the repo
- Local
    - ignored by version control (git), personal notes for the repo
    - imagine that you are doing some refactors, this should be only local
    
#### Comands

- `/init` -> creates CLAUDE.md file based on the project

#### Sample

```md
# Project

This is a Next.js 15 app using the App Router, Tailwind, and Drizzle ORM.

# Commands
- Dev server: `pnpm dev`
- Run tests: `pnpm test`
- Lint: `pnpm lint`

# Code Style
- Use 2-space indentation
- Prefer named exports
- All API routes go in app/api/
- Use server actions instead of API routes where possible
```