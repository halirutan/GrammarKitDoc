# Attribute Reference

This reference documents all attributes available in Grammar-Kit for controlling parser generation, PSI configuration, and parsing behavior. Attributes configure how Grammar-Kit generates code from your BNF grammar and determine the structure and behavior of the generated parser and PSI classes.

## Quick Reference

### Parser Configuration
| Attribute | Scope | Type | Description |
|-----------|-------|------|-------------|
| `parserClass` | Global | String | Fully qualified name of generated parser class |
| `parserPackage` | Global | String | Package for parser-related classes |
| `parserUtilClass` | Global | String | Parser utility class with helper methods |
| `parserImports` | Global | String/Array | Additional imports for generated parser |
| `consumeTokenMethod` | Global | String | Custom method name for token consumption |

### PSI Configuration
| Attribute | Scope | Type | Description |
|-----------|-------|------|-------------|
| `psiPackage` | Global | String | Package for PSI interfaces |
| `psiImplPackage` | Global | String | Package for PSI implementations |
| `psiClassPrefix` | Global | String | Prefix for all PSI class names |
| `psiImplClassSuffix` | Global | String | Suffix for PSI implementation classes |
| `psiImplUtilClass` | Global | String | Utility class for PSI implementations |
| `psiTreeUtilClass` | Global | String | Custom PsiTreeUtil class |
| `psiVisitorName` | Global | String | Name of generated visitor class |

### Code Generation
| Attribute | Scope | Type | Description |
|-----------|-------|------|-------------|
| `generate` | Global | Map | Generation options (psi, visitor, tokens, etc.) |
| `generateTokens` | Global | Boolean | Generate token constants |
| `generatePsi` | Global | Boolean | Generate PSI classes |
| `generateFirstCheck` | Global | Integer | First-set optimization depth |
| `generateTokenAccessors` | Global | Boolean | Generate token accessor methods |
| `classHeader` | Global | String | Header comment for generated classes |

### Rule Modifiers
| Attribute | Scope | Type | Description |
|-----------|-------|------|-------------|
| `pin` | Rule/Pattern | Integer/String | Commit point in sequence |
| `recoverWhile` | Rule/Pattern | String | Error recovery predicate |
| `name` | Rule | String | Override PSI class name |
| `rightAssociative` | Rule | Boolean | Right-to-left parsing for operators |
| `hooks` | Rule | String/Array | Parser hooks for custom logic |

### PSI Hierarchy
| Attribute | Scope | Type | Description |
|-----------|-------|------|-------------|
| `extends` | Global/Rule/Pattern | String | Base class or super rule |
| `implements` | Global/Rule/Pattern | String/Array | Interfaces to implement |
| `mixin` | Rule/Pattern | String | Mixin class for shared functionality |
| `stubClass` | Rule/Pattern | String | Stub class for indexing |
| `methods` | Rule/Pattern | Array/Map | Custom PSI methods |

### Element Types
| Attribute | Scope | Type | Description |
|-----------|-------|------|-------------|
| `elementType` | Rule | String | Share element type between rules |
| `elementTypeClass` | Global | String | Base class for element types |
| `elementTypeFactory` | Global | String | Factory for creating element types |
| `elementTypeHolderClass` | Global | String | Class holding element type constants |
| `elementTypePrefix` | Global | String | Prefix for element type names |
| `fallbackStubElementType` | Global | String | Default stub element type |

### Token Configuration
| Attribute | Scope | Type | Description |
|-----------|-------|------|-------------|
| `tokens` | Global | Array/Map | Token definitions |
| `tokenTypeClass` | Global | String | Base class for token types |
| `tokenTypeFactory` | Global | String | Factory for creating token types |

### Advanced Features
| Attribute | Scope | Type | Description |
|-----------|-------|------|-------------|
| `extraRoot` | Global | Boolean | Generate extra root rule |
| `extendedPin` | Global | Boolean | Extended pin mode |

---

## Parser Configuration

### parserClass
**Scope:** Global  
**Type:** String  
**Default:** Generated based on grammar file name

