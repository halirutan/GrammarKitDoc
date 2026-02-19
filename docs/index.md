# What is Grammar-Kit?

Grammar-Kit is an IntelliJ IDEA plugin by JetBrains for language plugin developers. It transforms BNF grammar definitions into working parsers, PSI classes, and lexer definitions, replacing hand-written parsing code with generated, readable output. The [IntelliJ Platform SDK documentation](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html) explicitly recommends Grammar-Kit for parser and PSI generation.

Grammar-Kit takes a `.bnf` grammar file as input and generates a PsiBuilder-based recursive descent parser, element type constants, and PSI (Program Structure Interface) classes. It also generates JFlex lexer definitions (`.flex` files) from the same grammar. You write the grammar, and Grammar-Kit produces the code that turns source text into a structured syntax tree your IDE plugin can work with.

## Use cases

Grammar-Kit handles a range of parsing tasks for IntelliJ-based IDEs:

- Programming languages: production plugins for Rust, Dart, Erlang, Clojure, Elm, Elixir, Perl, and Haxe all use Grammar-Kit. JetBrains' own [Dart plugin](https://github.com/JetBrains/intellij-plugins/tree/master/Dart) is built with it.
- Configuration formats: grammars for structured formats like JSON. Grammar-Kit includes a [JSON grammar](https://github.com/JetBrains/Grammar-Kit/blob/master/testData/livePreview/Json.bnf) as a test example.
- Domain-specific languages: custom expression languages, query languages, and other DSLs. Grammar-Kit's own BNF grammar is defined in itself.
- Query languages: specialized parsers like the [Cypher graph database plugin](https://github.com/neueda/jetbrains-plugin-graph-database-support).

The generated PSI tree integrates directly with the IntelliJ Platform, providing the foundation that powers syntax highlighting, code completion, navigation, and other IDE features. Grammar-Kit does not generate those features itself, but it produces the structural layer they depend on.

## Key capabilities

Grammar-Kit covers the full cycle from grammar authoring through code generation and IDE integration.

Live Preview lets you test a grammar against sample text in real time, without generating code or compiling anything. Open it with Ctrl+Alt+P (Cmd+Alt+P on macOS), and a structure view shows the PSI tree as you edit the grammar. This is the fastest way to iterate on grammar rules. See [Live Preview](grammar-development/live-preview.md) for details.

Expression parsing handles operator precedence automatically. You define expression rules in your grammar, and Grammar-Kit generates a compact Pratt-like parser that supports binary, prefix, postfix, and n-ary operators with correct priority and associativity. The entire expression hierarchy compiles down to just two generated methods. See [Expression Parsing](grammar-development/expression-parsing.md) for details.

Error recovery uses two attributes, `pin` and `recoverWhile`, to keep parsing useful even when input is incomplete or contains unexpected tokens. The `pin` attribute commits the parser at a specific position so it reports errors without abandoning the current rule. The `recoverWhile` attribute skips unexpected tokens until a recovery predicate matches. See [Error Recovery](grammar-development/error-recovery.md) for details.

Generated parsers integrate directly with the IntelliJ Platform. They extend `LightPsiParser`, and the runtime base class (`GeneratedParserUtilBase`) ships with the IntelliJ Platform itself since version 12.1, so you do not need to bundle it. A [Gradle plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) supports automated parser generation in CI builds.

The typical workflow is: create a `.bnf` file, prototype with Live Preview, generate parser and PSI classes (Ctrl+Shift+G / Cmd+Shift+G), generate a JFlex lexer, then implement `ParserDefinition` and register it in `plugin.xml`. The [Quick Start Tutorial](quick-start.md) walks through this process step by step.

---

To continue, see the [Features](features.md) overview, [install Grammar-Kit](installation.md), or jump to the [Quick Start Tutorial](quick-start.md).
