# BNF Grammar Syntax

This page enables you to write BNF grammars that Grammar-Kit uses to generate parsers, lexers, and PSI (Program Structure Interface) implementations for your custom language. Grammar-Kit extends the standard BNF notation with powerful features for building production-quality language support in IntelliJ IDEA.

## Introduction

Grammar-Kit uses an extended BNF (Backus-Naur Form) syntax that combines traditional BNF with additional constructs for practical parser generation. This variant includes modifiers and quantifiers (?, *, +) for optional and repeated elements, attributes for controlling code generation and parser behavior, predicates for lookahead and negative assertions, built-in error recovery mechanisms, and direct integration with IntelliJ's PSI tree structure. A Grammar-Kit BNF file describes your language's syntax rules and generates a complete parser that integrates with IntelliJ IDEA's language support framework.

## Grammar Structure

Every Grammar-Kit BNF file consists of three main parts: header attributes, token definitions, and grammar rules.

### 1. Header Attributes (Optional)

Configuration attributes enclosed in curly braces `{}` control parser generation:

```bnf
{
  // Parser class configuration
  parserClass="com.example.lang.parser.MyParser"
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
  
  // PSI class generation
  psiClassPrefix="My"
  psiImplClassSuffix="Impl"
  psiPackage="com.example.lang.psi"
  psiImplPackage="com.example.lang.psi.impl"
  
  // Token definitions
  tokens = [
    // Token definitions go here
  ]
}
```

### 2. Token Definitions

Tokens can be defined in the header's `tokens` attribute:

```bnf
tokens = [
  // Literal tokens
  PLUS="+"
  MINUS="-"
  LPAREN="("
  RPAREN=")"
  
  // Regular expression tokens
  ID="regexp:[a-zA-Z][a-zA-Z0-9]*"
  NUMBER="regexp:[0-9]+"
  STRING="regexp:\"[^\"]*\""
  
  // Whitespace and comments
  space="regexp:\s+"
  line_comment="regexp://.*"
  block_comment="regexp:/\*(.|\n)*\*/"
]
```

### 3. Grammar Rules

The actual production rules that define your language structure:

```bnf
// Root rule (entry point)
root ::= statement*

// Rule definitions
statement ::= assignment | expression ';'
assignment ::= ID '=' expression
expression ::= term (('+' | '-') term)*
term ::= factor (('*' | '/') factor)*
factor ::= NUMBER | ID | '(' expression ')'
```

### Complete Example

A complete grammar for a simple expression language demonstrates all three parts working together:

```bnf
{
  parserClass="com.example.expr.parser.ExprParser"
  extends="com.intellij.extapi.psi.ASTWrapperPsiElement"
  
  psiClassPrefix="Expr"
  psiImplClassSuffix="Impl"
  psiPackage="com.example.expr.psi"
  psiImplPackage="com.example.expr.psi.impl"
  
  tokens = [
    PLUS='+'
    MINUS='-'
    TIMES='*'
    DIVIDE='/'
    LPAREN='('
    RPAREN=')'
    SEMI=';'
    EQUALS='='
    
    space='regexp:\s+'
    ID='regexp:[a-zA-Z][a-zA-Z0-9]*'
    NUMBER='regexp:[0-9]+(\.[0-9]+)?'
    line_comment='regexp://.*'
  ]
}

root ::= statement*

statement ::= assignment | expression_statement
assignment ::= ID '=' expression ';'
expression_statement ::= expression ';'

expression ::= add_expr
add_expr ::= mul_expr (('+' | '-') mul_expr)*
mul_expr ::= primary_expr (('*' | '/') primary_expr)*
primary_expr ::= NUMBER | ID | '(' expression ')'
```

## Rule Syntax

Grammar-Kit provides several constructs for defining rules:

### Basic Rule Definition

Every rule follows the pattern `rule_name ::= expression`. Rules can reference other rules, tokens, or literal strings:

```bnf
rule_name ::= expression

// Rules referencing other rules
statement ::= if_statement | while_statement | expression_statement
if_statement ::= 'if' '(' expression ')' statement
```

### Sequences

Elements in a sequence are separated by spaces, and all elements must match in order:

```bnf
// All three elements must appear in sequence
function_call ::= ID '(' argument_list ')'

// Common pattern: keyword followed by content
import_statement ::= 'import' package_name ';'
```

### Choices (Alternatives)

Use the pipe symbol `|` to separate alternatives:

```bnf
// Match any one of these alternatives
literal ::= NUMBER | STRING | 'true' | 'false' | 'null'

// Alternatives can be complex expressions
statement ::= assignment ';' 
           | method_call ';' 
           | 'return' expression? ';'
```

### Quantifiers

Quantifiers specify how many times an element can appear.

#### Optional: `?`
Zero or one occurrence:

```bnf
// Optional else clause
if_statement ::= 'if' '(' condition ')' statement else_clause?
else_clause ::= 'else' statement

// Optional initialization
variable_decl ::= type ID ('=' expression)?
```

