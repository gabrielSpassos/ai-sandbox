### Hooks

- Allow to run commands on different points of Claude Code life cycle
- Are deterministic, will always run
- Configured at the `settings.json`

#### Types

- SessionStart -> fires at the start and primes the environment.
  - Use the startup source if you only want it on fresh starts.
  - to re-inject context after compaction, don't use PostCompact. Use SessionStart with the compact matcher. That's the one that actually gets its output back into the conversation.

- UserPromptSubmit -> when user submit a prompt and before claude process it

- PreToolUse -> runs before a tool call
  - It's the one that can stop something before it happens.

- PostToolUse -> runs after a tool call completes
  - usually where auto-formatting or an auto-lint goes.

- Notification ->  runs when claude sends a notification

- Stop -> runs when Claude wants to end its turn.
  - could refuse if some condition is not met yet

- SubagentStop -> same as Stop, but for subagent

- PreCompact -> fire before session compaction.

- PostCompact -> fire after session compaction.

- InstructionsLoaded -> fires when a CLAUDE.md or rule file loads
  - Handy for auditing what actually made it into context.

#### Sample

```
<your-project-root>/.claude/settings.json
```

`settings.json`

```json
{
  "hooks": [
    {
      "type": "PostToolUse",
      "matcher": "Edit|MultiEdit|Write",
      "command": "npx prettier --write \"$CLAUDE_CHANGED_FILES\""
    }
  ]
}


```

#### PreToolUse returns

- JSON
  - allow -> let the call through
  - deny -> stop the call
  - ask -> hand it back and ask user
  - defer -> pauses the tool and resume it later 
    - (only applicable for non-interactive -p runs)
    
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "...",
    "updatedInput": {
      "command": "..."
    }
  }
}
```

- No JSON
  - 0 -> success
    - plain text is ignored except at: `SessionStart`, `UserPromptSubmit`, `UserPromptExpansion`, text is added in context, makes the state-preserver hook work.
  - 2 -> error blocking
    - gets error as feedback to claude context
  - 1, or anything else -> error non blocking
