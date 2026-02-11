# Designing Grammar Rules

This page guides you through designing effective grammar rules for your language parser. You'll learn how to organize your grammar, apply common patterns, and avoid pitfalls that can lead to parsing errors or poor performance. The techniques presented here help you create maintainable grammars that generate efficient parsers with clean PSI hierarchies.

## Grammar Organization and Structure

Effective grammar organization starts with understanding how Grammar-Kit processes rules and generates code. Each public rule becomes a PSI element type, while private rules serve as internal parsing logic without creating AST nodes. This distinction drives many organizational decisions. Begin your grammar with the highest-level constructs and work down to terminals. This approach naturally creates a logical PSI hierarchy and makes the grammar easier to understand.

Start with your root rule that defines what constitutes a complete file in your language:

```bnf
{
  parserClass="com.example.lang.MyLanguageParser"
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
  
  elementTypeHolderClass="com.example.lang.psi.MyLanguageTypes"
  elementTypeClass="com.example.lang.psi.MyLanguageElementType"
  tokenTypeClass="com.example.lang.psi.MyLanguageTokenType"
  
  psiClassPrefix="MyLanguage"
  psiImplClassSuffix="Impl"
  psiPackage="com.example.lang.psi"
  psiImplPackage="com.example.lang.psi.impl"
}

// Root rule - what constitutes a complete file
root ::= file

// File contains a series of top-level elements
file ::= file_element*

// Each file element is a specific construct
private file_element ::= import_statement 
  | function_declaration 
  | class_declaration
  | statement
  {recoverWhile=file_element_recover}

// Recovery rule to skip to next top-level construct
private file_element_recover ::= !(IMPORT | FUNCTION | CLASS | ID)
```

This structure provides clear entry points and natural recovery boundaries. The private `file_element` rule handles the choice without creating an intermediate PSI node, while the recovery rule ensures the parser can continue after errors. Identify the major constructs in your language and create rules that reflect their logical structure. Group related rules together and use consistent naming patterns:

```bnf
// Declarations
class_declaration ::= CLASS identifier class_body
interface_declaration ::= INTERFACE identifier interface_body
function_declaration ::= FUNCTION identifier parameter_list block

// Statements
statement ::= expression_statement
  | block_statement
  | if_statement
  | while_statement
  | return_statement
  {recoverWhile=statement_recover}

private statement_recover ::= !(';' | '}' | statement_start)
private statement_start ::= IF | WHILE | RETURN | '{' | ID

// Expressions (see Expression Hierarchy section)
expression ::= assignment_expression
  | binary_expression
  | unary_expression
  | postfix_expression
  | primary_expression
```

### Naming Conventions and Rule Types

Consistent naming makes grammars more maintainable and helps other developers understand your intent. Grammar-Kit follows several conventions that you should adopt. Public rules create PSI nodes and should have descriptive names that reflect the language construct: `class_declaration` declares a class, `import_statement` imports a module, `parameter_list` lists function parameters, and `block_statement` represents a code block with braces.

Private rules handle internal parsing logic without creating nodes. Use underscores and descriptive suffixes: `statement_recover` for recovery predicates, `expr_recover` for expression recovery, `keyword_or_id` for matching either keywords or identifiers, and `comma_separated_list` for internal list parsing. Common suffix patterns communicate the rule's purpose: `*_expression` or `*_expr` for expression rules, `*_statement` for statements, `*_list` for list structures, `*_recover` for recovery predicates, and `*_start` for lookahead predicates.

The distinction between private and public rules is fundamental to grammar design. Public rules generate PSI element types and classes, while private rules exist only in the parser:

```bnf
// Public rule - creates ParameterListElement in PSI
parameter_list ::= '(' [ parameter (',' parameter)* ] ')' {pin=1}

// Public rule - creates ParameterElement in PSI  
parameter ::= type identifier default_value?

// Private rule - no PSI node, just parsing logic
private default_value ::= '=' expression {pin=1}

// Private rule - used for recovery, no PSI needed
private list_recover ::= !(')' | ',' | ';')
```

Use private rules when implementing recovery predicates, creating reusable parsing patterns, avoiding unnecessary PSI nodes, or handling internal choices that don't need AST representation.

### Advanced Rule Types

Meta rules provide reusable parsing patterns that can be instantiated with different parameters. They're particularly useful for lists and common structures:

```bnf
// Define a reusable comma-separated list pattern
meta comma_separated_list ::= <<param>> ( ',' <<param>> )* {pin(".*")=1}

// Use the meta rule for different list types
argument_list ::= '(' [ <<comma_separated_list expression>> ] ')'
parameter_list ::= '(' [ <<comma_separated_list parameter>> ] ')'
type_parameter_list ::= '<' <<comma_separated_list type_parameter>> '>'

// Meta rule for optional semicolon-terminated items
meta optional_semi ::= <<param>> ';'?

// Usage in different contexts
statement ::= <<optional_semi expression_statement>>
class_member ::= <<optional_semi field_declaration>>
```

