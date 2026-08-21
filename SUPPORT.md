# Support

## Questions

For usage questions — how to install, invoke `/sdd`, or work through a milestone — see the [user guide](docs/GUIDE.md) first. If it doesn't answer your question:

- Open a **GitHub Discussion** on the repository.
- Ask in the project's community channel linked from the repository.

When asking, include your environment: which AI tool(s) you installed into, your Node and Python versions, and the exact command or trigger you ran. For wizard problems, include the exit code `sdd-setup` reported (`0` all installed, `1` partial, `2` usage/config error).

## Bugs and feature requests

- **Bugs:** open a GitHub issue with a minimal reproduction (what you ran, what you expected, what happened, your Node/Python versions). If the critique engine failed, attach the relevant part of the critique log from `outputs/critique-log/` or the terminal output.
- **Feature requests:** describe the use case and, if possible, the milestone/task it maps to. Because this project is Spec-Driven, substantial features usually start as a spec before code — see [CONTRIBUTING.md](CONTRIBUTING.md) for how a change is structured.

## Contributing

If you want to fix or build something rather than ask, start with [CONTRIBUTING.md](CONTRIBUTING.md). It contains full worked examples for adding a new AI tool adapter and a new critic model.

## Security

For security-sensitive reports, do not open a public issue. See [SECURITY.md](SECURITY.md).

## Status

The project's current version is in [package.json](package.json); `sdd-setup --version` prints it, and [CHANGELOG.md](CHANGELOG.md) records the history. Publishing is automated from the version number — see [CONTRIBUTING.md](CONTRIBUTING.md#releasing).