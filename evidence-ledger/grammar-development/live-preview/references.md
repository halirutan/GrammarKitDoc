# Section 2.5: Live Preview — References

## Source File References

| Claim | Source | Verified |
|---|---|---|
| Live Preview shortcut is Ctrl-Alt-P | `plugin.xml:115`, `README.md:38` | Yes |
| Grammar Highlighting shortcut is Ctrl-Alt-F7 | `plugin.xml:124`, `README.md:71-72` | Yes |
| LivePreviewAction extends DumbAwareAction | `LivePreviewAction.java:20-39` | Yes |
| Preview file named `<grammar>.bnf.preview` | `LivePreviewHelper.java:85-95` | Yes |
| Auto-reparse uses 500ms MergingUpdateQueue | `LivePreviewHelper.java:64-77` | Yes |
| Dynamic language via ASM bytecode generation | `LivePreviewLanguage.java:143-183` | Yes |
| Lexer uses longest-match greedy algorithm | `LivePreviewLexer.java:77-108` | Yes |
| Keywords detected via StringUtil.isJavaIdentifier() | `LivePreviewLexer.java:162-188` | Yes |
| Whitespace tokens auto-detected from unused regexp tokens | `TUTORIAL.md:79-80`, `LivePreviewLexer.java:200-218` | Yes |
| Parser supports pin, recoverWhile, extends, hooks | `LivePreviewParser.java:134-312` | Yes |
| External static methods NOT supported in preview | `LivePreviewParser.java:346-350` | Yes |
| Only `eof` and `anything` external expressions supported | `LivePreviewParser.java:424-512` | Yes |
| Recursion detection via BitSet per offset | `LivePreviewParser.java:121-132` | Yes |
| Structure view shows PSI tree | `LivePreviewStructureViewFactory.java:40-153` | Yes |
| Brace pairs auto-created for `{}()[]<>` | `LivePreviewParser.java:66-71` | Yes |
| Recommended workflow: prototype → generate flex → ParserDefinition → perfect | `TUTORIAL.md:68-73` | Yes |
| Live Preview uses Java regex, JFlex supports subset | `README.md:240-241` | Yes |

## External References

- IntelliJ Platform SDK: [PsiBuilder](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html)
- IntelliJ Platform SDK: [Language and File Type](https://plugins.jetbrains.com/docs/intellij/language-and-filetype.html)
- Grammar-Kit README: https://github.com/JetBrains/Grammar-Kit/blob/master/README.md
- Grammar-Kit TUTORIAL: https://github.com/JetBrains/Grammar-Kit/blob/master/TUTORIAL.md