Specifies the fully qualified name of the generated parser class. This class contains all parsing methods and integrates with IntelliJ's parsing infrastructure. The parser class extends `com.intellij.lang.PsiParser` and implements the parsing logic for your grammar, with each rule in your grammar becoming a method in this class.

```bnf
{
  parserClass="com.example.lang.parser.MyLanguageParser"
}
```

### parserPackage
**Scope:** Global  
**Type:** String  
**Default:** Same package as `parserClass`

Defines the package for parser-related classes. This affects where utility classes and internal parser structures are generated. Use this when you want parser utilities in a specific package structure separate from the main parser class.

```bnf
{
  parserPackage="com.example.lang.parser"
}
```

### parserUtilClass
**Scope:** Global  
**Type:** String  
**Default:** None

Points to a utility class containing helper methods for parsing. These methods can be used in external rules or for complex parsing logic that's easier to express in Java. Common uses include parsing complex literals (strings with escapes, numbers), handling indentation-sensitive languages, custom error recovery logic, and performance-critical parsing sections.

```bnf
{
  parserUtilClass="com.example.lang.parser.MyLanguageParserUtil"
  parserImports="static com.example.lang.parser.MyLanguageParserUtil.*"
}

// Using external rule with utility method
json_string ::= <<parseStringLiteral>>
```

### parserImports
**Scope:** Global  
**Type:** String or Array  
**Default:** None

Adds import statements to the generated parser class. Use this when referencing custom classes in external rules or parser hooks. The imports can be static imports for utility methods or regular imports for types used in the parser.

```bnf
{
  parserImports=[
    "static com.example.lang.parser.MyLanguageParserUtil.*"
    "com.example.lang.psi.MyLanguageTypes"
  ]
}
```

### consumeTokenMethod
**Scope:** Global  
**Type:** String  
**Default:** "consumeToken"

Customizes the method name used for consuming tokens. This advanced feature allows integration with custom parsing frameworks that use different method names for token consumption.

```bnf
{
  consumeTokenMethod="customConsumeToken"
}
```

---

## PSI Configuration

### psiPackage
**Scope:** Global  
**Type:** String  
**Default:** Generated based on parser package

Specifies the package for PSI (Program Structure Interface) interfaces. These interfaces define the API for your language's AST nodes and serve as the public API for your language elements. Plugin features like refactoring, navigation, and analysis work through these interfaces.

```bnf
{
  psiPackage="com.example.lang.psi"
}
```

### psiImplPackage
**Scope:** Global  
**Type:** String  
**Default:** `psiPackage` + ".impl"

Package for PSI implementation classes. These concrete classes implement the PSI interfaces and are typically not used directly by plugin code. The separation between interfaces and implementations allows for cleaner API design and easier maintenance.

```bnf
{
  psiImplPackage="com.example.lang.psi.impl"
}
```

### psiClassPrefix
**Scope:** Global  
**Type:** String  
**Default:** None

Adds a prefix to all generated PSI class names. This helps avoid naming conflicts and creates consistent naming across your language plugin. The prefix applies to both interfaces and implementation classes.

```bnf
{
  psiClassPrefix="MyLang"
}
// Generates: MyLangFile, MyLangFunction, MyLangStatement, etc.
```

### psiImplClassSuffix
**Scope:** Global  
**Type:** String  
**Default:** "Impl"

Suffix for PSI implementation classes. Change this if "Impl" conflicts with your naming conventions or if you prefer a different suffix for implementation classes.

```bnf
{
  psiImplClassSuffix="Implementation"
}
// Generates: FunctionImplementation instead of FunctionImpl
```

### psiImplUtilClass
**Scope:** Global  
**Type:** String  
**Default:** None

Utility class containing helper methods for PSI implementations. Methods from this class can be mixed into PSI classes using the `methods` attribute. This approach keeps generated code clean while allowing complex custom logic to be written in Java.

```bnf
{
  psiImplUtilClass="com.example.lang.psi.impl.MyLangPsiImplUtil"
}

function ::= 'function' ID '(' ')' block {
  methods=[getName setName getPresentation]
}
```

