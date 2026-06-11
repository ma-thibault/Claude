"""Two-agent harness: a worker Claude agent runs a task while a separate
supervisor model call approves or denies each tool request, so the worker
never blocks waiting on a human.

Usage:
    python supervisor_worker.py "<task description>"
"""

import asyncio
import os
import sys

from anthropic import Anthropic
from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import (
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

SUPERVISOR_MODEL = os.environ.get("SUPERVISOR_MODEL", "claude-sonnet-4-6")

SUPERVISOR_SYSTEM_PROMPT = """You are a supervisor approving or denying tool calls \
made by a worker coding agent so it can run unattended.

Approve routine read/edit/test/build actions scoped to the project directory.
Deny anything destructive or irreversible (force-push, rm -rf, dropping data, \
credential access, network calls to unfamiliar hosts) or anything outside the \
project directory.

Reply with exactly one line: either "ALLOW" or "DENY <short reason>"."""

_anthropic = Anthropic()  # reads ANTHROPIC_API_KEY from the environment


async def supervisor_decide(
    tool_name: str, tool_input: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Ask the supervisor model whether to allow this tool call."""
    response = _anthropic.messages.create(
        model=SUPERVISOR_MODEL,
        max_tokens=50,
        system=SUPERVISOR_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Tool: {tool_name}\nInput: {tool_input}"}
        ],
    )
    decision = response.content[0].text.strip()
    print(f"[supervisor] {tool_name} -> {decision}")

    if decision.upper().startswith("ALLOW"):
        return PermissionResultAllow(updated_input=tool_input)

    reason = decision.split(" ", 1)[1] if " " in decision else "denied by supervisor"
    return PermissionResultDeny(message=reason)


async def prompt_stream(task: str):
    # can_use_tool requires the prompt to be an async iterable (streaming mode).
    yield {"type": "user", "message": {"role": "user", "content": task}}


async def run_worker(task: str) -> None:
    options = ClaudeAgentOptions(
        can_use_tool=supervisor_decide,
        permission_mode="default",
        cwd=os.getcwd(),
    )
    async for message in query(prompt=prompt_stream(task), options=options):
        print(message)


if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) or (
        "List the files in the current directory and summarize the project."
    )
    asyncio.run(run_worker(task))
