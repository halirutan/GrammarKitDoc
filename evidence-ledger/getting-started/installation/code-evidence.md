# Code Evidence: Installation and Setup

## Scope Information
This evidence covers section 1.3: Installation and Setup

---

## Plugin Identity
- Plugin name: `Grammar-Kit`
- Plugin ID: `org.jetbrains.idea.grammar` (from plugin.xml line 2)
- Vendor: JetBrains
- Marketplace URL: `http://plugins.jetbrains.com/plugin/6606`
- Description: "BNF Grammars and JFlex lexers editor. Readable parser/PSI code generator."
- GitHub repository: `https://github.com/JetBrains/Grammar-Kit`
- License: Apache 2.0
- Current dev version: `2023.3-dev` (from gradle.properties)
- Plugin group: `org.jetbrains`

## System Requirements
- **Java**: Java 17 required since Grammar-Kit 2022.3 (README.md: "Since 2022.3, Grammar-Kit plugin requires Java 17")
- **Java compile target**: `javaVersion=17` (gradle.properties line 33)
- **Default Java version for generated code**: 11 (GenOptions.java line 65: `javaVersion = StringUtil.parseInt(genOptions.get("java"), 11)`)
- **IntelliJ Platform**: since build `233` = IntelliJ IDEA 2023.3+ (gradle.properties line 9)
- **Platform type**: IU (IntelliJ IDEA Ultimate used for development, but plugin works on Community)
- **Required platform dependency**: `com.intellij.modules.lang` (plugin.xml line 9)

## Plugin Dependencies
- **Required**: `com.intellij.modules.lang` (core language support)
- **Optional**: `com.intellij.copyright` (copyright plugin integration)
- **Optional**: `com.intellij.java` (Java-related extensions, class references)
- **Optional**: `com.intellij.diagram` (UML/PSI tree diagrams)

## Version Compatibility Matrix (from CHANGELOG.md)
- `2023.3` - IntelliJ IDEA 2023.3+, Java 17, compatibility with 2024.2
- `2022.3` - IntelliJ IDEA 2022.3+, Java 17
- `2022.3.1` - Fixed compatibility with 2023.1 EAP
- `2021.1` - IntelliJ IDEA 2021.1+
- `2020.3` - IntelliJ IDEA 2020.3+, switched default generated Java to 11
- `2019.1` - Switched to year-based versioning
- `2017.1` - Switched to IntelliJ IDEA versioning scheme

## Installation Methods
- **Marketplace**: Settings/Preferences > Plugins > Marketplace > search "Grammar-Kit"
- **Offline/manual**: Download from marketplace URL or TeamCity dev builds
- **Latest dev build URL**: `https://teamcity.jetbrains.com/guestAuth/app/rest/builds/buildType:IntellijIdeaPlugins_GrammarKit_Build,status:SUCCESS/artifacts/content/GrammarKit*.zip`
- **Verification**: After install, `.bnf` files get BNF file type icon and syntax highlighting

## File Types Registered
- **BNF files**: extension `.bnf`, language ID `BNF`, file type name `BNF`
  - Source: BnfFileType.java - `getDefaultExtension()` returns `"bnf"`
  - Registered in plugin.xml: `extensions="bnf" language="BNF"`
- **JFlex files**: extension `.flex`, language ID `JFlex`, file type name `JFlex`
  - Registered in plugin.xml: `extensions="flex" language="JFlex"`
- **Live Preview**: internal file type `BNF_LP`, language `BNF_LP`

