# Introduction to Grammar-Kit

Grammar-Kit is an IntelliJ IDEA plugin that generates language support from grammar descriptions. When you need IntelliJ IDEA to understand a custom file format or programming language, Grammar-Kit transforms your grammar rules into a working parser and all the necessary integration code.

## What Grammar-Kit Does

Grammar-Kit solves a specific problem: teaching IntelliJ IDEA to understand new languages. Without it, implementing language support requires writing thousands of lines of parser code, PSI (Program Structure Interface) classes, and IDE integration logic. Grammar-Kit automates this process. You write grammar rules in BNF notation, and Grammar-Kit generates:

- A recursive descent parser that reads your language
- PSI classes representing your language's structure  
- Integration points for syntax highlighting, code completion, and navigation
- Error recovery mechanisms for robust parsing

The generated code integrates directly with IntelliJ's language support framework, giving your custom language the same capabilities as built-in languages.

## Core Features

Grammar-Kit provides a complete environment for grammar development:

**Live Preview** (Ctrl+Alt+P / Cmd+Alt+P): Test your grammar against sample text in real-time. The preview shows how your rules parse input and highlights any parsing errors immediately.

**Structure View** (Ctrl+F12 / Cmd+F12): Navigate your grammar with a hierarchical view of all rules. The structure popup makes it easy to jump between rules in large grammars.

**Parser Generation** (Ctrl+Shift+G / Cmd+Shift+G): Generate complete parser code with one command. Grammar-Kit produces readable Java code that implements your grammar rules as recursive descent methods.

**Built-in Analysis**: Grammar-Kit detects common grammar problems before generation. It identifies left recursion, unused rules, and ambiguous patterns that could cause parsing issues.

Additional capabilities include refactoring support (extract rule, introduce token), navigation to generated files, JFlex lexer integration, and PSI tree visualization.

## Grammar Basics

Grammar-Kit uses BNF (Backus-Naur Form) notation to describe language rules. A simple rule looks like this:

```bnf
greeting ::= 'hello' 'world'
```

The `::=` symbol means "is defined as". This rule matches the exact text "hello world". A more practical example:

```bnf
assignment ::= ID '=' NUMBER
```

This rule matches assignments like `age = 25` or `score = 100`. ID and NUMBER are tokens defined by your lexer.

Grammar-Kit extends standard BNF with additional operators:

```bnf
rule ::= required_part optional_part?        // ? means optional
list ::= item (',' item)*                    // * means zero or more
sequence ::= element+                        // + means one or more
choice ::= option1 | option2 | option3       // | means choice
```

These patterns cover most language constructs you'll need to parse.

## When to Use Grammar-Kit

Grammar-Kit is the standard tool for creating IntelliJ language plugins. Use it when you need to:

**Create Custom Language Plugins**: Grammar-Kit powers many production language plugins including [Clojure-Kit](https://github.com/gregsh/Clojure-Kit), [intellij-rust](https://github.com/intellij-rust/intellij-rust), [intellij-erlang](https://github.com/ignatov/intellij-erlang), [intellij-elixir](https://github.com/KronicDeth/intellij-elixir), [Perl5-IDEA](https://github.com/Camelcade/Perl5-IDEA), and [Dart](https://github.com/JetBrains/intellij-plugins/tree/master/Dart).

**Support Domain-Specific Languages**: Parse mathematical expressions, query languages, configuration languages, or any custom DSL. Grammar-Kit handles operator precedence, nested expressions, and complex language constructs.

**Parse Structured File Formats**: Create parsers for configuration files, data formats, or any text-based format with defined rules. Grammar-Kit generates type-safe AST classes that make file processing straightforward.

Example DSL for expressions:

```bnf
expr ::= term ('+' term)*
term ::= factor ('*' factor)*
factor ::= NUMBER | '(' expr ')'
```

This grammar correctly handles operator precedence and parentheses in expressions like `2 + 3 * 4` or `(2 + 3) * 4`.

## Prerequisites

To use Grammar-Kit effectively, you need:

**IntelliJ IDEA**: Grammar-Kit is an IntelliJ IDEA plugin. You should know how to install plugins, create projects, and navigate the IDE.

**Java Knowledge**: Grammar-Kit generates Java code. You need to read Java code, understand basic object-oriented concepts, and work with Java project structure. Since version 2022.3, Grammar-Kit requires Java 17 or higher.

**Parsing Concepts (helpful but not required)**: Understanding of BNF notation, tokens versus rules, and basic parsing concepts helps but isn't mandatory. Grammar-Kit's Live Preview and examples make these concepts concrete as you work.

## Complete Example

Here's a grammar for a simple configuration language:

```bnf
config ::= section*
section ::= '[' ID ']' property*
property ::= ID '=' value
value ::= STRING | NUMBER | BOOLEAN
```

This grammar parses configuration files like:

```
[database]
host = "localhost"
port = 5432
enabled = true

[cache]
size = 1000
timeout = 60
```

Grammar-Kit generates a complete parser from these four rules, including error recovery, PSI classes for each rule, and visitor interfaces for traversing the parse tree.

## Integration with IntelliJ Platform

Grammar-Kit has been included in the IntelliJ Platform since version 12.1, making it the standard tool for language plugin development. The generated code integrates seamlessly with IntelliJ's language support framework, providing:

- ParserDefinition implementation
- PSI element classes with proper hierarchy
- Stub support for indexing
- Error recovery mechanisms
- Integration points for highlighting, completion, and refactoring

## Next Steps

To start using Grammar-Kit: [Install the plugin](installation.md), then follow the [Quick Start Tutorial](quick-start.md) to create your first grammar.

For deeper understanding, see [BNF Syntax](../core-concepts/bnf-syntax.md) and [Grammar Attributes](../core-concepts/attributes.md).

## Additional Resources

- [Grammar-Kit Plugin Page](http://plugins.jetbrains.com/plugin/6606)
- [IntelliJ Platform SDK Documentation](https://plugins.jetbrains.com/docs/intellij/welcome.html)
- Example grammars: `testData/livePreview/Json.bnf`, `testData/generator/ExprParser.bnf`

## Editorial Notes

- Missing from docs: The evidence mentions `testData/livePreview/LivePreviewTutorial.bnf` as an example grammar, but it was removed during editing to streamline the resource list.
- Missing from docs: The evidence includes specific refactoring features (extract rule, introduce token) and diagram visualization that were mentioned briefly but not detailed.
- Missing from docs: The evidence shows Grammar-Kit can generate JFlex lexers and run JFlex generator, which was only briefly mentioned in the core features.
- Not in evidence: The original document's analogy comparing Grammar-Kit to a "recipe-to-meal converter" is not found in any evidence files.
- Style note: Removed all motivational content, encouragement boxes, and exclamation points per human-style guidelines.