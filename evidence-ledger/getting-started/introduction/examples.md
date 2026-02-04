# Examples: Introduction to GrammarKit

## Scope Information
This provides examples for section 1.1: Introduction to GrammarKit

## Basic BNF Grammar Support
```bnf
// Simple calculator grammar
root ::= statement*
statement ::= assignment | expression
assignment ::= ID '=' expression
expression ::= NUMBER | ID
```
- BNF rules define language structure
- ::= means "is defined as"
- | means choice (OR)
- * means zero or more

## What Parser Generation Produces
```java
// Generated parser method (conceptual)
public static boolean expression(PsiBuilder b, int l) {
  if (!recursion_guard_(b, l, "expression")) return false;
  boolean r;
  r = consumeToken(b, NUMBER);
  if (!r) r = consumeToken(b, ID);
  return r;
}
```
- Recursive descent parser methods
- PsiBuilder for AST construction
- Token consumption logic
- Error recovery support

## IntelliJ Platform Language Support
```bnf
{
  parserClass="com.example.MyParser"
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
  psiClassPrefix="My"
  psiImplClassSuffix="Impl"
}
```
- Generates PSI (Program Structure Interface)
- Integrates with IntelliJ Platform
- Creates language plugin components
- Enables IDE features automatically

## Custom Language Plugin Example
```bnf
// Domain-specific language for configs
config ::= section*
section ::= '[' ID ']' property*
property ::= ID '=' value
value ::= STRING | NUMBER | BOOLEAN
```
- Define your language structure
- Generate parser and PSI
- Add to language plugin
- Get syntax highlighting free

## DSL Support Example
```bnf
// Simple expression DSL
expr ::= term ('+' term)*
term ::= factor ('*' factor)*
factor ::= NUMBER | '(' expr ')'
```
- Mathematical expression parsing
- Operator precedence handling
- Nested expression support
- Common DSL pattern

## File Format Parser Example
```bnf
// Simplified JSON-like format
root ::= value
value ::= object | array | STRING | NUMBER
object ::= '{' [property (',' property)*] '}'
property ::= STRING ':' value
array ::= '[' [value (',' value)*] ']'
```
- Parse structured data files
- Generate type-safe AST
- Enable file validation
- Support IDE navigation

## Common Patterns
### Optional Elements
```bnf
statement ::= 'if' expr 'then' expr ['else' expr]
```
- Square brackets for optional
- Question mark alternative: expr?

### Repetition
```bnf
program ::= statement+     // one or more
params ::= ID (',' ID)*    // zero or more
```
- Plus for one-or-more
- Star for zero-or-more

### Grouping
```bnf
expr ::= term (('+' | '-') term)*
```
- Parentheses group elements
- Combine with repetition operators

## Anti-patterns
### Missing Root Rule
```bnf
// BAD: No entry point
statement ::= assignment | expression
expression ::= NUMBER
```
- Always define root rule
- Parser needs starting point

### Left Recursion
```bnf
// BAD: Infinite recursion
expr ::= expr '+' term | term
```
- Causes parser stack overflow
- Use iteration instead

### Ambiguous Grammar
```bnf
// BAD: Multiple parse paths
expr ::= ID | ID '(' ')'
```
- Parser can't decide path
- Make grammar deterministic

## Prerequisites Comments
```bnf
// Prerequisites for using GrammarKit:
// - IntelliJ IDEA installed
// - Basic Java knowledge (generated code is Java)
// - Understanding of BNF notation
// - Familiarity with parsing concepts helpful

{
  // Java 17+ required since 2022.3
  parserClass="com.example.MyParser"
}
```

## Related Examples
- For installation → See Section 1.2
- For grammar syntax → See Section 2.1
- For attributes → See Section 2.2
- For parser generation → See Section 3.1