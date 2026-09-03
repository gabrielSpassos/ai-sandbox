### Subagents

- specialized assistans that claude code delate tasks
- each agents has their own context windows
- when it finished returns a summary to the main thread
    - all the intermediate context usage is not passed to the main one
- help to handle context window usage
- built-in
    - general
    - explore
    - plan
- can create custom subagent
- can attach skills to the subagent

#### Commands

- `/agents`