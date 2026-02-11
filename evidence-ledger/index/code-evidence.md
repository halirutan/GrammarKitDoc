# Code Evidence: What is Grammar-Kit?

## Scope Information
This evidence covers section 1.1: What is Grammar-Kit?

## Core Transformation Concept
- Input: BNF grammar files (`.bnf` extension)
- Output: Working Java parser code
- Process: Automatic code generation
- Result: IntelliJ language support

## Primary Use Cases

### Language Support for IntelliJ IDEs
- Build plugins for programming languages
- Examples: Rust, Erlang, Elixir, Dart plugins
- Create syntax highlighting and code completion
- Enable refactoring and navigation

### Domain-Specific Languages (DSLs)
- Custom business rule languages
- Query languages
- Template languages
- Scripting languages

### Configuration File Formats
- JSON parser example: `testData/livePreview/Json.bnf`
- YAML-like formats
- Properties files
- Custom config formats

## Key Development Features

### Live Preview
- Test grammars interactively
- See parsing results instantly
- Debug grammar rules visually
- No compilation needed

### Visual Tools
- Structure view shows grammar organization
- PSI tree visualization
- Grammar diagram generation
- Rule navigation

### Developer-Friendly Actions
- Generate Parser: Creates Java code
- Extract Rule: Refactoring support
- Find Usages: Track rule references
- Quick Documentation: Built-in help

## IntelliJ Platform Integration
- Seamless IDE integration
- Part of IntelliJ Platform since 12.1
- Works with all JetBrains IDEs
- Standard plugin architecture

## Example Locations
- `testData/livePreview/Json.bnf`: Simple JSON parser
- `testData/livePreview/LivePreviewTutorial.bnf`: Beginner tutorial
- `grammars/Grammar.bnf`: BNF language itself
- Plugin examples: Clojure-Kit, intellij-rust

## Out of Scope
Features found but excluded (belong to other sections):
- Installation process → Section 1.2
- BNF syntax details → Section 2.1
- Attribute system → Section 2.2
- Advanced parsing techniques → Section 3.x
- Build integration → Section 6.x