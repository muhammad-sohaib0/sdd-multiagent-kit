# Security Policy

## Reporting a vulnerability

Please do **not** open a public issue for security problems. Report them privately by opening a security advisory or emailing the maintainers (see [SUPPORT.md](SUPPORT.md)).

Include, if possible:

- A description of the vulnerability and its impact.
- The affected version and file.
- Steps to reproduce (without exposing sensitive data).
- Any suggested mitigation.

You will receive an acknowledgement; we will work on a fix and coordinated disclosure.

## Scope

The scope is the kit's own components and the content that ships with them. In scope:

- The installer and adapters (`bin/`, `installers/`), especially any handling of API keys.
- The critique engine (`kit/scripts/`) — its network calls, provider requests, and prompt handling.
- The skills content (`kit/skills/`, `kit/SKILL.md`) — a skill that instructs an agent to exfiltrate data, read secrets, or take destructive actions is a security issue.
- The documentation files themselves, including `docs/` — a document that leaks a secret value is a security issue, not just a doc bug.
- Supply-chain tampering — a compromised release artifact, installer, or adapted dependency must be reported privately.

Out of scope:

- General misuse of API keys by the user (the kit only ever stores env-var *names*, never values, in config).
- Third-party provider outages or rate-limiting behavior.
- User errors such as committing their own `.env` despite the `.gitignore` rule.

## Good practices we expect

- Never commit `.env`, `.env.*`, tokens, or keys. `.gitignore` excludes them.
- The setup wizard collects keys in memory only; it never writes them to disk or config files.
- Keep provider keys in your environment, not in repository files.
- If a secret value is found in any committed file — including this documentation — treat it as a security incident: rotate the key, purge it from history, and report it privately.

## Responsible disclosure

We ask for a reasonable window (typically 90 days) before public disclosure so a fix can ship. Coordinated disclosure is preferred; we credit reporters who follow this process.