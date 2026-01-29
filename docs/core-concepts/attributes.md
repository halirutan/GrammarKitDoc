# Grammar-Kit Attributes

Grammar-Kit uses attributes to control parser generation, configure PSI (Program Structure Interface) classes, define error recovery strategies, and customize parser behavior. Attributes are key-value pairs enclosed in curly braces `{}` that appear at two levels: global attributes apply to the entire grammar file and control parser and PSI generation, while rule attributes apply to specific rules and control their parsing behavior and PSI representation. You can specify attributes directly on rules or apply them to multiple rules using pattern matching.

## Global Attributes

Global attributes appear at the beginning of your grammar file and configure the overall code generation process:

```bnf
{
  // Parser configuration
  parserClass="com.example.lang.parser.MyLanguageParser"
  parserPackage="com.example.lang.parser"
  parserUtilClass="com.example.lang.parser.MyLanguageParserUtil"
  parserImports="static com.example.lang.parser.MyLanguageParserUtil.*"
  
  // PSI configuration
  psiPackage="com.example.lang.psi"
  psiImplPackage="com.example.lang.psi.impl"
  psiClassPrefix="MyLang"
  psiImplClassSuffix="Impl"
  psiImplUtilClass="com.example.lang.psi.impl.MyLangPsiImplUtil"
  
  // Element type configuration
  elementTypeHolderClass="com.example.lang.psi.MyLangTypes"
  elementTypeClass="com.example.lang.psi.MyLangElementType"
  elementTypePrefix="MY_LANG_"
  tokenTypeClass="com.example.lang.psi.MyLangTokenType"
  
  // Generation options
  generate=[java="8" names="long" visitor="no" psi="yes"]
  generateTokens=true
  generateFirstCheck=2
  
  // Token definitions
  tokens=[
    LBRACE='{'
    RBRACE='}'
    LPAREN='('
    RPAREN=')'
    SEMICOLON=';'
    EQ='='
    
    // Regular expression tokens
    ID='regexp:\w+'
    NUMBER='regexp:\d+'
    STRING="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"
    LINE_COMMENT='regexp://.*'
    BLOCK_COMMENT='regexp:/\*(.|\n)*\*/'
    space='regexp:\s+'
  ]
  
  // Default inheritance
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
  implements="com.example.lang.psi.MyLangElement"
}
```

Parser configuration attributes control the generated parser class and its dependencies. Use **parserClass** to specify the fully qualified name of the generated parser class, **parserPackage** for the package containing parser-related classes, **parserUtilClass** for custom parser utility methods, and **parserImports** for additional imports needed by the generated parser.

PSI configuration attributes define how Grammar-Kit generates the Program Structure Interface classes. The **psiPackage** and **psiImplPackage** attributes specify where to generate PSI interfaces and their implementations. Use **psiClassPrefix** to add a consistent prefix to all generated PSI class names (e.g., "MyLang" results in MyLangFile, MyLangFunction), and **psiImplClassSuffix** to customize implementation class suffixes. The **psiImplUtilClass** attribute points to a utility class containing helper methods for PSI implementations.

Generation options control various aspects of code generation through the **generate** attribute, which accepts parameters like java version (8, 11, 17), names style ("long" for better debugging), visitor pattern support, and whether to generate PSI classes or token constants. The **generateTokens** attribute controls whether to generate token type constants in the element type holder class, while **generateFirstCheck** optimizes first-set checking by specifying the maximum lookahead depth.

The **tokens** attribute defines both literal tokens and pattern-based tokens:

```bnf
tokens=[
  // Literal tokens - exact string matches
  PLUS='+'
  MINUS='-'
  ASSIGN='='
  
  // Keyword tokens
  IF='if'
  ELSE='else'
  WHILE='while'
  
  // Pattern tokens using regular expressions
  ID='regexp:[a-zA-Z_][a-zA-Z0-9_]*'
  NUMBER='regexp:\d+(\.\d*)?'
  STRING='regexp:"([^"\\]|\\.)*"'
  
  // Whitespace and comments (typically skipped)
  space='regexp:\s+'
  line_comment='regexp://.*'
  block_comment='regexp:/\*(.|\n)*\*/'
]
```

## Rule Attributes

