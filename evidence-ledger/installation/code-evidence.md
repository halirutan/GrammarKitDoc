# Code Evidence: Installation and Setup

## Scope Information
This evidence covers section 1.2: Installation and Setup

## Plugin Installation
- Plugin ID: `org.jetbrains.idea.grammar`
- Plugin name: Grammar-Kit
- Marketplace: Available via IntelliJ plugin repository
- Version requirement: Java 17+ (since 2022.3)
- Platform version: 2023.3+ (pluginSinceBuild = 233)
- Dependencies: com.intellij.modules.lang

## Project Setup
- File type registration: `.bnf` extension
- Language name: BNF
- Icon: BnfIcons.FILE
- Plugin dependencies: Java, Diagram (optional), Copyright (optional)

## Creating BNF Files
- File extension: `.bnf`
- File type: BnfFileType.INSTANCE
- Language: BnfLanguage.INSTANCE
- Create via: New file with `.bnf` extension

## Basic Grammar Structure
- Root rule declaration: `root ::= expression`
- Sequence: `rule ::= part1 part2 part3`
- Choice: `rule ::= option1 | option2`
- Optional: `rule ::= [optional_part]` or `part?`
- Repetition: `rule ::= item*` or `item+`
- Grouping: `rule ::= (grouped parts)`

## Editor Features After Installation
- Syntax highlighting: BnfSyntaxHighlighterFactory
- Structure view: Ctrl+F12/Cmd+F12
- Live Preview: Ctrl+Alt+P/Cmd+Alt+P
- Generate parser: Ctrl+Shift+G/Cmd+Shift+G
- Brace matching: BnfBraceMatcher
- Code completion: BnfCompletionContributor
- Line comments: // or /* */
- Refactoring: Extract rule (Ctrl+Alt+M/Cmd+Alt+M)
- Refactoring: Introduce token (Ctrl+Alt+C/Cmd+Alt+C)
- Go to related file: Ctrl+Alt+Home/Cmd+Alt+Home
- Documentation popup: Ctrl+Q/Cmd+J

## Example Locations
- `testData/generator/Small.bnf`: Minimal grammar example
- `testData/livePreview/Json.bnf`: Simple complete grammar
- `grammars/Grammar.bnf`: Full BNF self-definition

## Out of Scope
Features found but excluded (belong to other sections):
- Grammar syntax details → Section 2.1
- Attribute system (pin, recoverWhile, extends) → Section 2.2
- Parser generation details → Section 3.x
- Advanced IDE features (inspections, diagram) → Section 5.2
- Expression parsing examples → Section 1.3