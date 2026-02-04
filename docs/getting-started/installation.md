# Installation and Setup

This page covers installing GrammarKit and configuring a language plugin project. You'll set up the plugin, create a project structure, and write your first grammar file.

## Prerequisites

GrammarKit requires Java 17 or higher and IntelliJ IDEA 2023.3 or newer (build 233+). Either Community or Ultimate Edition works. Basic familiarity with IntelliJ IDEA plugin development helps but isn't required.

GrammarKit versions follow IntelliJ IDEA releases. For example, GrammarKit 2023.3 is compatible with IntelliJ IDEA 2023.3 and later versions.

## Installing Grammar-Kit

Install Grammar-Kit through the IntelliJ IDEA plugin marketplace:

1. Open IntelliJ IDEA
2. Navigate to **File → Settings** (or **IntelliJ IDEA → Preferences** on macOS)
3. Select **Plugins** in the left sidebar
4. Click the **Marketplace** tab
5. Search for "Grammar-Kit"
6. Click **Install** on the Grammar-Kit plugin by JetBrains
7. Restart IntelliJ IDEA when prompted

After installation, verify GrammarKit works by creating a test BNF file. Right-click any directory in your project, select **New → File**, and name it `test.bnf`. The file should open with syntax highlighting and display the BNF file icon in the project view.

Test the keyboard shortcuts by opening the `.bnf` file and pressing **Ctrl+Alt+P** (Cmd+Alt+P on macOS) to open Live Preview, or **Ctrl+Shift+G** (Cmd+Shift+G on macOS) to open the parser generation dialog.

