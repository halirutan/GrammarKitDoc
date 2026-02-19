# Resources

## Official Resources

Grammar-Kit is developed and maintained by JetBrains. These are the primary sources for code, releases, and issue tracking.

| Resource | Link |
|----------|------|
| GitHub repository | [JetBrains/Grammar-Kit](https://github.com/JetBrains/Grammar-Kit) |
| Issue tracker | [GitHub Issues](https://github.com/JetBrains/Grammar-Kit/issues) |
| Plugin marketplace | [Grammar-Kit on JetBrains Marketplace](https://plugins.jetbrains.com/plugin/6606-grammar-kit) |
| Gradle plugin | [gradle-grammar-kit-plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) |
| Maven Central | `org.jetbrains:Grammar-Kit` |

The repository includes several documentation files worth reading directly:

| File | Contents |
|---|---|
| `README.md` | Feature overview, syntax reference, and attribute documentation |
| `TUTORIAL.md` | Step-by-step guide using Live Preview |
| `HOWTO.md` | Advanced topics including expression parsing, stubs, and code patterns |
| `CHANGELOG.md` | Version history from 1.0 through 2023.3 |

## IntelliJ Platform Documentation

Grammar-Kit generates code that integrates with the IntelliJ Platform's PSI framework. These resources cover the platform side of language plugin development.

| Resource | Link |
|----------|------|
| IntelliJ Platform SDK documentation | [plugins.jetbrains.com/docs/intellij](https://plugins.jetbrains.com/docs/intellij/) |
| Implementing a parser and PSI | [Parser and PSI guide](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html) |
| Custom language support tutorial | [Custom Language Support](https://plugins.jetbrains.com/docs/intellij/custom-language-support.html) |
| Plugin structure | [Plugin Structure](https://plugins.jetbrains.com/docs/intellij/plugin-structure.html) |
| Stub indexes | [Stub Indexes](https://plugins.jetbrains.com/docs/intellij/stub-indexes.html) |
| IntelliJ plugin template | [intellij-platform-plugin-template](https://github.com/JetBrains/intellij-platform-plugin-template) |

The SDK documentation [recommends Grammar-Kit](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html) as the standard approach for implementing parsers and PSI in language plugins.

## JFlex Resources

Grammar-Kit uses JFlex for lexer generation. JFlex 1.9.2 is downloaded automatically when you run the JFlex generator from the IDE.

| Resource | Link |
|----------|------|
| JFlex manual | [jflex.de/manual.html](https://jflex.de/manual.html) |
| JFlex GitHub | [jflex-de/jflex](https://github.com/jflex-de/jflex) |

Grammar-Kit uses a custom `idea-flex.skeleton` file extracted from the JFlex jar, which adapts JFlex output for use with the IntelliJ Platform lexer API. See [Lexer Integration](../code-generation/lexer-integration.md) for details.

## Build Tools

These tools are relevant if you automate parser generation in a build pipeline rather than generating from the IDE.

| Resource | Link |
|----------|------|
| Gradle | [gradle.org](https://gradle.org/) |
| IntelliJ Platform Gradle Plugin | [Gradle IntelliJ Plugin](https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html) |
| Gradle Changelog Plugin | [gradle-changelog-plugin](https://github.com/JetBrains/gradle-changelog-plugin) |

For Gradle-based parser generation setup, see [Gradle Setup](../integration/gradle-setup.md).

## Example Projects

Several production IntelliJ plugins use Grammar-Kit for their parsers. These repositories are useful as real-world references for grammar design, PSI customization, and plugin structure:

| Plugin | Language | Repository |
|---|---|---|
| intellij-rust | Rust | [intellij-rust](https://github.com/intellij-rust/intellij-rust) |
| intellij-plugins/Dart | Dart | [Dart](https://github.com/JetBrains/intellij-plugins/tree/master/Dart) |
| intellij-erlang | Erlang | [intellij-erlang](https://github.com/ignatov/intellij-erlang) |
| intellij-elixir | Elixir | [intellij-elixir](https://github.com/KronicDeth/intellij-elixir) |
| Perl5-IDEA | Perl | [Perl5-IDEA](https://github.com/Camelcade/Perl5-IDEA) |
| intellij-haxe | Haxe | [intellij-haxe](https://github.com/HaxeFoundation/intellij-haxe) |
| intellij-elm | Elm | [intellij-elm](https://github.com/intellij-elm/intellij-elm) |
| Clojure-Kit | Clojure | [Clojure-Kit](https://github.com/gregsh/Clojure-Kit) |

## Parsing Theory

These references cover the parsing algorithms and techniques that Grammar-Kit builds on.

- [Top Down Operator Precedence](http://javascript.crockford.com/tdop/tdop.html) by Douglas Crockford, describing the Pratt parsing approach that Grammar-Kit uses for expression parsing.
- Grammar-Kit's own `testData/generator/ExprParser.bnf`, a complete working example of Pratt-style expression parsing (included in [Example Grammars](examples.md)).

## Community

Grammar-Kit development happens on GitHub. File bug reports and feature requests through [GitHub Issues](https://github.com/JetBrains/Grammar-Kit/issues). Contributions are accepted as pull requests. The project is maintained by Greg Shrago (gregsh) at JetBrains and licensed under Apache 2.0.

## Version Requirements

The current Grammar-Kit development version targets the following platform:

| Component | Version |
|-----------|---------|
| Grammar-Kit | 2023.3-dev |
| IntelliJ IDEA (minimum) | 2023.3 (build 233) |
| Java | 17 |
| Gradle | 8.14.2 |

For installation instructions, see [Installation and Setup](../installation.md).
