# Code Evidence: Introduction to GrammarKit

## Scope Information
This evidence covers section 1.1: Introduction to GrammarKit

## What is GrammarKit

### Overview
- IntelliJ IDEA plugin for language plugin developers
- BNF Grammars and JFlex file editing support
- Parser/PSI code generator
- Readable parser/PSI code generation

### Key Features and Capabilities
- Live Preview: Test grammars
- Structure view: Grammar visualization
- Parser generation: Generate parser/PSI
- JFlex support: Generate and run lexer
- Refactoring: Extract rule, introduce token
- Navigation: Go to related files
- Inspections: Left recursion, unused rules
- Diagram: PSI tree visualization

### Relationship to IntelliJ Platform
- Generates code for IntelliJ language support
- Creates ParserDefinition components
- Produces PSI (Program Structure Interface) classes
- Integrates with IntelliJ Platform SDK
- Included in IntelliJ Platform since 12.1

## When to Use GrammarKit

### Custom Language Plugin Development
- Create parsers for new languages
- Examples: Clojure-Kit, intellij-rust, intellij-erlang
- Examples: intellij-elixir, Perl5-IDEA, Dart
- Generate language support components

### DSL Support
- Domain-specific language parsers
- Custom file format support
- Expression language parsing
- Configuration file parsers

### File Format Parsers
- JSON grammar example: testData/livePreview/Json.bnf
- Custom data format parsing
- Structured text processing

## Prerequisites

### IntelliJ IDEA Basics
- Plugin requires IntelliJ IDEA
- IntelliJ Platform SDK knowledge helpful

### Java Development Knowledge
- Generated code is Java
- External rules require Java methods
- PSI classes extend Java interfaces

### Parsing Concepts
- BNF grammar notation
- PEG (Parsing Expression Grammar) basics
- Token vs rule understanding
- Optional: AST/PSI concepts

## (Very Optional) Grammar Syntax Users Can Write
- Rules: `rule ::= expression`
- Sequences: `rule ::= part1 part2 part3`
- Choices: `rule ::= option1 | option2`
- Optional: `[optional]` or `optional?`
- Repetition: `item*` (zero-or-more), `item+` (one-or-more)
- Predicates: `&required`, `!forbidden`
- Grouping: `(grouped items)`, `{braced items}`

## Example Locations
- `grammars/Grammar.bnf`: Complete BNF self-definition
- `testData/livePreview/Json.bnf`: JSON parser example
- `testData/livePreview/LivePreviewTutorial.bnf`: Tutorial grammar
- `testData/generator/ExprParser.bnf`: Expression parsing

## Out of Scope
Features found but excluded (belong to other sections):
- Installation steps → Section 1.2
- Grammar syntax details → Section 2.1
- Attribute system → Section 2.2
- Parser generation specifics → Section 3.x
- Pin/recoverWhile attributes → Section 2.2
- Expression parsing details → Section 3.2