# Installation and Setup

This page covers installing the Grammar-Kit plugin, setting up a project with the right directory structure, and creating your first grammar file. After following these steps, you will have a working `.bnf` file with syntax highlighting and Live Preview.

## Prerequisites

Grammar-Kit runs inside IntelliJ IDEA. You need:

| Requirement | Minimum version |
|---|---|
| IntelliJ IDEA (Community or Ultimate) | 2023.3 or later |
| Java Development Kit | 17 or later |

You should be comfortable creating projects and navigating settings in IntelliJ IDEA. Java development experience is needed because Grammar-Kit generates Java source files. Familiarity with parsing concepts helps but is not required at this stage.

!!! note
    IntelliJ IDEA 2024.2 and later requires Java 21. Check the [Build Number Ranges](https://plugins.jetbrains.com/docs/intellij/build-number-ranges.html) page for your specific version.

## Installing the plugin

### From the marketplace

1. Open **Settings** (++ctrl+alt+s++ / ++cmd+comma++) and select **Plugins**.
2. Switch to the **Marketplace** tab and search for "Grammar-Kit".
3. Click **Install**, then restart the IDE when prompted.

The plugin is also available at [plugins.jetbrains.com/plugin/6606-grammar-kit](https://plugins.jetbrains.com/plugin/6606-grammar-kit).

For development builds, JetBrains publishes artifacts on [TeamCity](https://teamcity.jetbrains.com/guestAuth/app/rest/builds/buildType:IntellijIdeaPlugins_GrammarKit_Build,status:SUCCESS/artifacts/content/GrammarKit*.zip). Download the zip and install it through **Settings > Plugins > gear icon > Install Plugin from Disk**.

### Version compatibility

| Grammar-Kit | IntelliJ IDEA | Java |
|---|---|---|
| 2023.3 | 2023.3+ | 17 |
| 2022.3 | 2022.3+ | 17 |
| 2021.1 | 2021.1+ | 11 |
| 2020.3 | 2020.3+ | 11 |

Grammar-Kit follows the IntelliJ IDEA version numbering scheme. Each release targets the corresponding platform version and later.

### Verifying the installation

Create a new file with the `.bnf` extension in any project. If Grammar-Kit is installed correctly, you will see:

1. A BNF file icon on the editor tab.
2. Syntax highlighting for keywords, rules, and tokens.
3. Code completion when you start typing attributes or rule names.

Open Live Preview with ++ctrl+alt+p++ (++cmd+alt+p++ on macOS) to confirm the editor is fully functional. The preview pane displays a parse tree as you type grammar rules and sample input.

## Project setup

A language plugin project needs separate source roots for handwritten code and generated code. As the Grammar-Kit documentation states: "Handwritten classes and generated classes should always be in different source roots."

The recommended directory layout for a Gradle-based IntelliJ plugin project:

```
my-language-plugin/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
│
├── src/main/java/                          ← Handwritten source code
│   └── com/example/config/
│       ├── ConfigLanguage.java             ← Language singleton
│       ├── ConfigFileType.java             ← File type registration
│       ├── ConfigParserDefinition.java     ← Connects parser + lexer
│       ├── ConfigSyntaxHighlighter.java    ← Syntax coloring
│       └── ConfigLexer.flex                ← JFlex lexer definition
│
├── src/main/gen/                           ← Generated code (separate root!)
│   └── com/example/config/
│       ├── parser/
│       │   └── ConfigParser.java           ← Generated parser
│       └── psi/
│           ├── ConfigTypes.java            ← Generated element types
│           ├── ConfigProperty.java         ← Generated PSI interface
│           └── impl/
│               └── ConfigPropertyImpl.java ← Generated PSI implementation
│
├── src/main/resources/
│   ├── META-INF/
│   │   └── plugin.xml                      ← Plugin registration
│   └── com/example/config/
│       └── config.bnf                      ← Grammar file
│
└── src/test/
    ├── java/                               ← Test source code
    └── testData/                            ← Test input files
```

!!! warning
    Do not mix generated and handwritten code in the same source root. Regenerating the parser may overwrite handwritten files, and refactoring tools may modify generated code.

Mark `src/main/gen` as a generated source root in your `build.gradle.kts`:

```kotlin
sourceSets {
    main {
        java.srcDirs("src/main/java", "src/main/gen")
    }
}

idea {
    module {
        generatedSourceDirs.add(file("src/main/gen"))
    }
}
```

Some projects use a flat layout closer to Grammar-Kit's own structure, with top-level `src/`, `gen/`, and `resources/` directories. Either layout works as long as handwritten and generated code stay in separate roots.

### Dependencies and templates

The generated parser relies on `GeneratedParserUtilBase`, which ships with the IntelliJ Platform since version 12.1. You do not need to bundle it.

For build automation, the [Gradle Grammar-Kit Plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) (`org.jetbrains.grammarkit`, version 2023.3.0.2) runs parser and lexer generation as part of your Gradle build. See the [IntelliJ SDK documentation](https://plugins.jetbrains.com/docs/intellij/tools-gradle-grammar-kit-plugin.html) for configuration details, and [Gradle Plugin Setup](integration/gradle-setup.md) for a full walkthrough. The Gradle plugin does not support method mixins, and generic signatures may not be correct in all cases.

To start a new project from scratch, the [IntelliJ Platform Plugin Template](https://github.com/JetBrains/intellij-platform-plugin-template) provides a ready-made Gradle project structure. The IntelliJ SDK also has a [Creating a Plugin Project](https://plugins.jetbrains.com/docs/intellij/creating-plugin-project.html) guide that walks through the new-project wizard.

### Configuring the development environment

The default output directory for generated code is `gen`. You can change it and other plugin behavior through Java system properties (`-D` flags passed to the IDE or Gradle):

| Property | Default | Purpose |
|---|---|---|
| `grammar.kit.gen.dir` | `gen` | Output directory for generated code |
| `grammar.kit.gen.jflex.args` | (empty) | Extra arguments for JFlex generation |
| `grammar.kit.gpub.max.level` | `1000` | Parser recursion depth limit |
| `grammar.kit.inject.java` | `true` | Inject Java language in JFlex files |
| `grammar.kit.inject.regexp` | `true` | Inject RegExp language in BNF strings |

Whether to commit the `gen/` directory to version control is a team decision. Committing it makes the build reproducible without running generation but adds noise to diffs. Adding `gen/` to `.gitignore` keeps the repository clean but requires all contributors to generate before building.

## Your first grammar file

The smallest valid grammar is a single rule with no attributes:

```bnf
// minimal.bnf — Works in Live Preview without any attributes.
root ::= 'hello' 'world'
```

This grammar is enough to test Live Preview immediately. No attributes block is needed for prototyping, but without output paths configured, the grammar is not ready for code generation.

To generate code, you need an attributes block that specifies where the generated classes go. The following grammar for a simple key-value configuration language shows the complete structure:

```bnf
// config.bnf — A grammar for key-value configuration files.
//
// Example input this grammar parses:
//   host = "localhost"
//   port = 8080
//   debug = true

{
  // Where to put generated parser code
  parserClass="com.example.config.parser.ConfigParser"

  // Where to put generated PSI interfaces and implementations
  psiPackage="com.example.config.psi"
  psiImplPackage="com.example.config.psi.impl"

  // Class that holds all IElementType constants
  elementTypeHolderClass="com.example.config.psi.ConfigTypes"

  // Factory methods for element types (use defaults for now)
  elementTypeClass="com.example.config.psi.ConfigElementType"
  tokenTypeClass="com.example.config.psi.ConfigTokenType"

  // Token definitions — names on the left, patterns on the right
  tokens=[
    EQUALS  = '='
    SEMI    = ';'
    space   = 'regexp:\s+'
    comment = 'regexp://.*'
    number  = 'regexp:\d+'
    string  = "regexp:\"[^\"]*\""
    id      = 'regexp:\p{Alpha}\w*'
  ]
}

// The first rule is the root of the grammar.
// The parser starts here.
root ::= item *

// 'private' means this rule won't create its own PSI node.
// Its children fold into the parent.
private item ::= property ';'? {recoverWhile=item_recover}

// A property is an identifier, '=', and a value.
property ::= id '=' value {pin=2}

// Values can be strings, numbers, or identifiers (references).
value ::= string | number | id

// Recovery rule: skip tokens until we find something
// that looks like the start of the next property.
private item_recover ::= !(id | ';')
```

A grammar file has three parts. The attributes block (`{ ... }`) at the top configures code generation output locations. The `tokens` list inside it maps token names to string literals or regex patterns using the `'regexp:...'` syntax. The rules section defines the grammar structure, where each rule uses the `::=` operator. The first rule in the file becomes the parse root.

You can reference tokens by their quoted value (`'='`) for readability or by their name (`EQUALS`). Both forms resolve to the same token.

!!! tip
    Set `parserClass`, `psiPackage`, and `elementTypeHolderClass` before generating code. Without these attributes, Grammar-Kit uses defaults like `generated.GeneratedParser` and `generated.GeneratedTypes`, which are unlikely to match your project's package structure.

After saving the grammar file, test it:

1. Confirm the file shows a BNF icon in the editor tab.
2. Press ++ctrl+alt+p++ (++cmd+alt+p++) to open Live Preview.
3. Type sample input in the preview pane and check that a parse tree appears.
4. Press ++ctrl+shift+g++ (++cmd+shift+g++) to generate parser code into your `gen/` directory.

Editor features available for `.bnf` files:

| Feature | Shortcut | What it does |
|---|---|---|
| Live Preview | ++ctrl+alt+p++ / ++cmd+alt+p++ | Test grammar against sample input |
| Generate Parser Code | ++ctrl+shift+g++ / ++cmd+shift+g++ | Generate parser, PSI, and element types |
| Structure View | ++ctrl+f12++ / ++cmd+f12++ | Browse rules in the current file |
| Quick Documentation | ++ctrl+q++ / ++cmd+j++ | Show FIRST and FOLLOW sets for a rule |
| Go to Related File | ++ctrl+alt+home++ / ++cmd+alt+home++ | Jump to the generated file for a rule |

Eight inspections run by default, catching problems like unresolved references, unused rules, left recursion, and duplicate rules. Warnings appear directly in the editor as you type.

Next: the [Quick Start Tutorial](quick-start.md) walks through building a complete language plugin from grammar to working IDE support.
