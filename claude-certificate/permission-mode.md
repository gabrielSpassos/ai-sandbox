### Permission Modes

- **Manual** reads only, without prompting. Everything else asks first.
- **Accept** edits runs reads, file edits, and common file system bash commands without asking. This is for iterating on code that you review after the fact.
- **Plan** reads only. It researches and proposes changes without editing anything.
- **Auto accepts** everything, with a separate classifier model reviewing each action before it runs.
- **Don't ask** allows only pre-approved tools. Everything else is auto-denied with no prompt.
- **Bypass permissions** skips all checks. This is the equivalent of the **dangerously-skip-permissions** flag. Only run it inside an isolated container or virtual machine.

- Switch modes using shift + tab
    - manual, accept edits, plan, and auto

#### How Auto-Mode Works

- Hands-Off mode
- before each action executes, a separate classifier model reviews it
- Blocking:
    - production deploys and migrations
    - force push
    - piping downloaded code straight into a shell
    - send sensitve data to external endpoints
    - Destroying files that exist for the session