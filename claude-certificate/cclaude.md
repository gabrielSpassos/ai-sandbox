### Claude.md

- claude code persistent memory about the project
- include on version control (git)
- user can have a project and/or user level CLAUDE.md
- start a project without CLAUDE.md and include on it what the model keeps asking
- Include stack, commands, preferences
- reefer project docs with `@`
    
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