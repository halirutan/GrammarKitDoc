# Installation and Setup

This guide covers installing Grammar-Kit and setting up your first language plugin project.

## Prerequisites

Before installing Grammar-Kit, ensure your development environment meets these requirements:

- IntelliJ IDEA 2023.3 or later
- Java 17 or higher runtime environment
- Basic familiarity with IntelliJ IDEA's interface

## Installing Grammar-Kit

Open IntelliJ IDEA and navigate to **Settings** → **Plugins** → **Marketplace**. Search for "Grammar-Kit" and find the plugin with ID `org.jetbrains.idea.grammar`. Click **Install** and restart the IDE when prompted.

After restarting, verify the installation by creating a new file with the `.bnf` extension. The editor should display syntax highlighting for BNF grammar files. Test these keyboard shortcuts to confirm Grammar-Kit is active:

- **Ctrl+F12** (Cmd+F12 on Mac) - Opens the structure view
- **Ctrl+Alt+P** (Cmd+Alt+P on Mac) - Launches Live Preview
- **Ctrl+Shift+G** (Cmd+Shift+G on Mac) - Generates parser code

For manual installation or CI/CD environments, download Grammar-Kit from the [TeamCity dev builds](https://teamcity.jetbrains.com/guestAuth/app/rest/builds/buildType:IntellijIdeaPlugins_GrammarKit_Build,status:SUCCESS/artifacts/content/GrammarKit*.zip) and install via **Settings** → **Plugins** → **Install from disk**.

For Gradle-based projects, add the Grammar-Kit plugin to your build configuration:

```kotlin
plugins {
    id("org.jetbrains.grammarkit") version "2022.3.2"
}
```

## Project Setup

The recommended project structure separates grammar definitions from generated code to prevent conflicts and maintain clarity. Create a new IntelliJ plugin project with this directory structure:

```
my-language-plugin/
├── src/
│   └── main/
│       ├── java/           # Generated parser code
│       └── resources/
│           └── META-INF/
│               └── plugin.xml
├── grammars/
│   └── MyLanguage.bnf      # Grammar definition
└── build.gradle.kts        # Build configuration
```

The `grammars` directory keeps your `.bnf` files separate from generated Java code. This separation prevents accidental modifications to generated files and simplifies version control.

Configure your `plugin.xml` with the minimal requirements for language support:

```xml
<idea-plugin>
  <id>com.example.mylanguage</id>
  <name>My Language Support</name>
  
  <depends>com.intellij.modules.lang</depends>
  
  <extensions defaultExtensionNs="com.intellij">
    <fileType name="MyLang" 
              implementationClass="com.example.MyLangFileType" 
              fieldName="INSTANCE" 
              extensions="mylang"/>
    <lang.parserDefinition 
              language="MyLang" 
              implementationClass="com.example.MyLangParserDefinition"/>
  </extensions>
</idea-plugin>
```

For Gradle projects, configure the build file with Grammar-Kit support:

```kotlin
plugins {
    id("java")
    id("org.jetbrains.intellij") version "1.17.0"
    id("org.jetbrains.grammarkit") version "2022.3.2"
}

repositories {
    mavenCentral()
}

intellij {
    version.set("2023.3")
}

grammarKit {
    jflexRelease.set("1.9.2")
    grammarKitRelease.set("2022.3.2")
}
```

## First Grammar File

Create a minimal grammar file to verify your setup. In your `grammars` directory, create a file named `hello.bnf`:

```bnf
// hello.bnf
root ::= greeting
greeting ::= 'hello' name
name ::= ID
```

Save the file and observe the syntax highlighting. The editor colors keywords, rules, and tokens differently, confirming Grammar-Kit recognizes your file.

Every BNF grammar needs at least one rule. The example above defines three rules:

- `root` - The entry point for parsing
- `greeting` - A sequence of the literal 'hello' followed by a name
- `name` - References the built-in `ID` token for identifiers

Press **Ctrl+Shift+G** (Cmd+Shift+G on Mac) to generate the parser. Grammar-Kit creates Java classes in your `src/main/java` directory based on the grammar definition.

The editor provides these features for `.bnf` files:

- **Structure View** (Ctrl+F12/Cmd+F12) - Shows all rules in your grammar
- **Live Preview** (Ctrl+Alt+P/Cmd+Alt+P) - Tests parsing with sample input
- **Documentation** (Ctrl+Q/Cmd+J) - Displays help for grammar elements
- **Refactoring** - Extract rules (Ctrl+Alt+M/Cmd+Alt+M) or introduce tokens (Ctrl+Alt+C/Cmd+Alt+C)

## Common Setup Issues

Grammar files must use the `.bnf` extension. Files without this extension do not activate Grammar-Kit features, even with valid BNF syntax.

Never place grammar files in the `src` directory. Generated code overwrites source files in the same location, destroying your grammar definitions. Always use a separate `grammars` folder.

Grammar-Kit requires Java 17 or higher since version 2022.3. If you encounter compatibility errors, verify your Java version and IntelliJ IDEA version (must be 2023.3 or later).

With Grammar-Kit installed and your first grammar file created, continue to the [Quick Start Tutorial](quick-start.md) to build a complete JSON parser and learn core concepts like rules, tokens, and attributes.