Fake rules shape the PSI hierarchy without affecting parsing. They're useful for creating common base classes or organizing the PSI tree:

```bnf
// Fake rule defines common PSI interface
fake binary_expression ::= expression

// Actual rules extend the fake rule
additive_expression ::= expression '+' expression {extends=binary_expression}
multiplicative_expression ::= expression '*' expression {extends=binary_expression}
relational_expression ::= expression '<' expression {extends=binary_expression}

// All binary expressions now share a common PSI type
// This enables uniform handling in visitors and utilities
```

## Common Patterns and Design Decisions

Certain patterns appear repeatedly in language grammars. Understanding these patterns helps you implement them correctly and consistently. Lists are fundamental to most grammars, and Grammar-Kit provides several ways to handle them effectively:

```bnf
// Simple list - zero or more items
statement_list ::= statement*

// Non-empty list - one or more items
declaration_list ::= declaration+

// Comma-separated list with optional trailing comma
array_elements ::= '[' [ element_list ','? ] ']' {pin=1}
private element_list ::= expression (',' expression)*

// List with recovery - continues parsing after errors
argument_list ::= '(' [ argument (',' argument)* ] ')' {
  pin=1
  recoverWhile=argument_list_recover
}
private argument_list_recover ::= !(')' | ';' | '{')

// List with pinning on separators for better error recovery
field_list ::= field (pin_comma field)* {pin(".*")=1}
private pin_comma ::= ',' {pin=1}
```

Optional elements are common in language design. Grammar-Kit provides multiple ways to express them. You can use the `?` quantifier, `[]` brackets (equivalent to `?`), or create separate rules for complex optional structures:

```bnf
// Using ? quantifier
variable_declaration ::= VAR type? identifier initializer?

// Using [] brackets (equivalent to ?)
function_declaration ::= FUNCTION identifier parameter_list return_type? block
return_type ::= ':' type

// Optional with default parsing behavior
class_declaration ::= CLASS identifier extends_clause? implements_clause? class_body
extends_clause ::= EXTENDS type
implements_clause ::= IMPLEMENTS type_list

// Complex optional with pinning
initializer ::= '=' expression {pin=1}
// If '=' is seen, expression must follow
```

Properly handling nested structures requires careful attention to precedence and recovery:

```bnf
// Nested blocks with clear boundaries
block ::= '{' statement* '}' {pin=1}

// Nested expressions with precedence
expression ::= assignment_expression
  | conditional_expression  
  | logical_or_expression
  | logical_and_expression
  | equality_expression
  | relational_expression
  | additive_expression
  | multiplicative_expression
  | unary_expression
  | postfix_expression
  | primary_expression

// Nested with recovery at each level
class_body ::= '{' class_member* '}' {
  pin=1
  recoverWhile=class_body_recover
}
private class_body_recover ::= !'}'

class_member ::= field_declaration 
  | method_declaration 
  | class_declaration  // nested classes
  {recoverWhile=class_member_recover}
private class_member_recover ::= !('}' | FIELD | METHOD | CLASS)
```

