# Examples: Installation and Setup

## Scope Information
This provides examples for section 1.3: Installation and Setup

---

## Minimal Working Grammar File

A complete `.bnf` grammar for a simple key-value configuration language.
This is the first file a reader would create after installing Grammar-Kit.

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

- First rule becomes parse root
- `private` rules produce no PSI nodes
- `tokens` block defines lexer tokens
- `pin=2` enables error recovery at `=`
- `recoverWhile` skips garbage input
- Attributes block `{ }` goes before rules

### What to notice

The grammar has three sections:

1. **Header attributes** (`{ ... }`) — configures code generation output locations
2. **Token definitions** (`tokens=[...]`) — maps token names to string literals or regex patterns
3. **Rules** (`rule ::= expression`) — defines the grammar structure

### How to test it

After saving this file as `config.bnf`:

1. The file should show a BNF icon in the editor tab
2. Press <kbd>Ctrl+Alt+P</kbd> / <kbd>Cmd+Alt+P</kbd> to open Live Preview
3. Type sample input in the preview pane to see the parse tree
4. Press <kbd>Ctrl+Shift+G</kbd> / <kbd>Cmd+Shift+G</kbd> to generate parser code

---

## Even Simpler: Bare-Minimum Grammar

The smallest valid grammar — no header attributes at all.
Useful for prototyping in Live Preview before adding generation settings.

```bnf
// minimal.bnf — Works in Live Preview without any attributes.
root ::= 'hello' 'world'
```

- No attributes block required
- Defaults used for all settings
- Works immediately in Live Preview
- Not ready for code generation (no output paths)

---

## Basic Project Structure

Recommended directory layout for an IntelliJ language plugin using Grammar-Kit.
Based on Grammar-Kit's own project structure and the HOWTO guidance that
handwritten and generated classes must be in separate source roots.

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

- `src/main/java/` and `src/main/gen/` are separate source roots
- Generated code goes in `gen/` — never edit these files
- Grammar `.bnf` file lives in resources or source
- `.flex` file lives alongside handwritten code
- `gen/` directory should be in `.gitignore` (or committed, team preference)

### Marking `gen/` as a generated source root

In `build.gradle.kts`:

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

- Two java source directories declared
- IDEA marks `gen/` with special icon
- Generated files excluded from refactoring

### Alternative: classic layout

Some projects use a flat layout closer to Grammar-Kit's own structure:

```
my-language-plugin/
├── src/                ← Handwritten code
├── gen/                ← Generated code
├── resources/          ← plugin.xml, .bnf files
├── tests/              ← Test code
└── testData/           ← Test fixtures
```

- Matches Grammar-Kit's own project layout
- `gen/` default set by `grammar.kit.gen.dir` property
- Either layout works; be consistent

---

## plugin.xml Configuration

The essential registrations for a language plugin that uses Grammar-Kit.
Adapted from Grammar-Kit's own `plugin.xml`.

```xml
<idea-plugin>
  <id>com.example.config-language</id>
  <name>Config Language Support</name>
  <vendor>Your Name</vendor>
  <description>Support for .config files.</description>

  <!-- Required: core language support module -->
  <depends>com.intellij.modules.lang</depends>

  <extensions defaultExtensionNs="com.intellij">

    <!-- 1. Register the file type for .config files -->
    <fileType
        name="Config"
        implementationClass="com.example.config.ConfigFileType"
        fieldName="INSTANCE"
        extensions="config"
        language="Config"/>

    <!-- 2. Connect parser and lexer to the language -->
    <lang.parserDefinition
        language="Config"
        implementationClass="com.example.config.ConfigParserDefinition"/>

    <!-- 3. Syntax highlighting -->
    <lang.syntaxHighlighterFactory
        language="Config"
        implementationClass="com.example.config.ConfigSyntaxHighlighterFactory"/>

  </extensions>
</idea-plugin>
```

- `com.intellij.modules.lang` is always required
- `language=` must match your Language ID exactly
- `fieldName="INSTANCE"` points to the static singleton
- `extensions="config"` maps `.config` files to this type
- Three registrations are the minimum: fileType, parserDefinition, syntaxHighlighter

### What each registration does

| Registration | Purpose |
|---|---|
| `fileType` | Associates file extension with your language |
| `lang.parserDefinition` | Provides parser, lexer, and PSI element factory |
| `lang.syntaxHighlighterFactory` | Provides token-to-color mapping |

---

## Supporting Java Classes

### Language singleton

```java
package com.example.config;

import com.intellij.lang.Language;

public final class ConfigLanguage extends Language {
    public static final ConfigLanguage INSTANCE = new ConfigLanguage();

    private ConfigLanguage() {
        super("Config");  // Must match language= in plugin.xml
    }
}
```

- Language ID `"Config"` ties everything together
- Singleton pattern via `INSTANCE` field
- Constructor is private

### FileType class

Based on Grammar-Kit's `BnfFileType.java`:

```java
package com.example.config;

import com.intellij.openapi.fileTypes.LanguageFileType;
import javax.swing.*;
import org.jetbrains.annotations.NotNull;

public final class ConfigFileType extends LanguageFileType {
    public static final ConfigFileType INSTANCE = new ConfigFileType();

    private ConfigFileType() {
        super(ConfigLanguage.INSTANCE);
    }

    @Override public @NotNull String getName() { return "Config"; }

    @Override public @NotNull String getDescription() { return "Config file"; }

    @Override public @NotNull String getDefaultExtension() { return "config"; }

    @Override public Icon getIcon() { return null; }  // Add icon later
}
```

