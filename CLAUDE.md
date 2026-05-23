# CLAUDE.md

This file documents the repository for AI assistants (Claude Code and similar tools). Update it as the project evolves.

## Repository Status

This repository is freshly initialized. The only file currently tracked is `.gitkeep`. No source code, dependencies, build system, or tests exist yet.

**Owner:** mirai2x  
**Remote:** mirai2x/test  
**Default branch:** `main`

---

## Git Workflow

### Branch Strategy

- `main` — stable, production-ready state
- Feature branches use the pattern `claude/<description>-<id>` for AI-driven changes
- Create feature branches off `main`; open a PR to merge back

### Commit Conventions

- Write concise, imperative commit messages (e.g. "Add login endpoint", not "Added login endpoint")
- Focus the message on *why*, not *what* — the diff already shows what changed
- One logical change per commit; avoid bundling unrelated fixes

### Push Protocol

```bash
git push -u origin <branch-name>
```

Retry up to 4 times on network failure with exponential backoff (2s → 4s → 8s → 16s).

---

## Development Conventions (to be updated when code is added)

Until source code exists, these are the intended defaults:

### Code Style

- Follow the conventions of whatever language/framework is introduced
- Prefer explicit over implicit; avoid magic where a clear alternative exists
- No unnecessary comments — only document the non-obvious *why*, not the *what*
- No emojis in code or commit messages

### Testing

- Write tests for new behaviour before or alongside the implementation
- Do not commit code that breaks existing tests

### Security

- Never commit secrets, credentials, or `.env` files
- Validate all external input at system boundaries; trust internal code
- Follow OWASP Top 10 guidance when writing web-facing code

---

## Working with AI Assistants

- This file is the primary source of truth for repo conventions; keep it current
- When adding a new language, framework, or tool, update the relevant section here
- Prefer editing existing files over creating new ones
- Do not add abstractions, refactors, or cleanup beyond what a task requires
- Do not create intermediate planning documents — work from conversation context

---

## Updating This File

When the project gains a codebase, replace the placeholder sections above with accurate information covering:

- Project purpose and architecture overview
- Directory structure and what lives where
- How to install dependencies and run the project locally
- How to run tests and linters
- Any environment variables required (`cp .env.example .env`)
- Deployment process