Most languages distinguish between statements (which don't produce values) and expressions (which do). This distinction affects grammar organization:

```bnf
// Statements - no value produced
statement ::= expression_statement
  | declaration_statement  
  | if_statement
  | while_statement
  | return_statement
  | block_statement
  {recoverWhile=statement_recover}

// Expression statement - expression used as statement
expression_statement ::= expression ';'

// Expressions - produce values
expression ::= assignment_expr
  | ternary_expr
  | binary_expr
  | unary_expr
  | postfix_expr
  | call_expr
  | primary_expr

// Some constructs can be both
// Block expression (like Rust/Kotlin)
block_expression ::= '{' statement* expression? '}' {
  extends=expression
  // Last expression is the block's value
}
```

### Expression Hierarchy Pattern

The expression hierarchy pattern is crucial for parsing expressions with proper precedence and associativity:

```bnf
{
  extends(".*_expr")=expression
}

// Top-level expression rule
expression ::= assignment_expr
  | ternary_expr
  | or_expr
  | and_expr
  | equality_expr
  | relational_expr  
  | shift_expr
  | additive_expr
  | multiplicative_expr
  | unary_expr
  | postfix_expr
  | primary_expr

// Assignment (right-associative)
assignment_expr ::= expression '=' expression {rightAssociative=true}

// Ternary conditional
ternary_expr ::= expression '?' expression ':' expression

// Binary operators (left-associative by default)
or_expr ::= expression '||' expression
and_expr ::= expression '&&' expression
equality_expr ::= expression ('==' | '!=') expression
relational_expr ::= expression ('<' | '>' | '<=' | '>=') expression
shift_expr ::= expression ('<<' | '>>') expression
additive_expr ::= expression ('+' | '-') expression
multiplicative_expr ::= expression ('*' | '/' | '%') expression

// Unary operators
unary_expr ::= ('+' | '-' | '!' | '~') expression

// Postfix operators
postfix_expr ::= expression ( '++' | '--' )

// Primary expressions - the atoms
primary_expr ::= literal
  | identifier  
  | '(' expression ')'
  | array_literal
  | object_literal

// Literals
literal ::= NUMBER | STRING | TRUE | FALSE | NULL
```

## Avoiding Common Pitfalls

Understanding common grammar design problems helps you avoid them from the start. Left recursion occurs when a rule references itself as its first element. While Grammar-Kit supports left recursion with the `left` modifier, it's important to understand when and how to use it:

```bnf
// Direct left recursion - use 'left' modifier
left binary_expression ::= expression operator expression

// Or restructure to avoid left recursion
expression ::= primary_expression suffix*
private suffix ::= binary_operator expression
  | '[' expression ']'  
  | '(' argument_list ')'

// Expression hierarchy pattern (recommended)
expression ::= assignment_expr
assignment_expr ::= ternary_expr [ '=' assignment_expr ]
ternary_expr ::= or_expr [ '?' expression ':' ternary_expr ]
or_expr ::= and_expr ( '||' and_expr )*
and_expr ::= equality_expr ( '&&' equality_expr )*
// ... continue hierarchy
```

Ambiguity occurs when input can be parsed in multiple ways. Resolve ambiguity through rule ordering, pinning, or restructuring:

```bnf
// Ambiguous - is "if (x) if (y) a; else b;" parsed as:
// if (x) { if (y) a; else b; }  OR  if (x) { if (y) a; } else b;
if_statement ::= IF '(' expression ')' statement else_clause?
else_clause ::= ELSE statement

// Resolved using pinning - else binds to nearest if
if_statement ::= IF '(' expression ')' statement else_clause? {pin=2}
else_clause ::= ELSE statement {pin=1}

// Ambiguous - call or array access?
postfix ::= expression '(' argument_list ')'
  | expression '[' expression ']'

// Resolved with clear precedence
postfix_expression ::= primary_expression postfix_suffix*
private postfix_suffix ::= arguments | index | member_access
arguments ::= '(' argument_list ')' {pin=1}
index ::= '[' expression ']' {pin=1}
member_access ::= '.' identifier {pin=1}
```

Token conflicts arise when the lexer can't determine which token to produce. Design your tokens and keywords carefully:

```bnf
{
  tokens = [
    // Define keywords explicitly
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    
    // Use regexp for flexible matching
    ID = 'regexp:\p{Alpha}\w*'
    NUMBER = 'regexp:\d+(\.\d+)?'
    STRING = "regexp:\"([^\"\\]|\\.)*\""
    
    // Operators - be careful with overlap
    PLUS_PLUS = '++'
    PLUS = '+'
    ARROW = '->'
    MINUS = '-'
  ]
}

// In the grammar, keywords take precedence over ID
identifier ::= ID
  | KEYWORD_AS_ID  // if you need keywords as identifiers

// Use & predicate to resolve ambiguity
type_or_expr ::= &type type | expression
```

Grammar design significantly impacts parser performance. Follow these guidelines for optimal performance. Use consumeToken methods for simple token sequences, minimize backtracking with proper pinning, optimize expression parsing with priorities, use first-token optimization for statement choices, and avoid deep recursion in lists:

```bnf
// Use consumeToken methods for simple token sequences
{
  consumeTokenMethod(".*_list")="consumeTokenFast"
}

// Minimize backtracking with proper pinning
function_call ::= identifier '(' argument_list ')' {pin=2}
// Once '(' is seen, commit to function call

// Optimize expression parsing with priorities
expression ::= or_expr
or_expr ::= and_expr ( '||' and_expr )*
and_expr ::= equality_expr ( '&&' equality_expr )*
// Continues down to primary - no backtracking needed

// Use first-token optimization
statement ::= if_statement
  | while_statement  
  | for_statement
  | return_statement
  | expression_statement
// Parser can decide based on first token

// Avoid deep recursion in lists
// Bad - creates deep tree
list ::= item | item ',' list

// Good - creates flat tree  
list ::= item ( ',' item )*
```

## Best Practices and Next Steps

Following these practices will help you create maintainable, efficient grammars. Start with structure by designing your PSI hierarchy before writing rules. Use private rules to keep the PSI tree clean by making internal rules private. Pin strategically on tokens that commit the parser to a path. Recover gracefully by adding recovery rules at major structure boundaries. Test incrementally using Live Preview to validate rules as you write them. Document patterns by adding comments explaining complex rules and design decisions. Follow naming conventions throughout your grammar. Get correctness first, then optimize for performance.

With a well-designed grammar structure in place, you can focus on specific parsing challenges:

- [Expression Parsing](expression-parsing.md) - Deep dive into expression precedence and optimization
- [Error Recovery](error-recovery.md) - Advanced techniques for resilient parsers
- [PSI Customization](../code-generation/psi-customization.md) - Shaping your PSI hierarchy

For complete examples of well-structured grammars, see the [Example Grammars](../appendices/examples.md) appendix.