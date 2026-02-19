# Section 2.6: External Rules — References

## Source File References

| Claim | Source | Verified |
|---|---|---|
| External rule syntax: `external name ::= method params` | `README.md:149-170` | Yes |
| Inline syntax: `<<methodName params>>` | `README.md:149-157` | Yes |
| First two parameters always `PsiBuilder builder, int level` | `HOWTO.md:96-119` | Yes |
| Double-quoted strings passed as-is | `README.md:154-157` | Yes |
| Single-quoted strings unquoted first | `README.md:154-157` | Yes |
| Rule references become `GeneratedParserUtilBase.Parser` instances | `README.md:157` | Yes |
| `parserUtilClass` resolves external methods | `attributeDescriptions/parserUtilClass.html` | Yes |
| `parserImports` for additional static imports | `README.md:211-217` | Yes |
| Meta rules are parametrized parse functions | `README.md:104-106` | Yes |
| Meta rule parameters: `<<param>>` syntax | `README.md:104-106` | Yes |
| Live Preview: external static methods NOT supported | `LivePreviewParser.java:346-350` | Yes |
| Live Preview: only `eof` and `anything` supported | `LivePreviewParser.java:424-512` | Yes |
| Recovery predicates can be meta parameters | `ExternalRules.bnf:64-68` | Yes |
| Cross-class meta rule references work | `ExternalRules.bnf:81-99` | Yes |

## External References

- Grammar-Kit README (External Rules section): https://github.com/JetBrains/Grammar-Kit/blob/master/README.md
- Grammar-Kit HOWTO (External Rules section): https://github.com/JetBrains/Grammar-Kit/blob/master/HOWTO.md
- IntelliJ Platform SDK: [PsiBuilder](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html)
- GeneratedParserUtilBase (Parser interface): IntelliJ Platform source