## Project Setup - Directory Structure
- **Recommended separation**: "Handwritten classes and generated classes should always be in different source roots." (HOWTO.md line 11)
- **Source directories** (from Grammar-Kit's own build.gradle.kts):
  - `src` - handwritten source code
  - `gen` - generated parser/PSI code (marked as generated source dir)
  - `resources` - resource files
  - `tests` - test source code
  - `testData` - test data files
- **Generated output directory**: configurable via `grammar.kit.gen.dir` system property, default `"gen"` (Options.java line 14)
- **Generation target logic** (FileGeneratorUtil.java):
  - If BNF file is in a source root, generates to `gen/` under content root
  - Respects `parserClass` package for subdirectory structure
  - Looks for existing files first to determine target

## Essential Dependencies (for consuming projects)
- **Grammar-Kit library** (for Gradle builds):
  - Maven coordinates: `org.jetbrains:Grammar-Kit` (build.gradle.kts publishing section)
  - Artifact: `grammar-kit.jar` (buildGrammarKitJar task, line 135)
  - Published to MavenCentral (nexusPublishing config)
- **Gradle plugin** (for build automation):
  - `gradle-grammar-kit-plugin`: `https://github.com/JetBrains/gradle-grammar-kit-plugin`
  - Limitations: no method mixins, generic signatures may be incorrect (README.md lines 51-52)
- **Runtime dependency**: `GeneratedParserUtilBase` included in IntelliJ Platform since 12.1 (README.md line 209)
- **No need to bundle** GeneratedParserUtilBase in projects

## Configuration - Plugin Settings
- `grammar.kit.gen.dir` - output directory for generated code (default: `"gen"`)
- `grammar.kit.gen.jflex.args` - JFlex generator arguments (default: `""`)
- `grammar.kit.gpub.max.level` - parser recursion depth limit (default: `1000`)
- `grammar.kit.inject.java` - inject Java in JFlex files (default: `true`)
- `grammar.kit.inject.regexp` - inject RegExp in BNF strings (default: `true`)
- Source: Options.java

## Configuration - Default Attribute Values (for new grammars)
- `parserClass` default: `"generated.GeneratedParser"`
- `psiPackage` default: `"generated.psi"`
- `psiImplPackage` default: `"generated.psi.impl"`
- `elementTypeHolderClass` default: `"generated.GeneratedTypes"`
- `psiClassPrefix` default: `""` (empty)
- `psiImplClassSuffix` default: `"Impl"`
- `psiVisitorName` default: `"Visitor"`
- `extendedPin` default: `true`
- `generatePsi` default: `true`
- `generateTokens` default: `true`
- `generateFirstCheck` default: `2`
- Source: KnownAttribute.java

## First Grammar File - Basic Structure
- File extension: `.bnf`
- Structure: optional attributes block `{ ... }` followed by rules
- Rules use `::=` operator: `rule_name ::= expression`
- Comments: `//` line comments, `/* */` block comments
- Strings: single-quoted `'text'` or double-quoted `"text"`
- Regexp tokens: `'regexp:\pattern'`

## First Grammar File - Minimal Grammar Pattern
- Header attributes block (optional but recommended): `{ parserClass="..." psiPackage="..." }`
- Root rule: first rule or specified via `external grammar ::= parseGrammar ...`
- Token definitions in `tokens=[...]` block
- Rules defined as `name ::= expression`
- Source: Grammar.bnf (self-definition), Json.bnf (simple example)

## Verification - How to Confirm Installation Works
- **File recognition**: Create a `.bnf` file; it should show BNF file icon
- **Syntax highlighting**: BNF keywords, rules, tokens get colored
- **Editor features available after install**:
  - Code completion for attributes and rules
  - Structure view (Ctrl+F12 / Cmd+F12)
  - Live Preview (Ctrl+Alt+P / Cmd+Alt+P)
  - Generate Parser Code (Ctrl+Shift+G / Cmd+Shift+G)
  - Quick documentation (Ctrl+Q / Cmd+J) shows FIRST/FOLLOWS sets
- **Inspections active** (all enabled by default):
  - Unresolved BNF references
  - Unused rule
  - Unused attribute
  - Suspicious token
  - Left recursion
  - Duplicate rule
  - Identical choice branches
  - Unreachable choice branch
- **Context menu items**: Live Preview, Generate Parser Code, Generate JFlex Lexer, Run JFlex Generator

## IDE Actions and Shortcuts
- Generate Parser Code: Ctrl+Shift+G / Cmd+Shift+G
- Live Preview: Ctrl+Alt+P / Cmd+Alt+P
- Grammar Highlighting (in preview): Ctrl+Alt+F7 / Cmd+Alt+F7
- Extract Rule: Ctrl+Alt+M / Cmd+Alt+M (reuses ExtractMethod shortcut)
- Introduce Token: Ctrl+Alt+C / Cmd+Alt+C (reuses IntroduceConstant shortcut)
- Structure popup: Ctrl+F12 / Cmd+F12
- Go to related file: Ctrl+Alt+Home / Cmd+Alt+Home
- Quick documentation: Ctrl+Q / Cmd+J
- Navigate to matched expressions: Ctrl+B / Cmd+B (inside attribute pattern)
- Unwrap/remove expression: Ctrl+Shift+Del / Cmd+Shift+Del
- Flip choice branches: Alt+Enter (intention)

## General Usage Workflow (from README.md)
1. Create grammar `*.bnf` file
2. Tune grammar using Live Preview + Structure view
3. Generate parser/ElementTypes/PSI classes (Ctrl+Shift+G)
4. Generate lexer `*.flex` file, then run JFlex generator (context menu)
5. Implement ParserDefinition and register in plugin.xml
6. Mix-in resolve and other functionality to PSI

## Related Resources
- IntelliJ Platform Plugin Template: `https://github.com/JetBrains/intellij-platform-plugin-template`
- Custom Language Support Tutorial: `https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html`
- JetBrains Slack: `#intellij-platform` channel
- X/Twitter: `@JBPlatform`

## Example Locations
- `testData/livePreview/Json.bnf` - minimal complete grammar (JSON)
- `testData/generator/ExprParser.bnf` - expression grammar with tokens block
- `testData/livePreview/LivePreviewTutorial.bnf` - tutorial grammar
- `grammars/Grammar.bnf` - Grammar-Kit's own BNF self-definition (complete attribute example)
- `TUTORIAL.md` - full sample.bnf grammar text inline

## Out of Scope
Features found but excluded (belong to other sections):
- Detailed grammar syntax (rule modifiers, meta rules, predicates) -> Section 2.1
- Attribute system details (pin, recoverWhile, extends, etc.) -> Section 3.1
- Parser generation internals (two-pass, code splitting) -> Section 3.2
- Expression parsing (left recursion, operator precedence) -> Section 2.3
- Gradle plugin setup details -> Section 4.2.1
- Quick start tutorial walkthrough -> Section 1.4
- Error recovery mechanics (pin/recoverWhile behavior) -> Section 2.4
- Live Preview workflow details -> Section 2.5
- PSI customization (mixin, methods, fake rules) -> Section 3.4
- JFlex lexer development -> Section 3.3

## Missing Documentation
- No official version compatibility matrix published (reconstructed from CHANGELOG)
- No explicit minimum IntelliJ version per Grammar-Kit version table
- No documented offline installation steps (only dev build link provided)
- No official project template or archetype for Grammar-Kit projects
- `grammar.kit.gen.dir` and other system properties not documented in README
- No documented SDK configuration steps specific to Grammar-Kit
- No team development / VCS best practices documented in source