#### Zero or more: `*`
Any number of occurrences, including none:

```bnf
// Zero or more statements
block ::= '{' statement* '}'

// List with optional items
array ::= '[' (expression (',' expression)*)? ']'
```

#### One or more: `+`
At least one occurrence:

```bnf
// At least one digit
integer ::= digit+

// Non-empty list
identifier_list ::= ID (',' ID)+
```

### Grouping

Use parentheses to group elements:

```bnf
// Group alternatives within a sequence
declaration ::= ('var' | 'const' | 'let') ID '=' expression

// Group for quantifiers
qualified_name ::= ID ('.' ID)*

// Complex grouping
expr ::= term (('+' | '-') term)*
```

### Square Brackets (Inline Optional)

Square brackets `[]` are shorthand for optional groups. These two forms are equivalent:

```bnf
rule1 ::= 'class' ID ['extends' ID] '{' '}'
rule2 ::= 'class' ID ('extends' ID)? '{' '}'
```

### Curly Braces (Inline Attributes)

Curly braces after a rule add attributes:

```bnf
// Pin attribute for error recovery
assignment ::= ID '=' expression {pin=2}

// Multiple attributes
array ::= '[' array_elements? ']' {pin=1 recoverWhile=not_bracket}
```

### Predicates

Predicates provide lookahead without consuming tokens.

#### And-predicate: `&`
Succeeds if the following element matches (positive lookahead):

```bnf
// Only parse 'get' as a getter if followed by an ID
getter ::= &'get' 'get' ID '(' ')'

// Disambiguate between similar constructs
type_cast ::= &'(' '(' type ')' expression
```

#### Not-predicate: `!`
Succeeds if the following element doesn't match (negative lookahead):

```bnf
// Match any token except closing brace
block_content ::= !'}' element

// Common recovery pattern
recover ::= !(';' | '}' | 'else')
```

### Practical Examples

#### Lists with Separators

```bnf
// Simple comma-separated list
argument_list ::= expression (',' expression)*

// Optional list with at least one element when present
parameter_list ::= [parameter (',' parameter)*]

// List with optional trailing comma
array_elements ::= expression (',' expression)* ','?
```

#### Optional Elements

```bnf
// Optional modifiers
method ::= modifier* type ID '(' parameters? ')' block
modifier ::= 'public' | 'private' | 'static'

// Optional with default
visibility ::= ('public' | 'private' | 'protected')?
```

#### Nested Structures

```bnf
// Nested blocks
block ::= '{' statement* '}'
statement ::= simple_statement | block

// Nested expressions
expression ::= assignment | conditional
assignment ::= ID '=' expression
conditional ::= expression '?' expression ':' expression
```

#### Statement vs Expression Distinction

```bnf
// Statements don't return values
statement ::= expression_stmt | if_stmt | while_stmt | block
expression_stmt ::= expression ';'

// Expressions do return values
expression ::= literal | ID | binary_expr | '(' expression ')'
binary_expr ::= expression operator expression

// Some constructs can be both
if_stmt ::= 'if' '(' expression ')' statement
if_expr ::= 'if' '(' expression ')' expression 'else' expression
```

## Token Types

Grammar-Kit supports three types of tokens:

### 1. Literal Tokens

String literals in single or double quotes are matched exactly:

```bnf
// Single quotes (common for operators and keywords)
operator ::= '+' | '-' | '*' | '/'
keyword ::= 'if' | 'else' | 'while' | 'return'

// Double quotes (equivalent to single quotes)
assignment ::= ID "=" expression
```

Use literal tokens for keywords (`'if'`, `'class'`, `'return'`), operators (`'+'`, `'::'`, `'=>'`), and delimiters (`';'`, `','`, `'{'`). Use single quotes for consistency and define frequently used literals as named tokens.

### 2. Named Tokens

Tokens defined in the `tokens` block and referenced by name:

```bnf
{
  tokens = [
    // Operators
    PLUS='+'
    MINUS='-'
    ASSIGN='='
    ARROW='=>'
    
    // Keywords can be tokens too
    IF='if'
    ELSE='else'
    
    // Complex tokens
    ID='regexp:[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER='regexp:[0-9]+'
  ]
}

// Using named tokens
expression ::= term ((PLUS | MINUS) term)*
assignment ::= ID ASSIGN expression
arrow_function ::= ID ARROW expression
```

Use named tokens for frequently used literals, when you need to attach attributes to tokens, or for better readability in complex rules. Named tokens provide central definition that makes changes easier, allow specifying token text and pattern separately, and create clearer rule definitions.

### 3. Regular Expression Tokens

Define tokens using regular expressions with `regexp:` prefix:

