# Examples: BNF Grammar Syntax

## Scope Information
This provides examples for section 2.1: BNF Grammar Syntax

## Basic Grammar File Structure
```bnf
{
  tokens = [
    PLUS='+'
    id='regexp:\\w+'
  ]
}

root ::= expression
expression ::= id '+' id
```
- Header attributes in braces
- Token definitions array
- Grammar rules follow header

## Token Definitions

### Literal Tokens
```bnf
tokens = [
  SEMI=';'
  PLUS='+'
  KEYWORD='if'
]
```
- Named token with symbol
- Single quotes for literals
- Token names in UPPER_CASE

### Regexp Tokens
```bnf
tokens = [
  id='regexp:\\w+'
  number='regexp:\\d+'
  space='regexp:\\s+'
]
```
- Prefix with `regexp:`
- Standard regex patterns
- Required for Live Preview

### Mixed Token Types
```bnf
{
  tokens = [
    // Named tokens
    EQ='='
    LPAREN='('
    
    // Regexp tokens
    id='regexp:[a-zA-Z]+'
    string='regexp:"[^"]*"'
    
    // Keywords
    IF='if'
    THEN='then'
  ]
}
```
- Combine different token types
- Comments with `//`
- Order matters for precedence

## Rule Syntax with Sequences and Choices

### Basic Sequences
```bnf
assignment ::= id '=' expression
```
- Space-separated sequence
- Rules reference tokens/rules

### Choice Operator
```bnf
value ::= number | string | boolean
boolean ::= 'true' | 'false'
```
- Pipe `|` for alternatives
- Each option tried in order

### Combined Sequences and Choices
```bnf
statement ::= assignment | if_stmt | while_stmt
if_stmt ::= 'if' expr 'then' statement
```
- Mix sequences and choices
- Reference other rules

## Quantifiers Usage

### Optional (?)
```bnf
function ::= 'def' id params? body
params ::= '(' param_list ')'
```
- Zero or one occurrence
- Makes element optional

### One or More (+)
```bnf
param_list ::= param (',' param)+
block ::= '{' statement+ '}'
```
- At least one required
- Repeats with separator

### Zero or More (*)
```bnf
program ::= statement*
args ::= arg (',' arg)*
```
- Zero allowed
- Unlimited repetitions

## Grouping with Parentheses

### Simple Grouping
```bnf
expr ::= term ('+' term)*
```
- Groups elements together
- Apply quantifiers to group

### Complex Grouping
```bnf
declaration ::= ('var' | 'const') id ('=' value)?
```
- Group alternatives
- Group optional parts

### Nested Groups
```bnf
list ::= '[' (value (',' value)*)? ']'
```
- Groups within groups
- Combine with quantifiers

## Predicates Examples

### And Predicate (&)
```bnf
keyword_id ::= &keyword id
keyword ::= 'if' | 'then' | 'else'
```
- Positive lookahead
- Doesn't consume input

### Not Predicate (!)
```bnf
expr_end ::= !'+' !'-'
safe_id ::= !keyword id
```
- Negative lookahead
- Fails if pattern matches

### EOF Predicate
```bnf
file ::= item* !<<eof>>
item ::= !<<eof>> statement
```
- Check end of file
- External predicate syntax

## Rule Modifiers

### Private Rules
```bnf
expr ::= private_term (op private_term)*
private private_term ::= number | id
```
- No PSI node created
- Internal grammar use only

### External Rules
```bnf
external parse_string ::= parseStringContents
external meta_rule ::= <<param>>
```
- Hand-written parser method
- Delegates to Java code

### Meta Rules
```bnf
meta list ::= <<item>> (',' <<item>>)*
numbers ::= <<list number>>
ids ::= <<list id>>
```
- Parameterized rule templates
- Reusable patterns

### Left Rules
```bnf
expr ::= term plus_expr*
left plus_expr ::= '+' term
```
- Left-associative parsing
- Wraps left sibling

## Common Patterns

### Optional Separators
```bnf
rule ::= id '::=' expr ';'?
```
- Trailing semicolon optional

### List with Separators
```bnf
list ::= item (',' item)*
```
- Classic comma-separated list

### Block Structure
```bnf
block ::= '{' statement* '}'
```
- Delimited content blocks

## Anti-patterns

### Missing Regexp Prefix
```bnf
tokens = [
  id='\\w+'  // WRONG: needs regexp:
]
```
- Live Preview won't work

### Wrong Quantifier Position
```bnf
rule ::= id? '::=' expr  // WRONG
rule ::= id '::='? expr  // WRONG
```
- Quantifiers on elements only

### Invalid Token Names
```bnf
tokens = [
  my-token='-'  // WRONG: use MY_TOKEN
  123='123'     // WRONG: start with letter
]
```
- Follow naming conventions

### Ambiguous Choices
```bnf
expr ::= id | id '=' value  // WRONG
```
- First choice always wins
- Reorder or refactor

## Related Examples
- For attribute configuration → See Section 2.2
- For Live Preview setup → See Section 2.3
- For expression parsing → See Section 3.2
- For complete parsers → See Appendices