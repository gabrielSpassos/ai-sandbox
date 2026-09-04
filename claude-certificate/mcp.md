### Model Context Protocol (MCP)

- open standard that allows claude code to connect to external tools and data sources
- Claude automatically understand when should use that MCP
- Context cost:
    - MCP adds tools to context even when not using them
    - disable not used MCPs
    - CLI is more efficient than a MCP

#### MCP Servers

##### Types

- HTTP Servers, remote services hosted by the MCP provider, connected over network
- STDIO Servers, local processes that run on local machine

##### Scope

- Local
    - available on current project for you
    - `claude.json`
- User
    - available all yours projects
    - `claude.json`
- Project
    - project available to anyone
    - versioned on checking control (git)
    - `project/.mcp.json`

#### Commands

- `/mcp` -> list, check status, disable
- `claude mcp add` -> add server