Rule attributes control parsing behavior and PSI generation for individual rules. You can apply them directly to rules or use pattern matching to apply them to multiple rules at once. The most important rule attributes are pin, recoverWhile, extends, implements, methods, and mixin.

The **pin** attribute marks a position in a sequence where the parser commits to that parse branch. Once a pinned element is matched, the parser will not backtrack even if later elements fail:

```bnf
// Pin by position (1-based)
function ::= 'function' ID '(' params? ')' block {pin=1}

// Pin by element
if_statement ::= 'if' '(' expression ')' statement else_clause? {pin="if"}

// Pin with pattern matching - pin first element in all statements
{
  pin(".*_statement")=1
}

assignment_statement ::= ID '=' expression ';'
return_statement ::= 'return' expression? ';'
```

Pin works with error recovery to create robust parsers. In a parenthesized list, pinning the opening parenthesis ensures the parser commits to parsing a list once it sees '('. The items rule pins the first item, and each item uses recoverWhile to skip invalid content until it finds a comma or closing parenthesis:

```bnf
list ::= '(' items? ')' {pin=1}
private items ::= item (',' item)* {pin(".*")=1}
item ::= expression {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

The **recoverWhile** attribute specifies a predicate rule that determines when to stop error recovery:

```bnf
// Basic recovery
statement ::= assignment | if_statement | while_statement {
  recoverWhile=statement_recover
}
private statement_recover ::= !(';' | '}' | 'if' | 'while' | ID)

// Recovery with auto-generation
method_body ::= '{' statement* '}' {pin=1 recoverWhile="#auto"}
// "#auto" generates recovery as !FOLLOW(method_body)

// Complex recovery in expressions
expression ::= term (('+' | '-') term)* {
  recoverWhile=expression_recover
}
private expression_recover ::= !(')' | ';' | ',')
```

The **extends** and **implements** attributes control the PSI class hierarchy for better API design:

```bnf
// All expression rules extend a common base
{
  extends(".*_expr")=expr
}

// Define inheritance hierarchy
expr ::= add_expr
  | mul_expr  
  | call_expr
  | literal_expr

// Create abstract base classes using fake rules
fake binary_expr ::= expr op expr {
  extends=expr
  methods=[
    left="expr[0]"
    operator="op"
    right="expr[1]"
  ]
}

add_expr ::= expr '+' expr {extends=binary_expr}
mul_expr ::= expr '*' expr {extends=binary_expr}

// Implement interfaces
identifier ::= ID {
  implements=["com.example.lang.psi.NamedElement" 
              "com.intellij.psi.PsiNameIdentifierOwner"]
}
```

The **methods** attribute defines custom methods in generated PSI classes:

```bnf
// Simple accessors
variable_declaration ::= 'var' ID '=' expression {
  methods=[
    getName
    setName
    getNameIdentifier
  ]
}

// Path-based accessors for complex structures
function ::= 'function' ID '(' params? ')' return_type? block {
  methods=[
    name="ID"
    parameters="params/param"  // Navigate to nested elements
    returnType="return_type"
    getPresentation           // Custom method implementation
  ]
  
  // Reference to implementation
  mixin="com.example.lang.psi.impl.FunctionMixin"
}

// Array-style accessors
argument_list ::= '(' (expression (',' expression)*)? ')' {
  methods=[
    arguments="expression"      // Returns List<Expression>
    firstArgument="expression[0]"
    lastArgument="expression[-1]"
  ]
}
```

The **mixin** attribute adds shared functionality to PSI classes by specifying a base class that provides common implementations:

```bnf
// Mixin class provides implementation
class_declaration ::= 'class' ID extends_clause? '{' member* '}' {
  mixin="com.example.lang.psi.impl.ClassMixin"
  implements="com.example.lang.psi.MyLangClass"
  
  methods=[
    getName
    getSuperClass
    getMethods="member/method_declaration"
  ]
}