The utility class provides implementations for these methods:
```java
public class MyLangPsiImplUtil {
  public static String getName(MyLangFunction function) {
    return function.getId().getText();
  }
  
  public static ItemPresentation getPresentation(MyLangFunction function) {
    // Return custom presentation for structure view
  }
}
```

### psiTreeUtilClass
**Scope:** Global  
**Type:** String  
**Default:** "com.intellij.psi.util.PsiTreeUtil"

Specifies a custom PsiTreeUtil class. This advanced feature allows you to provide specialized tree traversal methods specific to your language's needs.

```bnf
{
  psiTreeUtilClass="com.example.lang.psi.MyLangPsiTreeUtil"
}
```

### psiVisitorName
**Scope:** Global  
**Type:** String  
**Default:** "Visitor"

Name of the generated visitor class. The visitor pattern enables processing of PSI trees for analysis, code generation, and other traversal-based operations. The generated visitor includes visit methods for each PSI element type.

```bnf
{
  psiVisitorName="MyLangVisitor"
}
// Generates: MyLangVisitor with visitFunction(), visitStatement(), etc.
```

---

## Code Generation

### generate
**Scope:** Global  
**Type:** Map  
**Default:** Various defaults per option

Comprehensive control over code generation. This attribute supersedes individual generateXXX attributes and provides fine-grained control over all aspects of code generation. The map format allows you to specify only the options you want to change from defaults.

```bnf
{
  generate=[
    // PSI generation options
    psi="yes"                    // Generate PSI classes (default: yes)
    psi-classes-map="no"         // IElementType to PSI class map (default: no)
    psi-factory="yes"            // PSI factory methods (default: yes)
    visitor="yes"                // Visitor pattern support (default: yes)
    visitor-value="void"         // Visitor return type (default: void)
    
    // Type generation options
    elements="yes"               // Element type constants (default: yes)
    element-case="upper"         // Element constant case (upper/lower/as-is)
    tokens="yes"                 // Token constants (default: yes)
    token-case="upper"           // Token constant case (upper/lower/as-is)
    token-sets="no"              // TokenSet constants from choices (default: no)
    exact-types="no"             // Use exact types vs IElementType (default: no)
    
    // Parser options
    names="long"                 // Variable naming (short/long/classic)
    first-check="2"              // First-set optimization depth (default: 2)
    java="11"                    // Target Java version (default: 11)
    
    // Other options
    fqn="no"                     // Fully qualified names (default: no)
    token-accessors="no"         // Generate token getters (default: no)
  ]
}
```

Common configurations:
```bnf
// Minimal generation for embedded grammars
generate=[psi="no" tokens="no"]

// Maximum IDE integration
generate=[visitor="yes" token-sets="yes" token-accessors="yes"]

// Modern Java with better debugging
generate=[java="17" names="long"]
```

### generateTokens
**Scope:** Global  
**Type:** Boolean  
**Default:** true

Controls generation of token type constants. Set to false if you define tokens elsewhere, such as when sharing tokens between multiple parsers or when using a custom lexer with its own token definitions.

```bnf
{
  generateTokens=false  // Don't generate token constants
}
```

### generatePsi
**Scope:** Global  
**Type:** Boolean  
**Default:** true

Controls PSI class generation. Disable this for parser-only usage without IDE integration, such as when using Grammar-Kit for standalone parsing tasks or when integrating with a different AST representation.

```bnf
{
  generatePsi=false  // Parser only, no PSI
}
```

### generateFirstCheck
**Scope:** Global  
**Type:** Integer  
**Default:** 2

Depth of first-set analysis for parser optimization. Higher values may improve parser performance by enabling better prediction of which alternatives to try, but they also increase code generation time and parser size. Values between 2 and 4 provide the best balance for most grammars.

```bnf
{
  generateFirstCheck=3  // Deeper lookahead optimization
}
```

### generateTokenAccessors
**Scope:** Global  
**Type:** Boolean  
**Default:** false

Generate getter methods for tokens in PSI classes. This provides convenient access to keywords and operators in your PSI elements, which is useful for refactoring operations, syntax highlighting, and other IDE features that need to work with specific tokens.

```bnf
{
  generateTokenAccessors=true
}

if_statement ::= 'if' '(' expression ')' statement
// Generates: PsiElement getIfKeyword() in IfStatement
```

