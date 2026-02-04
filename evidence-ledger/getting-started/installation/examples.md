# Examples: Installation and Setup

## Scope Information
This provides examples for section 1.2: Installation and Setup

## Minimal Working Grammar
```bnf
// hello.bnf
root ::= greeting
greeting ::= 'hello' name
name ::= ID
```
- Verifies Grammar-Kit installation
- Shows syntax highlighting
- Tests parser generation

## Basic Project Structure
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
- Standard plugin layout
- Separate grammar folder
- Generated code location

## Essential plugin.xml Configuration
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
- Minimal language registration
- File type association
- Parser definition link

## Simple build.gradle.kts
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
    // path to BNF grammar
    jflexRelease.set("1.9.2")
    grammarKitRelease.set("2022.3.2")
}
```
- Grammar-Kit plugin setup
- IntelliJ plugin configuration
- Version specifications

## Common Patterns
### First Grammar File
```bnf
{
  parserClass="com.example.MyParser"
}

root ::= element+
element ::= 'keyword' | ID | NUMBER
```
- Parser class specification
- Simple rule definition

### Verify Installation
```bnf
// test.bnf - Type this and check:
// 1. Syntax highlighting appears
// 2. Ctrl+F12 shows structure
// 3. Ctrl+Shift+G generates parser
root ::= 'test'
```
- Quick installation check
- Keyboard shortcut test

## Anti-patterns
### Missing File Extension
```bnf
// Wrong: mygrammar (no extension)
// Right: mygrammar.bnf
root ::= element
```
- Must use .bnf extension

### Wrong Project Structure
```
// Wrong: Grammar in src/main/java/
src/main/java/grammar.bnf

// Right: Separate grammar folder
grammars/grammar.bnf
```
- Keep grammars separate
- Avoid source conflicts

## Related Examples
- For grammar syntax → See Section 2.1
- For attributes → See Section 2.2
- For parser generation → See Section 3.1
- For complex grammars → See Section 1.3