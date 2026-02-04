# Agent Guidelines for Grammar-Kit Documentation Project

This document provides essential information for AI agents working on the Grammar-Kit documentation project.

## Project Overview

This project creates comprehensive user documentation for Grammar-Kit, an IntelliJ IDEA plugin that provides BNF Grammars and JFlex file editing support with parser/PSI code generation capabilities.

## Project Structure

### Core Directories

- `/Grammar-Kit/` - Source repository (READ-ONLY)
  - `README.md`, `TUTORIAL.md`, `HOWTO.md` - Existing documentation
  - `/resources/messages/attributeDescriptions/` - Attribute documentation
  - `/testData/` - Example grammars and use cases
  - `/grammars/` - BNF and JFlex grammar definitions

- `/evidence-ledger/` - Evidence-based documentation system
  - `{topic-path}/code-evidence.md` - Technical evidence from source
  - `{topic-path}/examples.md` - Code examples and snippets
  - `{topic-path}/references.md` - Links and external references
  - `{topic-path}/topic-summary.md` - Writing guidance for topic
  - `metadata/evidence-index.json` - Evidence tracking

- `/docs/` - MkDocs documentation source files
  - `index.md` - Landing page
  - `getting-started/` - Introduction, installation, quick start
  - Additional sections per documentation outline

- `/info/` - Project information
  - `documentation-outline.md` - Complete documentation structure
  - `user-task-map.md` - User personas and workflows
  - `file-meta.md` - Documentation-relevant files catalog

- `/.opencode/skills/` - Writing guidelines
  - `human-style.md` - Technical writing style guide

## Documentation Workflow

### Evidence-Based Process

1. **Evidence Collection** (code-analyst)
   - Extract technical details from Grammar-Kit source
   - Document features, APIs, and behaviors
   - Create code examples from testData

2. **Topic Architecture** (topic-architect)
   - Create topic summaries based on evidence
   - Structure content for clarity
   - Map evidence to documentation sections

3. **Content Creation** (drafter)
   - Write user-facing documentation
   - Follow topic summaries and evidence
   - Apply human-style guidelines

4. **Quality Assurance** (copyeditor)
   - Ensure technical accuracy
   - Apply style guidelines
   - Improve clarity and flow

### Writing Standards

#### Style Guidelines (from human-style.md)
- Write like a calm teammate: clear, direct, respectful
- Use active voice and present tense
- Avoid humor, pep talks, and motivational content
- Limit paragraphs to 5 sentences
- Use lists only when they improve scanning
- Group related content under fewer headings

#### Grammar-Kit Specific
- Always write "Grammar-Kit" with a dash
- Define technical terms on first use
- Include complete, runnable code examples
- Focus on practical, task-oriented content

## Key Information Sources

### Grammar Examples
- `grammars/Grammar.bnf` - BNF self-definition
- `testData/generator/ExprParser.bnf` - Expression parsing
- `testData/livePreview/Json.bnf` - JSON grammar example

### User Personas
1. **IntelliJ Plugin Developer** - Creating language support
2. **Build/CI User** - Gradle-based parser generation
3. **Grammar Maintainer** - Evolving existing grammars

### Common User Tasks
- Creating a new grammar
- Debugging parsing issues
- Implementing error recovery
- Integrating with IntelliJ PSI
- Setting up build automation

## MkDocs Documentation

### Configuration
- **Config**: `mkdocs.yml` in project root
- **Theme**: Material for MkDocs
- **Python**: 3.12 (via uv package manager)

### Commands
- `make serve` - Local preview at http://127.0.0.1:8000
- `make build` - Build static site
- `make deploy` - Deploy to GitHub Pages
- `make clean` - Clean build artifacts

### Documentation Sections
1. Getting Started
2. Core Concepts
3. Parser Development
4. Code Generation
5. IDE Integration
6. Build Integration
7. Advanced Topics
8. Troubleshooting
9. Reference
10. Appendices

## Agent-Specific Guidelines

### For code-analyst
- Focus on user-visible features
- Extract practical examples
- Document keyboard shortcuts
- Note common patterns

### For topic-architect
- Create beginner-friendly outlines
- Map evidence to sections
- Structure for progressive learning
- Identify prerequisites

### For drafter
- Write task-oriented content
- Use evidence as source of truth
- Apply human-style guidelines
- Include practical examples

### For copyeditor
- Verify technical accuracy
- Ensure style consistency
- Improve clarity without changing meaning
- Check "Grammar-Kit" spelling

## Important Notes

- Never modify Grammar-Kit source files
- Focus on end-user documentation
- Prioritize common use cases
- Keep examples practical and complete
- Always use evidence-based approach for accuracy