### classHeader
**Scope:** Global  
**Type:** String  
**Default:** None

Header comment added to all generated classes. Use this for copyright notices, license information, or generation metadata. The header appears at the top of every generated Java file.

```bnf
{
  classHeader="// Copyright (c) 2024 Example Corp\n// Generated by Grammar-Kit"
}
```

---

## Rule Modifiers

### pin
**Scope:** Rule, Pattern  
**Type:** Integer or String  
**Default:** None

Marks a position where the parser commits to the current rule. Once a pinned element is matched, the parser won't backtrack even if later elements fail. This improves error recovery by preventing the parser from trying alternative rules after it has recognized the start of a construct. Pinning strategies include using pin=1 for statements starting with keywords, pin=2 for constructs like assignments (pinning after '='), and pinning on delimiters for lists and blocks.

```bnf
// Pin by position (1-based)
function ::= 'function' ID '(' params? ')' block {pin=1}

// Pin by element name or string
if_statement ::= 'if' '(' expression ')' statement {pin="if"}

// Pattern-based pinning
{
  pin(".*_statement")=1  // Pin first element in all statements
}
```

### recoverWhile
**Scope:** Rule, Pattern  
**Type:** String (rule name or "#auto")  
**Default:** None

Specifies error recovery behavior. The parser consumes tokens while the predicate matches, allowing graceful handling of syntax errors. Use this with pinned rules for robust parsing. Recovery predicates should be negative (using !) and include likely synchronization tokens. The "#auto" value generates a "not in follow set" predicate that works well for well-structured grammars.

```bnf
// Basic recovery
statement ::= assignment | if_statement {
  recoverWhile=statement_recover
}
private statement_recover ::= !(';' | '}' | ID)

// Auto recovery (generates "not in follow set")
method_body ::= '{' statement* '}' {
  pin=1 
  recoverWhile="#auto"
}

// Pattern-based recovery
{
  recoverWhile(".*_item")=item_recover
}
private item_recover ::= !(',' | ')' | ']')
```

### name
**Scope:** Rule  
**Type:** String  
**Default:** Based on rule name

Overrides the generated PSI class name. Use this for better API names or to handle reserved words. This attribute affects only the generated class name, not the rule name used in the grammar.

```bnf
// Rename rule to avoid keyword conflicts
class_ ::= 'class' ID '{' '}' {name="classDeclaration"}

// Better API name
id ::= ID {name="identifier"}
```

### rightAssociative
**Scope:** Rule  
**Type:** Boolean  
**Default:** false

Makes binary expressions parse right-to-left. This is important for operators like assignment or exponentiation where the natural associativity differs from the default left-to-right parsing. Right associativity ensures that expressions like `a^b^c` parse as `a^(b^c)` and `a=b=c` parse as `a=(b=c)`.

```bnf
// Right-associative power operator
power_expr ::= expr '^' expr {rightAssociative=true}
// Parses a^b^c as a^(b^c)

// Assignment is typically right-associative
assign_expr ::= expr '=' expr {rightAssociative=true}
// Parses a=b=c as a=(b=c)
```

### hooks
**Scope:** Rule  
**Type:** String or Array  
**Default:** None

Inserts custom parsing logic at specific points. This advanced feature allows you to add custom behavior during parsing, such as managing symbol tables, handling context-sensitive parsing, or implementing custom error recovery strategies.

```bnf
block ::= '{' statement* '}' {
  hooks=[
    leftBraceHook="handleBlockStart"
    rightBraceHook="handleBlockEnd"
  ]
}
```

---

## PSI Hierarchy

### extends
**Scope:** Global, Rule, Pattern  
**Type:** String  
**Default:** "com.intellij.extapi.psi.ASTWrapperPsiElement" (global)

Defines inheritance for PSI classes. Can reference a class name or another rule. Rules extending the same base are flattened in the AST, which simplifies tree structure and improves performance. This flattening means that intermediate wrapper nodes are eliminated when a rule extends its parent rule.

