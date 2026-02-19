# Features

Grammar-Kit provides a BNF grammar editor, a parser and PSI code generator, and a Live Preview system for testing grammars interactively. It also supports JFlex lexer development. If you are building a custom language plugin, a DSL, or a file format parser, Grammar-Kit handles the grammar-to-code pipeline inside the IDE.

## Grammar Editing

Grammar-Kit treats BNF files (`.bnf`) and JFlex files (`.flex`) as first-class languages with full IDE support. The BNF editor provides syntax highlighting with 20 customizable color keys, covering elements from rules and tokens to pin and recover markers. JFlex files have their own dedicated highlighter and color settings.

Code completion suggests rule names, token names, attribute names, keywords, and external method references as you type. Navigation covers the standard operations: open the structure view (++ctrl+f12++), find usages of a rule (++alt+f7++), jump to generated code (++ctrl+alt+home++), or view a rule's FIRST and FOLLOW sets through quick documentation (++ctrl+q++).

Grammar-Kit includes refactoring actions adapted for grammar files. Extract Rule (++ctrl+alt+m++) pulls a selected expression into a new named rule. Introduce Token (++ctrl+alt+c++) extracts a token into a named definition. Inline Rule replaces references with the rule body, Rename provides in-place renaming for rules and attributes, and Unwrap Expression (++ctrl+shift+del++) removes surrounding parentheses or brackets.

Eight built-in inspections catch common grammar problems, all enabled by default:

- Unresolved BNF references
- Unused rule
- Unused attribute
- Suspicious token
- Left recursion
- Duplicate rule
- Identical choice branches
- Unreachable choice branch

Two intentions are available through ++alt+enter++: flip choice branches and convert between `?` and `[]` optional syntax. The editor also provides code folding, brace matching, commenting, spell checking, and regexp language injection in token patterns.

## Code Generation

Grammar-Kit generates a complete parser, element type constants, PSI interfaces, and PSI implementation classes from a single `.bnf` file. Trigger generation with ++ctrl+shift+g++ from the editor, or use the [Gradle plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) for build automation. The IDE supports batch generation across multiple `.bnf` files and a two-pass generation mode not available through Gradle.

For lexer development, Grammar-Kit can generate a `.flex` file from the token definitions in your BNF grammar, converting Java regex patterns to JFlex syntax. Running the JFlex generator (++ctrl+shift+g++ on a `.flex` file) compiles the flex specification into Java lexer code, automatically downloading JFlex 1.9.2 if needed. A parser utility class generator scaffolds a custom `parserUtilClass` when you need one.

For details on generated code structure, see [Attributes System](code-generation/attributes.md).

## Live Preview

Live Preview lets you test grammar rules against sample input without generating any code. Open it with ++ctrl+alt+p++ to get a split editor where one side shows your BNF grammar and the other accepts test input. The preview reparses automatically as you edit the grammar, with a 500ms debounce to avoid unnecessary work.

The preview pane includes its own structure view, so you can inspect the resulting parse tree directly. Grammar highlighting at caret (++ctrl+alt+f7++) shows which grammar expressions match at the current cursor position in the preview, so you can trace how your rules consume input.

For the full workflow, see [Live Preview Workflow](grammar-development/live-preview.md).

## IntelliJ Platform Integration

Generated parsers produce `PsiElement` implementations that plug directly into the IntelliJ Platform's [PSI framework](https://plugins.jetbrains.com/docs/intellij/psi.html). Grammar-Kit requires only `com.intellij.modules.lang` as a dependency, and the generated code integrates with standard Language API extension points like `lang.parserDefinition`, `lang.syntaxHighlighterFactory`, and `lang.findUsagesProvider`. Optional integrations add Java-aware navigation, UML diagram support, and copyright handling for generated files.

Multiple production plugins use Grammar-Kit, including [Rust](https://github.com/intellij-rust/intellij-rust), [Dart](https://github.com/JetBrains/intellij-plugins/tree/master/Dart), [Erlang](https://github.com/ignatov/intellij-erlang), [Elixir](https://github.com/KronicDeth/intellij-elixir), [Perl](https://github.com/Camelcade/Perl5-IDEA), [Haxe](https://github.com/HaxeFoundation/intellij-haxe), [Elm](https://github.com/intellij-elm/intellij-elm), [Clojure](https://github.com/gregsh/Clojure-Kit), and [Cypher](https://github.com/neueda/jetbrains-plugin-graph-database-support). The IntelliJ SDK documentation [recommends Grammar-Kit](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html) for implementing parsers and PSI.

To get started, see [Installation and Setup](installation.md) or go to the [Quick Start Tutorial](quick-start.md).
