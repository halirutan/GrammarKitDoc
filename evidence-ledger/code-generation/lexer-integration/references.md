# Section 3.3: Lexer Integration — References

## Source File References

| Claim | Source | Verified |
|---|---|---|
| Generated flex file named `_<GrammarName>Lexer.flex` | `BnfGenerateLexerAction.java:258-263` | Yes |
| Flex template at `/templates/lexer.flex.template` | `BnfGenerateLexerAction.java:57` | Yes |
| Velocity template engine used for generation | `BnfGenerateLexerAction.java:83-126` | Yes |
| Java regex patterns converted to JFlex syntax | `BnfGenerateLexerAction.java:218-256` | Yes |
| JFlex URL: jetbrains cache-redirector, version 1.9.2 | `BnfRunJFlexAction.java:254-311` | Yes |
| JFlex executed with `-Xmx512m` and `idea-flex.skeleton` | `BnfRunJFlexAction.java:128-186` | Yes |
| JFlex output shown in Messages tool window | `BnfRunJFlexAction.java:188-252` | Yes |
| Generated lexer implements `FlexLexer` interface | `lexer.flex.template` | Yes |
| Token constants imported from `elementTypeHolderClass` | `lexer.flex.template` | Yes |
| `BAD_CHARACTER` for unrecognized input | `lexer.flex.template` | Yes |
| Full JFlex IDE support: highlighting, completion, etc. | `plugin.xml:96-109` | Yes |
| Three token types: explicit, implicit keyword, implicit text-matched | `README.md:176-185` | Yes |
| Text-matched tokens are slower | `BnfAnnotator.java:141-151` | Yes |
| `tokenTypeClass` for custom IElementType subclass | `attributeDescriptions/tokenTypeClass.html` | Yes |
| `tokenTypeFactory` for factory method | `attributeDescriptions/tokenTypeFactory.html` | Yes |

## External References

- JFlex documentation: https://jflex.de/manual.html
- Grammar-Kit README (Lexer section): https://github.com/JetBrains/Grammar-Kit/blob/master/README.md
- IntelliJ Platform SDK: [Implementing Lexer](https://plugins.jetbrains.com/docs/intellij/implementing-lexer.html)
