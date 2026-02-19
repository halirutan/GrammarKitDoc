# Section 2.7: Grammar Composition — References

## Source File References

| Claim | Source | Verified |
|---|---|---|
| `parserClass` can split parsing code into multiple files | `attributeDescriptions/parserClass.html` | Yes |
| Semicolon required before `{` for global attribute block | `attributeDescriptions/parserClass.html` | Yes |
| Generator splits code for large grammars | `README.md:202-208` | Yes |
| Pattern-based attributes apply via regex | `README.md:122-129` | Yes |
| `extraRoot` marks additional parse entry points | `attributeDescriptions/extraRoot.html` | Yes |
| Token definitions from first block apply to all parser classes | `README.md:172-186` | Yes |
| PSI configuration shared across parser classes | `testData/generator/PsiGen.bnf` (observation) | Yes |
| Cross-class meta rule references work | `testData/generator/ExternalRules.bnf:81-99` | Yes |
| Generator produces files in order: parsers, types, PSI interfaces, PSI impls, visitor | `ParserGenerator.java:277-341` | Yes |
| Grammar.bnf and JFlex.bnf coexist with separate namespaces | `grammars/Grammar.bnf`, `grammars/JFlex.bnf` | Yes |

## External References

- Grammar-Kit README (Parser Structure): https://github.com/JetBrains/Grammar-Kit/blob/master/README.md
- IntelliJ Platform SDK: [Plugin Structure](https://plugins.jetbrains.com/docs/intellij/plugin-structure.html)