```bnf
{
  tokens = [
    // Identifiers
    ID='regexp:[a-zA-Z_][a-zA-Z0-9_]*'
    
    // Numbers
    INTEGER='regexp:[0-9]+'
    FLOAT='regexp:[0-9]+\.[0-9]+'
    NUMBER='regexp:[0-9]+(\.[0-9]+)?'
    
    // Strings
    STRING='regexp:"[^"]*"'
    CHAR='regexp:\'[^\']\''
    
    // Comments and whitespace
    space='regexp:\s+'
    line_comment='regexp://.*'
    block_comment='regexp:/\*(.|\n)*\*/'
  ]
}
```

Use regular expression tokens for identifiers and names, numbers and numeric literals, string literals with escape sequences, comments and whitespace, and any pattern-based token. Regular expressions use standard Java regex syntax. Escape special characters (`\.` for dot, `\*` for asterisk), use character classes (`\w`, `\d`, `\s`), and Unicode categories (`\p{Alpha}`, `\p{Digit}`).

### Token Precedence

When multiple token patterns could match, Grammar-Kit follows these rules: longest match wins (`'<='` matches as one token, not `'<'` followed by `'='`), explicit tokens take precedence over implicit literals, and the first matching pattern in the tokens list wins.

```bnf
{
  tokens = [
    // These are checked in order
    LTEQ='<='  // Matches '<=' as single token
    LT='<'     // Only matches '<' not followed by '='
    EQ='='
    
    // Keywords vs identifiers
    IF='if'                               // Matches 'if' exactly
    ID='regexp:[a-zA-Z_][a-zA-Z0-9_]*'  // Matches other identifiers
  ]
}
```

### Live Preview Behavior

In Grammar-Kit's Live Preview, literal tokens are highlighted immediately as you type them, named tokens show their names in the PSI tree, regexp tokens are matched dynamically and validated, and undefined tokens are highlighted as errors.

### Best Practices

Define whitespace handling explicitly with a space token that is usually skipped by the parser. Handle comments explicitly with line_comment and block_comment tokens. Use meaningful token names that clearly indicate their purpose (LEFT_PAREN instead of LP). Group related tokens together in your tokens block for better organization.

```bnf
tokens = [
  // Whitespace
  space='regexp:\s+'
  
  // Comments
  line_comment='regexp://.*'
  block_comment='regexp:/\*(.|\n)*\*/'
  
  // Operators
  PLUS='+' MINUS='-' TIMES='*' DIVIDE='/'
  LEFT_PAREN='(' RIGHT_PAREN=')'
  
  // Comparison
  EQ='==' NEQ='!=' LT='<' GT='>' LTEQ='<=' GTEQ='>='
  
  // Literals
  NUMBER='regexp:[0-9]+' STRING='regexp:"[^"]*"'
]
```

## Common Patterns

Here are complete examples of frequently used grammar patterns:

### Comma-Separated Lists

```bnf
// Simple list (may be empty)
argument_list ::= [expression (',' expression)*]

// Non-empty list
parameter_list ::= parameter (',' parameter)*

// List with optional trailing comma
array_literal ::= '[' [array_element (',' array_element)* ','?] ']'

// List with recovery
safe_list ::= element (',' element)* {recoverWhile=not_semicolon}
private not_semicolon ::= !(';' | '}')
```

### Block Structures

```bnf
// Basic block
block ::= '{' statement* '}'

// Block with recovery
safe_block ::= '{' block_content* '}' {pin=1}
private block_content ::= !'}' statement {recoverWhile=not_brace}
private not_brace ::= !'}'

// Nested blocks with proper scoping
compound_statement ::= '{' inner_statement* '}'
inner_statement ::= variable_declaration | expression_statement | compound_statement
```

### Expression Precedence

```bnf
// Classic precedence climbing
expression ::= assignment_expr
assignment_expr ::= conditional_expr ('=' assignment_expr)?
conditional_expr ::= or_expr ('?' expression ':' conditional_expr)?
or_expr ::= and_expr ('||' and_expr)*
and_expr ::= equality_expr ('&&' equality_expr)*
equality_expr ::= relational_expr (('==' | '!=') relational_expr)*
relational_expr ::= additive_expr (('<' | '>' | '<=' | '>=') additive_expr)*
additive_expr ::= multiplicative_expr (('+' | '-') multiplicative_expr)*
multiplicative_expr ::= unary_expr (('*' | '/' | '%') unary_expr)*
unary_expr ::= ('!' | '-' | '+')? postfix_expr
postfix_expr ::= primary_expr ('.' ID | '[' expression ']' | '(' argument_list? ')')*
primary_expr ::= ID | NUMBER | STRING | '(' expression ')'
```

### Error Recovery Patterns

```bnf
// Skip tokens until recovery point
statement ::= assignment ';' {pin=1 recoverWhile=statement_recover}
private statement_recover ::= !(';' | '{' | '}' | ID)

// Pinning for better error messages
function ::= 'function' ID '(' parameter_list? ')' block {pin=2}

// Multiple recovery strategies
class_member ::= field_decl | method_decl {recoverWhile=member_recover}
private member_recover ::= !('public' | 'private' | 'static' | '}')
```

Use the Live Preview feature to test your grammar as you write it, and refer to the examples above for common patterns and best practices.