For development builds or specific versions, download the plugin ZIP from the [JetBrains TeamCity](https://teamcity.jetbrains.com/guestAuth/app/rest/builds/buildType:IntellijIdeaPlugins_GrammarKit_Build,status:SUCCESS/artifacts/content/GrammarKit*.zip) and install via **Settings → Plugins → ⚙️ → Install Plugin from Disk**.

## Project Setup

Create a new IntelliJ Platform Plugin project through **File → New → Project → IntelliJ Platform Plugin**. Configure the project with IntelliJ IDEA IU-233.x or newer as the Project SDK, Java 17 as the language, and Gradle as the build system.

Update your `build.gradle.kts` file:
   ```kotlin
   plugins {
       id("java")
       id("org.jetbrains.kotlin.jvm") version "1.9.0"
       id("org.jetbrains.intellij") version "1.16.0"
   }

   group = "com.example"
   version = "1.0-SNAPSHOT"

   repositories {
       mavenCentral()
   }

   intellij {
       version.set("2023.3")
       type.set("IC") // or "IU" for Ultimate
       plugins.set(listOf("com.intellij.java")) // Optional, for Java support
   }

   sourceSets {
       main {
           java {
               srcDirs("src/main/java", "src/main/gen")
           }
       }
   }

   tasks {
       patchPluginXml {
           sinceBuild.set("233")
           untilBuild.set("241.*")
       }
   }
   ```

Organize your project to separate generated code from hand-written code:

```
my-language-plugin/
├── src/
│   ├── main/
│   │   ├── java/              # Hand-written code
│   │   │   └── com/example/
│   │   │       ├── MyLanguage.java
│   │   │       ├── MyParserDefinition.java
│   │   │       └── grammar/
│   │   │           └── MyLanguage.bnf
│   │   ├── gen/               # Generated code (excluded from VCS)
│   │   │   └── com/example/
│   │   │       ├── MyParser.java
│   │   │       └── psi/
│   │   │           ├── MyTypes.java
│   │   │           └── impl/
│   │   └── resources/
│   │       └── META-INF/
│   │           └── plugin.xml
│   └── test/
│       └── java/
│           └── com/example/
│               └── MyParsingTest.java
├── build.gradle.kts
└── .gitignore
```

Add generated directories to `.gitignore`:

```gitignore
# Generated parser/PSI code
src/main/gen/
src/test/gen/

# IntelliJ
.idea/
*.iml
out/

# Gradle
.gradle/
build/
```

Update your `plugin.xml` to include required dependencies:

```xml
<idea-plugin>
    <id>com.example.mylanguage</id>
    <name>My Language Support</name>
    <vendor>Your Name</vendor>
    
    <!-- Required dependency for language support -->
    <depends>com.intellij.modules.lang</depends>
    
    <!-- Optional: For Java interop features -->
    <depends optional="true">com.intellij.java</depends>
    
    <extensions defaultExtensionNs="com.intellij">
        <!-- Language extensions will go here -->
    </extensions>
</idea-plugin>
```

## Creating Your First Grammar

Create a BNF grammar file by right-clicking on `src/main/java/com/example/grammar/`, selecting **New → File**, and naming it `MyLanguage.bnf`. Add this basic grammar structure:

```bnf
{
  // Parser class configuration
  parserClass="com.example.MyParser"
  parserUtilClass="com.example.MyParserUtil"
  
  // PSI class configuration
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
  
  psiClassPrefix="My"
  psiImplClassSuffix="Impl"
  psiPackage="com.example.psi"
  psiImplPackage="com.example.psi.impl"
  
  // Element type configuration
  elementTypeHolderClass="com.example.psi.MyTypes"
  elementTypeClass="com.example.psi.MyElementType"
  tokenTypeClass="com.example.psi.MyTokenType"
  
  // Utility configuration
  psiImplUtilClass="com.example.psi.impl.MyPsiImplUtil"
  
  // Tokens
  tokens=[
    LBRACE='{'
    RBRACE='}'
    SEMI=';'
    EQ='='
    
    space='regexp:\s+'
    comment='regexp://.*'
    number='regexp:\d+'
    id='regexp:\p{Alpha}\w*'
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"
  ]
}

// Grammar rules
root ::= item*

private item ::= !<<eof>> statement {pin=1}

statement ::= assignment | block {pin=1}

assignment ::= id '=' expression ';' {pin=2}

block ::= '{' item* '}' {pin=1}

expression ::= number | string | id
```

The grammar file contains three main sections: header attributes (in `{ }`) that configure code generation, token definitions that define lexical elements, and grammar rules that define the language structure.

When editing `.bnf` files, GrammarKit provides syntax highlighting, structure view (Ctrl+F12 or Cmd+F12), code completion (Ctrl+Space), error detection, and quick documentation (Ctrl+Q or Cmd+J on attributes).

Test your grammar using Live Preview:

1. Open your `.bnf` file
2. Press **Ctrl+Alt+P** (Cmd+Alt+P on macOS)
3. Type sample code in the preview editor:
   ```
   x = 42;
   {
     name = "test";
     count = 100;
   }
   ```
4. The structure tree shows how your grammar parses the input
5. Use **Ctrl+Alt+F7** (Cmd+Alt+F7) to highlight the current rule

Live Preview uses a simplified lexer based on your token definitions. The actual lexer behavior may differ, especially for complex tokens or whitespace handling.

With GrammarKit installed and your first grammar created, you can generate the parser (Ctrl+Shift+G), create a lexer (right-click the `.bnf` file → Generate JFlex Lexer), implement ParserDefinition to wire your parser into IntelliJ, and add IDE features like syntax highlighting and code completion. Continue with the [Quick Start Tutorial](quick-start.md) for a complete walkthrough.

## Troubleshooting

**BNF files not recognized**: Ensure the plugin is enabled in Settings → Plugins → Installed. Grammar-Kit should be checked. If the problem persists, invalidate caches through File → Invalidate Caches and Restart.

**Keyboard shortcuts not working**: Check for conflicts in Settings → Keymap by searching for "Grammar". On macOS, use Cmd instead of Ctrl for all shortcuts.

**Parser generation fails**: Verify Java 17+ is configured as Project SDK, check that output directories exist and are writable, and look for error messages in the Event Log (bottom right corner).

For additional help, see the [Grammar-Kit GitHub](https://github.com/JetBrains/Grammar-Kit) repository, join the [IntelliJ Platform Slack](https://plugins.jetbrains.com/slack) #grammar-kit channel, or report issues on the [Grammar-Kit issue tracker](https://github.com/JetBrains/Grammar-Kit/issues).