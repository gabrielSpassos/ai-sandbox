### Workflow

#### Explore Plan
- Explore code base with read-only way
- Define clear what is the success criteria

#### Code
- Implement/Approve the plan to actually do the code
- Can use tools (such as a claude code chrome extention)
- Use a test suite to validate the changes

#### Commit and Push
- Run code reviewer **subagent**
    - subagent will not have the main context bias

#### Handle long sessions

- scope the work before claude starts
    - use plan mode to read-only analysis
    - review the plan
    - ask claude to update the plan
    - iterate on the plan

- steer Claude into the right direction
    - `/compact` with description on what to focus to summarize
        - e.g: `/compact Focus on the --version flag implementation`
    - `/rewind` to restore to the last checkpoint if claude did something wrong
        - Restore code and conversation - roll back both together.
        - Restore conversation - roll back just the chat.
        - Restore code - roll back just the files.
        - Summarize from here - summarizes everything after the checkpoint. Great if you had a side conversation and wnt free up some space.
        - Summarize up to here - summarizes everything before the checkpoint. Great when you had a long setup phase you want to compress, but you want to keep the implementation parts intact.

- let claude run autonomously 
    - `/goal` set a completion conditions, what done looks like, evaluator will work until confirms the conditions are met. 
        - conditions must be checkable from claude outputs, like tests results
    - `/loop` runs a prompt on interval, can act when the state changes

- run parallel with `worktrees`
    - helps to 2+ claude sessions conflicts on files
    - independent files trees
    - `.worktreeinclude` -> ignore files (.env/configs) to not include on version control