```bnf
// Global default
{
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
}

// Pattern-based hierarchy
{
  extends(".*_expr")=expr
  extends(".*_literal")=literal_expr
}

// Rule-specific
binary_expr ::= expr operator expr {extends=expr}

// Using fake rules for abstract classes
fake binary_operation ::= expr {
  extends=expr
  methods=[left="expr[0]" right="expr[1]"]
}
add_expr ::= expr '+' expr {extends=binary_operation}
```

AST flattening example:
```bnf
expr ::= add_expr | mul_expr | primary_expr
add_expr ::= expr '+' expr {extends=expr}
// Without extends: expr -> add_expr -> expr '+' expr
// With extends: expr -> expr '+' expr (flattened)
```

### implements
**Scope:** Global, Rule, Pattern  
**Type:** String or Array  
**Default:** None

Specifies interfaces for PSI classes to implement. This enables integration with IntelliJ Platform APIs and allows your language elements to participate in platform features like navigation, refactoring, and search. Common interfaces include PsiNamedElement for named elements and NavigatablePsiElement for elements that can be navigated to.

```bnf
// Single interface
identifier ::= ID {
  implements="com.intellij.psi.PsiNamedElement"
}

// Multiple interfaces
function ::= 'function' ID '(' ')' block {
  implements=[
    "com.intellij.psi.PsiNamedElement"
    "com.intellij.psi.NavigatablePsiElement"
  ]
}

// Pattern-based
{
  implements(".*_declaration")="com.example.lang.psi.Declaration"
}
```

### mixin
**Scope:** Rule, Pattern  
**Type:** String  
**Default:** None

Specifies a base class providing shared implementation. The mixin class must extend the class specified in `extends` and allows you to add custom behavior to generated PSI classes. This is useful when you need complex logic that's difficult to express in utility methods or when you want to override framework methods.

```bnf
function ::= 'function' ID '(' params? ')' block {
  mixin="com.example.lang.psi.impl.FunctionMixin"
  implements="com.example.lang.psi.NamedElement"
  methods=[getName setName]
}
```

Mixin class example:
```java
public abstract class FunctionMixin extends ASTWrapperPsiElement implements NamedElement {
  public FunctionMixin(ASTNode node) { super(node); }
  
  public String getName() {
    PsiElement id = findChildByType(ID);
    return id != null ? id.getText() : null;
  }
}
```

### stubClass
**Scope:** Rule, Pattern  
**Type:** String  
**Default:** None

Enables stub support for efficient indexing. The PSI class must extend `StubBasedPsiElementBase` to use stubs. Stubs improve performance by storing essential information without parsing full file content, which is crucial for features like Find Usages and Go to Symbol that need to work across large codebases.

```bnf
class_decl ::= 'class' ID '{' member* '}' {
  extends="com.intellij.extapi.psi.StubBasedPsiElementBase<?>"
  stubClass="com.example.lang.stubs.ClassStub"
  implements="com.example.lang.psi.MyLangClass"
}
```

### methods
**Scope:** Rule, Pattern  
**Type:** Array or Map  
**Default:** None

Defines custom methods in PSI classes. Can be method names (delegated to psiImplUtilClass) or path-based accessors. Path-based accessors provide convenient navigation through the PSI tree using a simple syntax: simple names for direct children, `/` for path separation, `[n]` for array indexing (0-based, negative from end), and names without paths for methods from the utility class.

```bnf
// Simple method names (implemented in utility class)
variable ::= 'var' ID '=' expr {
  methods=[getName setName getNameIdentifier]
}

// Path-based accessors
function ::= 'function' ID '(' params? ')' return_type? block {
  methods=[
    name="ID"                    // Returns PsiElement (the ID)
    parameterList="params"       // Returns Params PSI element
    parameters="params/param"    // Returns List<Param>
    returnType="return_type"     // Returns ReturnType (nullable)
  ]
}

// Array accessors
binary_expr ::= expr op expr {
  methods=[
    left="expr[0]"              // First expression
    operator="op"               // Operator element
    right="expr[1]"             // Second expression
    operands="expr"             // All expressions (List)
  ]
}

// Renaming generated methods
list ::= '[' (item (',' item)*)? ']' {
  methods=[
    elements="item"             // Rename getItemList() to getElementList()
    item=""                     // Suppress getItemList() completely
  ]
}
```

