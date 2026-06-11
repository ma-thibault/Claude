# Two-Agent Harness (Worker + Supervisor)

A minimal example of running a Claude agent **fully unattended** by replacing
human approval with a second model call.

## How it works

- `supervisor_worker.py` starts a "worker" session via the
  [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)
  (`query()` with `permission_mode="default"`).
- Whenever the worker wants to use a tool (`Read`, `Edit`, `Bash`, ...), the
  SDK calls `supervisor_decide()` instead of prompting a human.
- `supervisor_decide()` sends the tool name + input to a separate "supervisor"
  model call, which replies `ALLOW` or `DENY <reason>`. That decision is
  returned to the worker as `PermissionResultAllow` / `PermissionResultDeny`.

This is the same idea as the `autonomous-worker` subagent
(`.claude/agents/autonomous-worker.md`, which uses
`permissionMode: bypassPermissions`), but here a model actively reviews each
action instead of approving everything unconditionally.

## Setup

```bash
cd agent-harness
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in ANTHROPIC_API_KEY
export $(cat .env | xargs)
```

## Run

```bash
python supervisor_worker.py "Add a hello-world script and run it"
```

Each tool call the worker makes will print a line like:

```
[supervisor] Bash -> ALLOW
[supervisor] Bash -> DENY this command force-pushes to a remote branch
```

## Customizing

- **Supervisor policy**: edit `SUPERVISOR_SYSTEM_PROMPT` in
  `supervisor_worker.py` to change what gets approved/denied.
- **Supervisor model**: set `SUPERVISOR_MODEL` in `.env` (defaults to
  `claude-sonnet-4-6`). It can be cheaper/faster than the worker model since
  its job is just allow/deny.
- **Worker config**: `ClaudeAgentOptions` in `run_worker()` accepts the usual
  fields — `model`, `system_prompt`, `allowed_tools`, `max_turns`, etc.

## Caveats

- `can_use_tool` requires the prompt to be passed as an async iterable
  (streaming mode) — see `prompt_stream()`. A plain string prompt raises a
  `ValueError` when `can_use_tool` is set.
- The supervisor is itself an LLM and can be wrong — treat this as a starting
  point for experimentation, not a security boundary. Run it in an isolated
  environment (container/VM), same as `autonomous-worker`.
