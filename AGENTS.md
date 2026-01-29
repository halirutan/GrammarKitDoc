# Agent Guidelines for Grammar-Kit Documentation Project

This document provides essential information for AI agents working on creating user-facing documentation for Grammar-Kit.

## Project Overview

This project creates comprehensive user documentation for Grammar-Kit, an IntelliJ IDEA plugin that provides BNF Grammars and JFlex file editing support with parser/PSI code generation capabilities. The documentation aims to help language plugin developers effectively use Grammar-Kit.

## Project Structure

### Documentation Sources
- `/Grammar-Kit/` - Source repository (READ-ONLY for feature extraction)
  - `README.md`, `TUTORIAL.md`, `HOWTO.md` - Existing documentation
  - `/resources/messages/attributeDescriptions/` - Attribute documentation
  - `/testData/` - Example grammars and use cases
  - `/grammars/` - BNF and JFlex grammar definitions
- `/info/` - Extracted information for documentation
  - `user-task-map.md` - User tasks and workflows
  - `file-meta.md` - Documentation-relevant files catalog
  - `main-image-description.md` - Visual documentation assets
  - `documentation-outline.md` - Comprehensive documentation structure
- `/.opencode/skills/` - Technical writing guidelines
- `/ai-out/` - Generated documentation output
- `/prompts/` - Documentation generation prompts
- `/docs/` - MkDocs documentation source files

### Key Information Sources

#### Grammar Examples
- `grammars/Grammar.bnf` - BNF self-definition showing all features
- `testData/generator/ExprParser.bnf` - Expression parsing patterns
- `testData/livePreview/Json.bnf` - Real-world JSON grammar

#### Attribute Documentation
All files in `/resources/messages/attributeDescriptions/` contain HTML documentation for each Grammar-Kit attribute (pin, recoverWhile, extends, etc.)

#### User Workflows
- `info/user-task-map.md` - Complete user journey mapping
- Live Preview workflow with shortcuts
- Parser generation and integration steps

## Documentation Writing Guidelines

### Technical Writing Principles
1. **User-Centric**: Focus on tasks users want to accomplish
2. **Progressive Disclosure**: Basic usage first, advanced topics later
3. **Practical Examples**: Working code users can copy and adapt
4. **Clear Structure**: Logical flow from installation to advanced usage

### Documentation Style
- **Voice**: Active, second person ("you can...")
- **Tense**: Present tense for current behavior
- **Code Examples**: Complete, runnable examples with context
- **Terminology**: Define on first use, maintain consistency

### Content Organization
1. **Getting Started** - Installation and first grammar
2. **Core Concepts** - Rules, tokens, attributes
3. **Common Tasks** - Typical user workflows
4. **Advanced Features** - Expression parsing, error recovery
5. **Reference** - Complete attribute/feature documentation
6. **Troubleshooting** - Common issues and solutions

## Documentation Tasks

### Information Extraction
When examining Grammar-Kit source:
- Focus on user-visible features and behaviors
- Extract examples from testData files
- Note keyboard shortcuts and UI actions
- Identify common patterns and best practices

### Content Creation
- Write task-oriented guides ("How to...")
- Create complete, working examples
- Document all attributes with use cases
- Explain error messages and solutions

### Quality Checks
- Verify technical accuracy against source
- Ensure examples are complete and correct
- Check that terminology is consistent
- Validate all keyboard shortcuts

## Important Resources

### User Personas (from user-task-map.md)
1. **IntelliJ Plugin Developer** - Interactive grammar development
2. **Build/CI User** - Gradle-based generation
3. **Grammar Maintainer** - Evolving existing grammars

### Key Features to Document
- BNF grammar syntax and modifiers
- Live Preview with structure view
- Parser/PSI generation
- JFlex lexer integration
- Error recovery mechanisms
- Expression parsing with precedence
- Stub support for indexing

### Common User Questions
- How to start with a new grammar?
- How to debug parsing issues?
- How to handle left recursion?
- How to implement error recovery?
- How to integrate with IntelliJ PSI?

## Documentation Standards

### File Naming
- Use descriptive names: `error-recovery.md`, `expression-parsing.md`
- Group related topics in directories
- Maintain flat structure where possible

### Cross-References
- Link between related topics
- Reference source examples in Grammar-Kit
- Point to IntelliJ Platform SDK where needed

### Code Examples
```bnf
// Always provide context
{
  // Grammar-level attributes
  parserClass="com.example.MyParser"
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
}

// Show complete, working rules
statement ::= assignment | expression
assignment ::= ID '=' expression {pin=2}
```

## MkDocs Documentation System

### Documentation Structure
- **Source Files**: Located in `/docs/` directory
- **Configuration**: `mkdocs.yml` in project root
- **Theme**: Material for MkDocs with professional features
- **Navigation**: Organized by learning progression

### Documentation Outline
The comprehensive documentation structure is defined in `/info/documentation-outline.md` and includes:
1. Getting Started (installation, setup, quick start)
2. Core Concepts (BNF syntax, attributes, Live Preview)
3. Parser Development (grammar design, expressions, error recovery)
4. Code Generation (parser, lexer, PSI customization)
5. IDE Integration (ParserDefinition, language features, testing)
6. Build Integration (Gradle setup, CI/CD)
7. Advanced Topics (external rules, composition, performance)
8. Troubleshooting (common issues, debugging, migration)
9. Reference (complete attribute reference, syntax, shortcuts)
10. Appendices (examples, resources, FAQ)

### Building Documentation
- **Development**: `make serve` (runs local server at http://127.0.0.1:8000)
- **Production**: `make build` (generates static site in `site/`)
- **Dependencies**: Managed via uv (see `pyproject.toml`)
- **Python Version**: 3.12 (specified in `.python-version`)

## Tools and Commands

### Documentation Generation
- **Local Preview**: `make serve` or `uv run mkdocs serve`
- **Build Static Site**: `make build` or `uv run mkdocs build`
- **Deploy to GitHub Pages**: `make deploy`
- **Clean Build**: `make clean`

### Development Setup
1. Install uv package manager
2. Run `make install` to set up dependencies
3. Use `make serve` to preview documentation
4. Edit files in `/docs/` directory

### Source Inspection
- Read files from `/Grammar-Kit/` for feature details
- Extract examples from `/testData/`
- Reference attribute docs from `/resources/messages/`

## Notes

- This is a documentation project - never modify Grammar-Kit source
- Focus on end-user documentation, not implementation details
- Prioritize common use cases over edge cases
- Keep examples practical and applicable