---

## Element Types

### elementType
**Scope:** Rule  
**Type:** String  
**Default:** None

Shares element type between rules. Rules with the same elementType produce the same node type in the AST, which is useful when multiple grammar rules represent the same logical construct. This is particularly helpful with fake rules for creating abstract syntax representations.

```bnf
// Both rules create the same AST node type
string ::= DOUBLE_QUOTED_STRING {elementType=stringLiteral}
string2 ::= SINGLE_QUOTED_STRING {elementType=stringLiteral}

// Useful with fake rules
fake binary_expr ::= expr op expr
add_expr ::= expr '+' expr {elementType=binary_expr}
mul_expr ::= expr '*' expr {elementType=binary_expr}
```

### elementTypeClass
**Scope:** Global  
**Type:** String  
**Default:** "com.intellij.psi.tree.IElementType"

Base class for element types. Customize this when you need special element type behavior, such as custom debugging representations or integration with language-specific features.

```bnf
{
  elementTypeClass="com.example.lang.psi.MyLangElementType"
}
```

### elementTypeFactory
**Scope:** Global  
**Type:** String  
**Default:** None

Factory method for creating element types. This provides an alternative to using a custom elementTypeClass when you need centralized control over element type creation or want to reuse existing element type instances.

```bnf
{
  elementTypeFactory="com.example.lang.psi.MyLangElementTypeFactory.create"
}
```

### elementTypeHolderClass
**Scope:** Global  
**Type:** String  
**Default:** Generated based on package

Class containing all element type constants. Reference this class in your ParserDefinition to access the generated element types for your language. The class contains static fields for each rule and token in your grammar.

```bnf
{
  elementTypeHolderClass="com.example.lang.psi.MyLangTypes"
}
// Generates: MyLangTypes.FUNCTION, MyLangTypes.STATEMENT, etc.
```

### elementTypePrefix
**Scope:** Global  
**Type:** String  
**Default:** None

Prefix for element type constant names. Use this to ensure unique naming when integrating with other languages or to follow specific naming conventions in your codebase.

```bnf
{
  elementTypePrefix="MY_LANG_"
}
// Generates: MY_LANG_FUNCTION, MY_LANG_STATEMENT, etc.
```

### fallbackStubElementType
**Scope:** Global  
**Type:** String  
**Default:** None

Default stub element type for error recovery in stub building. This advanced feature ensures robust indexing by providing a fallback when the parser encounters malformed code during stub building.

```bnf
{
  fallbackStubElementType="com.example.lang.stubs.ErrorStub.TYPE"
}
```

---

## Token Configuration

### tokens
**Scope:** Global  
**Type:** Array or Map  
**Default:** None

Defines tokens for the grammar. Supports literal tokens and regular expression patterns. Token patterns include literal strings for direct matches and regexp patterns for more complex tokens. Token names in lowercase are typically skipped by the parser, and order matters for overlapping patterns - place more specific patterns before general ones.

```bnf
{
  tokens=[
    // Literal tokens
    PLUS='+'
    MINUS='-'
    LPAREN='('
    RPAREN=')'
    
    // Keywords
    IF='if'
    ELSE='else'
    WHILE='while'
    
    // Pattern tokens with regular expressions
    ID='regexp:[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER='regexp:\d+(\.\d*)?'
    STRING='regexp:"([^"\\]|\\.)*"'
    
    // Comments and whitespace (usually skipped)
    space='regexp:\s+'
    line_comment='regexp://.*'
    block_comment='regexp:/\*(.|\n)*\*/'
  ]
}
```

### tokenTypeClass
**Scope:** Global  
**Type:** String  
**Default:** "com.intellij.psi.tree.IElementType"

Base class for token types. Customize this when you need special token behavior, such as custom token categories for syntax highlighting or special handling in the lexer.

```bnf
{
  tokenTypeClass="com.example.lang.psi.MyLangTokenType"
}
```

### tokenTypeFactory
**Scope:** Global  
**Type:** String  
**Default:** None

