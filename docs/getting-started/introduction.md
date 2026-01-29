# Introduction to GrammarKit

## Overview

GrammarKit is an IntelliJ IDEA plugin that generates parsers for custom languages, file formats, and domain-specific languages. It provides a complete workflow from grammar definition to working parser implementation.

You write your language grammar using extended Backus-Naur Form (BNF) syntax. GrammarKit then generates the Java parser code and PSI (Program Structure Interface) classes that IntelliJ needs to understand your language. The generated code integrates directly with IntelliJ's language support framework, enabling syntax highlighting, code completion, refactoring, and error detection.

The development workflow consists of five steps:

- Create a BNF grammar file describing your language
- Use Live Preview to test and refine your grammar
- Generate parser and PSI classes
- Create a JFlex lexer for tokenization
- Integrate with IntelliJ's language support framework

GrammarKit includes IDE features for grammar development: syntax highlighting, code completion, refactoring support, and inspections for BNF files. The Live Preview feature shows how your grammar parses text in real-time as you develop.

## When to Use GrammarKit

GrammarKit is designed for parsing structured text in IntelliJ IDEA. Use it when developing language plugins for programming languages, scripting languages, configuration languages, or query languages. Many production language plugins use GrammarKit, including [Clojure-Kit](https://github.com/gregsh/Clojure-Kit), [intellij-rust](https://github.com/intellij-rust/intellij-rust), and [intellij-erlang](https://github.com/ignatov/intellij-erlang).

The plugin also handles domain-specific languages like build configuration files, template languages, business rule languages, and data transformation languages. For file format parsing, GrammarKit works well with configuration files, data interchange formats, log files, and custom markup languages.

Consider alternatives when parsing simple key-value pairs (use Properties API), handling huge files that require streaming (use SAX-style parsing), or working with standard formats like JSON or XML (use existing parsers).

## Prerequisites

You need basic IntelliJ IDEA knowledge: creating projects, installing plugins, and navigating the IDE. Since GrammarKit generates Java code, you should understand Java syntax and basic object-oriented programming concepts. GrammarKit requires Java 17 or higher since version 2022.3.

Understanding parsing concepts helps but isn't required to start. The Live Preview feature lets you experiment and learn through immediate visual feedback. You'll develop intuition for tokens, lexers, grammar rules, and parse trees as you work.

Your development environment needs IntelliJ IDEA (Community or Ultimate Edition), JDK 17 or higher, and the GrammarKit plugin from the JetBrains Marketplace.

To install GrammarKit and create your first grammar, continue to the installation guide.