- Extends `LanguageFileType`, links to Language
- `getName()` must match `name=` in plugin.xml fileType
- `getDefaultExtension()` returns without the dot

### ParserDefinition class

Based on Grammar-Kit's `BnfParserDefinition.java`:

```java
package com.example.config;

import com.intellij.lang.*;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.project.Project;
import com.intellij.psi.*;
import com.intellij.psi.tree.*;
import com.example.config.parser.ConfigParser;   // ← Generated
import com.example.config.psi.ConfigTypes;        // ← Generated
import org.jetbrains.annotations.NotNull;

public class ConfigParserDefinition implements ParserDefinition {

    public static final IFileElementType FILE =
        new IFileElementType(ConfigLanguage.INSTANCE);

    @Override
    public @NotNull Lexer createLexer(Project project) {
        return new ConfigLexer();  // Your JFlex-generated lexer
    }

    @Override
    public @NotNull PsiParser createParser(Project project) {
        return new ConfigParser();  // Generated by Grammar-Kit
    }

    @Override
    public @NotNull IFileElementType getFileNodeType() {
        return FILE;
    }

    @Override
    public @NotNull TokenSet getCommentTokens() {
        return TokenSet.create(ConfigTypes.COMMENT);
    }

    @Override
    public @NotNull TokenSet getWhitespaceTokens() {
        return TokenSet.WHITE_SPACE;
    }

    @Override
    public @NotNull TokenSet getStringLiteralElements() {
        return TokenSet.create(ConfigTypes.STRING);
    }

    @Override
    public @NotNull PsiElement createElement(ASTNode node) {
        return ConfigTypes.Factory.createElement(node);  // Generated factory
    }

    @Override
    public @NotNull PsiFile createFile(@NotNull FileViewProvider viewProvider) {
        return new ConfigFile(viewProvider);  // Your PsiFile subclass
    }
}
```

- `createParser()` returns the Grammar-Kit generated parser
- `createLexer()` returns your JFlex-generated lexer
- `createElement()` delegates to generated `Factory` class
- Token sets define what the parser skips automatically

---

## Common Patterns

### Token block with regex patterns

```bnf
{
  tokens=[
    // Whitespace and comments (usually skipped by parser)
    space   = 'regexp:\s+'
    comment = 'regexp://.*'

    // Literals
    number  = 'regexp:\d+(\.\d*)?'
    string  = "regexp:\"([^\"\\]|\\.)*\""
    id      = 'regexp:\p{Alpha}\w*'

    // Fixed-text tokens (keywords and punctuation)
    SEMI    = ';'
    COMMA   = ','
    LBRACE  = '{'
    RBRACE  = '}'
    EQ      = '='
  ]
}
```

- Regex tokens use `'regexp:...'` syntax
- Fixed tokens map name to literal text
- `space` token used as whitespace in Live Preview
- Names become `IElementType` constants

### Referencing tokens by value

```bnf
// Preferred: use quoted values for readability
property ::= id '=' value ';'

// Also valid: use token names
property ::= id EQ value SEMI
```

- Quoted values preferred for readability
- Token names resolve ambiguity
- Both forms reference the same token

---

## Anti-patterns

### Missing source root separation

```
my-plugin/
├── src/
│   └── com/example/
│       ├── MyParser.java          ← GENERATED
│       ├── MyParserDefinition.java ← HANDWRITTEN
│       └── psi/
│           ├── MyTypes.java       ← GENERATED
│           └── MyPsiUtil.java     ← HANDWRITTEN
```

- **Wrong**: generated and handwritten code mixed
- Regeneration may overwrite handwritten files
- Refactoring tools may modify generated code
- **Fix**: use separate `src/` and `gen/` roots

### Grammar without generation attributes

```bnf
// DON'T: no attributes means defaults like "generated.GeneratedParser"
root ::= item *
item ::= id '=' value
value ::= number | string
```

- Works in Live Preview only
- Generated code uses default package `generated`
- No control over output class names
- **Fix**: always add `parserClass`, `psiPackage`, `elementTypeHolderClass`

### Wrong language ID mismatch

```xml
<!-- In plugin.xml -->
<fileType language="config" .../>              <!-- lowercase -->
<lang.parserDefinition language="Config" .../>  <!-- capitalized -->
```

```java
// In Language class
super("Config");  // capitalized
```

- **Wrong**: `"config"` ≠ `"Config"`
- Language ID is case-sensitive
- Parser won't connect to file type
- **Fix**: use identical string everywhere

---

## Related Examples
- For grammar syntax details → See Section 2.1 (Grammar Syntax)
- For error recovery (pin/recoverWhile) → See Section 2.4 (Error Recovery)
- For expression parsing → See Section 2.3 (Expression Parsing)
- For JFlex lexer development → See Section 3.3 (Lexer Development)
- For Gradle build setup → See Section 4.2.1 (Build Integration)
- For Live Preview workflow → See Section 2.5 (Live Preview)