Factory method for creating token types. This provides an alternative to using a custom tokenTypeClass when you need centralized control over token type creation or want to implement token type caching.

```bnf
{
  tokenTypeFactory="com.example.lang.psi.MyLangTokenTypeFactory.create"
}
```

---

## Advanced Features

### extraRoot
**Scope:** Global  
**Type:** Boolean  
**Default:** false

Generates an additional root rule that matches any single rule. Useful for fragment parsing or testing.

```bnf
{
  extraRoot=true
}
// Generates: root ::= rule1 | rule2 | ... | ruleN
```

### extendedPin
**Scope:** Global  
**Type:** Boolean  
**Default:** false

Enables extended pin mode with more aggressive error recovery. Experimental feature for complex grammars.

```bnf
{
  extendedPin=true
}
```

---

## Practical Examples

### Expression Parser with Precedence
```bnf
{
  extends(".*_expr")=expr
}

expr ::= assign_expr
  | or_expr
  | and_expr
  | equality_expr
  | relational_expr
  | additive_expr
  | multiplicative_expr
  | unary_expr
  | postfix_expr
  | primary_expr

// Binary expressions with precedence
fake binary_expr ::= expr {
  methods=[
    left="expr[0]"
    operator="operator"
    right="expr[1]"
  ]
}

multiplicative_expr ::= expr mul_op expr {extends=binary_expr}
additive_expr ::= expr add_op expr {extends=binary_expr}
private mul_op ::= '*' | '/'
private add_op ::= '+' | '-'
```

### Robust Statement Parsing
```bnf
statement ::= if_stmt | while_stmt | block_stmt | expr_stmt {
  recoverWhile=statement_recover
}
private statement_recover ::= !('}' | ';' | 'if' | 'while')

if_stmt ::= 'if' '(' expr ')' statement else_clause? {
  pin=1
  methods=[
    condition="expr"
    thenBranch="statement"
    elseBranch="else_clause/statement"
  ]
}

block_stmt ::= '{' statement* '}' {
  pin=1
  recoverWhile="#auto"
}
```

### List Parsing with Recovery
```bnf
// Comma-separated list with recovery
arg_list ::= '(' [ arg (',' arg)* ] ')' {pin=1}
private arg ::= expr {pin=1 recoverWhile=arg_recover}
private arg_recover ::= !(',' | ')')

// Generic list pattern
{
  pin(".*_list_item")=1
  recoverWhile(".*_list_item")=list_item_recover
}
private list_item_recover ::= !(',' | ';' | ')' | ']' | '}')
```

### PSI with References
```bnf
{
  psiImplUtilClass="com.example.lang.psi.impl.PsiImplUtil"
}

var_ref ::= ID {
  methods=[
    getReference
    getName
    setName
  ]
  implements="com.intellij.psi.PsiNamedElement"
}

// In PsiImplUtil:
// public static PsiReference getReference(VarRef element) {
//   return new MyReference(element);
// }
```

## Common Attribute Combinations

### Minimal Grammar
```bnf
{
  parserClass="com.example.SimpleParser"
  tokens=[
    ID='regexp:\w+'
    space='regexp:\s+'
  ]
}
```

### Full IDE Integration
```bnf
{
  parserClass="com.example.lang.parser.MyLangParser"
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
  
  psiClassPrefix="MyLang"
  psiImplPackage="com.example.lang.psi.impl"
  psiPackage="com.example.lang.psi"
  psiImplUtilClass="com.example.lang.psi.impl.MyLangPsiImplUtil"
  
  elementTypeHolderClass="com.example.lang.psi.MyLangTypes"
  elementTypeClass="com.example.lang.psi.MyLangElementType"
  tokenTypeClass="com.example.lang.psi.MyLangTokenType"
  
  generate=[psi="yes" visitor="yes" token-accessors="yes"]
}
```

### Performance-Optimized
```bnf
{
  generateFirstCheck=3
  generate=[first-check="3" names="short" java="17"]
  
  // Stub support for key elements
  extends(".*_declaration")="com.intellij.extapi.psi.StubBasedPsiElementBase<?>"
  stubClass(".*_declaration")="com.example.lang.stubs.$1Stub"
}
```