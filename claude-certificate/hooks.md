### Hooks

- Allow to run commands on different points of Claude Code life cycle
- Are deterministic, will always run
- Configured at the `settings.json`

#### Types

- UserPromptSubmit -> when user submit a prompt and before claude process it
- PreToolUse -> runs before a tool call
- PostToolUse -> runs after a tool call completes
- Notification ->  runs when claude sends a notification
- Stop -> runs when claude finishes responding