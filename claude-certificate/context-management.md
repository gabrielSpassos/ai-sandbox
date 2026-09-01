### Context Management 

- context window, "memory"
- use `CLAUDE.md` to store general things that should be remembered in multiple sessions
- be explicit and specific
- turn-off MCPs that are not related to the session
- skills will not use the context window if not used
- subagents run in parallel with independent context window

#### Commands

- `/context` -> see the context window
- `/compact` -> sumarize, reduce the corrent context, might loose details also trigger automatically
- `/clear` -> wipe-out all the context 
- Use `compact` when will continue on the same context/feature and `clear` if will start a new one