// The mixin class would implement complex logic:
// public abstract class ClassMixin extends ASTWrapperPsiElement implements MyLangClass {
//   public String getName() { /* implementation */ }
//   public MyLangClass getSuperClass() { /* resolve extends clause */ }
// }
```

Other important rule attributes include **name** to override the PSI class name (e.g., `{name="identifier"}` generates IdentifierImpl instead of IdTokenImpl), **elementType** to share element types between rules, and **stubClass** to enable stub support for indexing. The elementType attribute is particularly useful with fake rules to create shared base types for similar constructs. The stubClass attribute requires extending StubBasedPsiElementBase and enables efficient indexing of language elements.

## Pattern-Based Attributes and Best Practices

Pattern-based attributes apply settings to multiple rules matching a regular expression pattern, reducing repetition and ensuring consistency across your grammar:

```bnf
{
  // Apply to all rules ending with "_expr"
  extends(".*_expr")=expr
  
  // Pin first element in all statement rules
  pin(".*_statement")=1
  
  // Add recovery to all declaration rules
  recoverWhile(".*_declaration")=declaration_recover
  
  // Complex patterns
  implements("(class|interface|enum)_declaration")="com.example.lang.psi.TypeDeclaration"
  
  // Multiple attributes for a pattern
  methods(".*_literal")=[getValue setValue]
}
```

Patterns are Java regular expressions applied to rule names. More specific patterns override general ones, and direct rule attributes always override pattern-based ones. When multiple attribute sources apply to a rule, they resolve in order of precedence: direct rule attributes first, then pattern-based attributes (more specific patterns before general ones), followed by global extends/implements defaults, and finally Grammar-Kit defaults.

Here's how precedence works in practice:
```bnf
{
  // Global default
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
  
  // Pattern for all expressions
  extends(".*_expr")=expr
  
  // More specific pattern
  extends("binary_.*_expr")=binary_expr
}

// Rule-specific overrides all
add_expr ::= expr '+' expr {extends=arithmetic_expr}
```

For robust parsing, combine pin and recoverWhile attributes strategically. Pin commits the parser to a specific parse path once it matches a key token, while recoverWhile skips invalid content until it finds a synchronization point. This combination enables parsers to handle malformed input gracefully:

```bnf
// Top-level recovery
file ::= element*
private element ::= !<<eof>> statement {
  pin=1
  recoverWhile=element_recover
}
private element_recover ::= !(statement_start)
private statement_start ::= 'if' | 'while' | 'for' | ID | '{'

// Nested structure recovery
block ::= '{' statement* '}' {pin=1}
statement ::= stmt_content ';'? {
  pin=1
  recoverWhile=statement_recover
}
private statement_recover ::= !(';' | '}' | statement_start)
```

When designing expression hierarchies, use pattern-based extends attributes to create a clean PSI structure. Define base expression rules and group related expressions together. Use fake rules to establish abstract base classes in your PSI hierarchy:

```bnf
{
  extends(".*_expr")=expr
  extends(".*_literal")=literal_expr
}

// Base expression rule
expr ::= assignment_expr
  | binary_expr_group
  | unary_expr_group  
  | postfix_expr_group
  | primary_expr_group

// Group related expressions
private binary_expr_group ::= add_expr | mul_expr | compare_expr
private primary_expr_group ::= literal_expr | ref_expr | paren_expr

// Fake rules for PSI hierarchy
fake binary_expr ::= expr
fake literal_expr ::= expr {
  methods=[getValue]
}

// Concrete rules
number_literal ::= NUMBER {extends=literal_expr}
string_literal ::= STRING {extends=literal_expr}
```

Organize tokens into logical groups for clarity. Define operators, delimiters, keywords, and pattern-based tokens separately. Mark whitespace and comment tokens for skipping during parsing:

```bnf
{
  tokens=[
    // Operators
    PLUS='+'
    MINUS='-'
    MULTIPLY='*'
    DIVIDE='/'
    
    // Delimiters  
    LPAREN='('
    RPAREN=')'
    LBRACE='{'
    RBRACE='}'
    
    // Keywords (reserved)
    IF='if'
    ELSE='else'
    WHILE='while'
    RETURN='return'
    
    // Patterns
    ID='regexp:[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER='regexp:\d+(\.\d*)?'
    STRING='regexp:"([^"\\]|\\.)*"'
    
    // Skip tokens
    space='regexp:\s+'
    line_comment='regexp://.*'
  ]
}
```

Common patterns emerge when using attributes effectively. For comma-separated lists, pin the opening delimiter and use recoverWhile on each item to handle malformed input. For optional clauses like if-else statements, pin key tokens and use methods attributes to provide clean accessors. When implementing name resolution, combine methods and mixin attributes to add reference resolution capabilities to identifier nodes.

