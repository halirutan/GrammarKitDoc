# Section 3.2: Parser Generation — References

## Source File References

| Claim | Source | Verified |
|---|---|---|
| Generate shortcut: Ctrl-Shift-G / Cmd-Shift-G | `README.md:39` | Yes |
| GenerateAction extends AnAction | `GenerateAction.java:51` | Yes |
| Generator runs in background with progress indicator | `GenerateAction.java:107-120` | Yes |
| ParserGenerator extends GeneratorBase | `ParserGenerator.java:57` | Yes |
| Generation order: parsers, types, PSI interfaces, PSI impls, visitor | `ParserGenerator.java:277-341` | Yes |
| Static methods generated for each BNF expression | `README.md:113-120` | Yes |
| Naming convention: `rule_name_N1_N2_..._NX` | `README.md:113-120` | Yes |
| Sequence → short-circuit `&&` chain | `HOWTO.md:18-68` | Yes |
| Choice → fallthrough `if (!result)` chain | `HOWTO.md:18-68` | Yes |
| Zero-or-more → `while(true)` loop returning true | `HOWTO.md:18-68` | Yes |
| Expression parsing generates Pratt-parser with priority table | `HOWTO.md:124-223` | Yes |
| Abstract rules get no parsing code | `ParserGenerator.java:182-199` | Yes |
| Command-line: `java -jar grammar-kit.jar <output> <grammars>` | `HOWTO.md:400-424` | Yes |
| Gradle limitations: no method mixins, no two-pass | `README.md:44-51` | Yes |
| Target directory resolved from parserClass package | `GenerateAction.java:87-105` | Yes |
| Default file header: `"// This is a generated file..."` | `BnfConstants.java:14` | Yes |

## External References

- Grammar-Kit README: https://github.com/JetBrains/Grammar-Kit/blob/master/README.md
- Grammar-Kit HOWTO: https://github.com/JetBrains/Grammar-Kit/blob/master/HOWTO.md
- Gradle Grammar-Kit Plugin: https://github.com/JetBrains/gradle-grammar-kit-plugin
- IntelliJ Platform SDK: [Implementing a Parser](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html)
