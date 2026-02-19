# Grammar-Kit Documentation

User documentation for [Grammar-Kit](https://github.com/JetBrains/Grammar-Kit), the JetBrains IntelliJ IDEA plugin for BNF grammar editing and parser/PSI code generation. The published site is at [grammarkit.github.io/documentation](https://grammarkit.github.io/documentation/).

The documentation covers grammar development and BNF syntax, expression parsing and error recovery, parser and PSI code generation, IDE and Gradle integration, and advanced topics like performance tuning and debugging. It is built with [MkDocs](https://www.mkdocs.org/) and the Material theme.

## How it works

This project treats the Grammar-Kit source code as the single source of truth. Instead of writing documentation by hand, it uses a pipeline of specialized AI agents that extract facts from the source, validate them, and transform them into user-facing documentation. The process runs in two phases: evidence collection and documentation creation.

### Evidence collection

Three "evidence writer" agents read the Grammar-Kit source repository and produce structured files in the `evidence-ledger/` directory:

1. A code analyst (`code-analyst`) reads the source and extracts user-facing facts: grammar syntax, configurable attributes, IDE actions, keyboard shortcuts, and observable behavior. It writes `code-evidence.md` for each topic.
2. An example generator (`example-generator`) reads the code evidence and the test data in the Grammar-Kit repo, then creates minimal working examples. It writes `examples.md` for each topic.
3. A reference checker (`reference-checker`) validates file paths, cross-references, and external links against the actual source. It writes `references.md` for each topic.

### Documentation creation

Three "evidence reader" agents work only from the evidence ledger. They cannot access Grammar-Kit source directly:

1. A topic architect (`topic-architect`) designs the content structure for each page based on the evidence and the documentation outline in `info/`. It writes `topic-summary.md`.
2. A drafter (`drafter`) transforms the evidence into prose documentation following the topic summary. It writes the actual `docs/*.md` files.
3. A copyeditor (`copyeditor`) polishes the draft for clarity, consistency, and technical accuracy, using the evidence as the source of truth.

### Configuration and inputs

The agent definitions live in `.opencode/agent/`. Each file defines one agent's role, access permissions, and output format. A primary orchestrator agent (`techdocs.md`) coordinates the pipeline and delegates to the six subagents.

The `info/` directory contains the planning inputs that seed the pipeline:

- `documentation-outline.md` defines the full documentation structure and section scope
- `user-task-map.md` maps user personas and workflows to documentation topics
- `file-meta.md` catalogs which Grammar-Kit source files are relevant to documentation

A style guide in `.opencode/skills/human-style.md` enforces consistent writing across all agents.

### The evidence ledger

The `evidence-ledger/` directory sits between source code and final documentation. Each topic gets a subdirectory with four files: `code-evidence.md`, `examples.md`, `references.md`, and `topic-summary.md`. A metadata file at `evidence-ledger/metadata/evidence-index.json` tracks which topics have complete evidence and whether the documentation is in sync.

This separation means the documentation can be regenerated from evidence without re-analyzing the source, and evidence can be updated independently when the source changes.

## Contributing

Run `make install` to install dependencies, then `make serve` to start a local preview server at http://127.0.0.1:8000. See [DEVELOPMENT.md](DEVELOPMENT.md) for the full development workflow, project structure, and available commands.

## License

This documentation is licensed under the Apache 2.0 License.
