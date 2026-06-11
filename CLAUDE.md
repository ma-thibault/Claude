# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and other AI assistants when working with code in this repository.

## Project Status

This repository is currently empty/new. This file is a starter template — update it as the codebase grows so it stays an accurate guide for future work.

## Project Overview

_TODO: Describe what this project is, its purpose, and who it's for._

## Tech Stack

_TODO: List the primary language(s), frameworks, runtime, and major dependencies once chosen._

## Repository Structure

_TODO: Once the project is scaffolded, document the top-level layout, e.g.:_
```
/src        - application source code
/tests      - automated tests
/docs       - additional documentation
```

## Development Setup

_TODO: Document how to install dependencies and run the project locally (e.g. package manager, environment variables, required tools)._

## Common Commands

_TODO: List the commands used during development, for example:_
- Install dependencies: `_command_`
- Run the dev server: `_command_`
- Run tests: `_command_`
- Run a single test: `_command_`
- Lint / format: `_command_`
- Build for production: `_command_`

## Development Workflow

- Work happens on feature branches; avoid committing directly to `main`.
- Write clear, descriptive commit messages explaining *why* a change was made.
- Keep pull requests focused and reasonably small.
- Run tests and linters before committing.

## Code Conventions

_TODO: Document naming conventions, formatting rules, file organization patterns, and any architectural principles specific to this project._

## Testing

_TODO: Describe the testing strategy (unit, integration, e2e), where tests live, and how to run them._

## Custom Subagents

This repo includes example Claude Code subagents in `.claude/agents/`:

- **code-reviewer** — read-only review of diffs for bugs, security issues, and style (`Read, Grep, Glob, Bash`).
- **debugger** — reproduces failures, root-causes them, and applies a fix (`Read, Edit, Bash, Grep, Glob`).
- **docs-sync** — keeps this CLAUDE.md and other docs in sync with the codebase (`Read, Edit, Glob, Grep, Bash`, `model: haiku`).

Manage subagents with the `/agents` command (create, edit, delete, change tools/model). Invoke one explicitly with `@agent-name`, or let Claude delegate automatically based on each agent's `description`. Project-level agents live in `.claude/agents/*.md` (shared via git); personal ones go in `~/.claude/agents/`.

## Notes for AI Assistants

- Prefer editing existing files over creating new ones.
- Match existing code style and conventions once established.
- Keep changes minimal and focused on the task at hand; avoid unrelated refactors.
- Update this CLAUDE.md as the project evolves so it remains a reliable reference.
