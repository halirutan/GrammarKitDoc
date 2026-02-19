# Examples: Expression Parsing

## Scope Information
This provides examples for section 2.3: Expression Parsing

## Expression Parsing Fundamentals

### Basic Expression Grammar
```bnf
{
  extends(".*expr")=expr
}

expr ::= add_expr
  | mul_expr
  | unary_expr
  | primary_expr

add_expr ::= expr '+' expr
  | expr '-' expr

mul_expr ::= expr '*' expr
  | expr '/' expr

unary_expr ::= '-' expr
  | '+' expr

primary_expr ::= number
  | '(' expr ')'
```
- Defines operator precedence hierarchy
- Higher rules = lower precedence
- Binary operators parse left-to-right
- Unary operators bind tighter
- Parentheses override precedence

### Expression vs Statement Parsing
```bnf
root ::= statement*
statement ::= expr ';'
  | assignment ';'

assignment ::= id '=' expr

expr ::= add_expr | mul_expr | primary
// expressions produce values

primary ::= number | id | '(' expr ')'
```
- Statements require semicolons
- Expressions compute values
- Assignments are statements
- Expressions nest in statements

## Implementing Precedence

### Traditional Precedence Climbing
```bnf
expr ::= term ('+' term | '-' term)*
term ::= factor ('*' factor | '/' factor)*
factor ::= unary | primary
unary ::= '-' factor | '+' factor
primary ::= number | '(' expr ')'
```
- Each level handles operators
- Lower levels = higher precedence
- Explicit nesting structure
- Creates deep PSI trees

### Layer-Based Approach
```bnf
{
  extends(".*expr")=expr
}

expr ::= assign_group
  | add_group
  | mul_group
  | unary_group
  | primary_group

private assign_group ::= assign_expr
private add_group ::= plus_expr | minus_expr
private mul_group ::= mul_expr | div_expr
private unary_group ::= unary_plus | unary_minus
private primary_group ::= number | paren_expr

assign_expr ::= expr '=' expr
plus_expr ::= expr '+' expr
minus_expr ::= expr '-' expr
mul_expr ::= expr '*' expr
div_expr ::= expr '/' expr
unary_plus ::= '+' expr
unary_minus ::= '-' expr
paren_expr ::= '(' expr ')'
```
- Private groups organize operators
- Same priority in groups
- Cleaner grammar structure
- Flatter PSI with extends

### Priority Attributes
```bnf
{
  // Priority table generated in parser:
  // 0: assign_expr
  // 1: plus_expr, minus_expr  
  // 2: mul_expr, div_expr
  // 3: unary_expr
  // 4: primary_expr
}

expr ::= assign_expr
  | add_group
  | mul_group  
  | unary_expr
  | primary_expr
  {extraRoot=true}

// Lower in grammar = higher priority
```
- Priority increases top-to-bottom
- Comments show priority table
- extraRoot marks expression boundary
- Parser uses priority loop

## Associativity Control

### Left Associative Operators
```bnf
// Default behavior - left to right
expr ::= expr '+' expr  // 1+2+3 = (1+2)+3
  | expr '-' expr       // 5-3-1 = (5-3)-1
  | primary

// Explicit left recursion
left add_expr ::= '+' factor
expr ::= factor add_expr*
factor ::= number | '(' expr ')'
```
- Default parsing is left-associative
- Left modifier enables recursion
- Creates flat PSI trees
- Efficient for chains

### Right Associative Operators
```bnf
// Assignment and exponentiation
assign_expr ::= expr '=' expr { rightAssociative=true }
// a=b=c parsed as a=(b=c)

exp_expr ::= expr '^' expr { rightAssociative=true }
// 2^3^4 parsed as 2^(3^4)
```
- rightAssociative attribute
- Parses right-to-left
- Common for assignment
- Used for exponentiation

### Non-Associative Operators
```bnf
// Comparison operators
compare_expr ::= expr '<' expr
  | expr '>' expr
  | expr '==' expr

// Prevent chaining: a < b < c is error
expr ::= compare_expr {
  // No compare_expr in operands
}
  | add_expr
  | primary
```
- Some operators don't chain
- Grammar prevents nesting
- Comparisons typically non-associative
- Requires explicit parentheses

### Mixed Associativity
```bnf
{
  extends(".*expr")=expr
}

expr ::= assign_expr      // right associative
  | ternary_expr         // right associative
  | or_expr              // left associative
  | and_expr             // left associative
  | compare_expr         // non-associative
  | add_expr             // left associative
  | mul_expr             // left associative
  | exp_expr             // right associative
  | unary_expr
  | primary_expr

assign_expr ::= expr '=' expr { rightAssociative=true }
ternary_expr ::= expr '?' expr ':' expr { rightAssociative=true }
exp_expr ::= expr '^' expr { rightAssociative=true }

// Others are left associative by default
```
- Different operators, different rules
- Attribute controls each operator
- Parser handles mixed types
- Maintains correct precedence

## Expression Optimization

### Avoiding Deep PSI Trees
```bnf
// BAD: Creates deep nesting
expr ::= term
term ::= factor  
factor ::= unary
unary ::= postfix
postfix ::= primary
primary ::= number

// GOOD: Flat structure
expr ::= add_expr | mul_expr | unary_expr | primary
add_expr ::= expr '+' expr
// ... other rules
```
- Avoid intermediate rules
- Direct operator definitions
- Reduces PSI depth
- Better performance

### Using Extends for Flat Structure
```bnf
{
  extends(".*expr")=expr
  // All *expr rules extend expr
}

expr ::= plus_expr
  | minus_expr
  | mul_expr
  | div_expr
  | ref_expr
  | literal_expr

// PSI shows expr nodes, not plus_expr
plus_expr ::= expr '+' expr
minus_expr ::= expr '-' expr

// Shared PSI type for references
fake ref_expr ::= expr? '.' identifier
simple_ref_expr ::= identifier {extends=ref_expr elementType=ref_expr}
qualified_expr ::= expr '.' identifier {extends=ref_expr elementType=ref_expr}
```
- extends flattens hierarchy
- Reduces PSI node types
- fake defines interfaces
- elementType reuses types

### The Expression Parsing Idiom
```bnf
{
  extends(".*expr")=expr
  consumeTokenMethod(".*_op")="consumeTokenFast"
}

// Expression root with priority groups
expr ::= assign_group
  | add_group
  | mul_group
  | unary_group
  | primary_group
  {extraRoot=true}

// Private groups for same priority
private add_group ::= plus_expr | minus_expr
private mul_group ::= mul_expr | div_expr

// Left recursion for efficiency
left plus_expr ::= plus_op factor
private plus_op ::= '+'
factor ::= mul_group | unary_group | primary_group

// Or binary style
binary_plus ::= expr '+' expr
```
- Standard Grammar-Kit pattern
- Combines all optimizations
- Private groups organize
- Left recursion option

### Binary and N-ary Operations
```bnf
// Binary operation (two operands)
add_expr ::= expr '+' expr

// N-ary operation (2+ operands)  
exp_expr ::= expr ('**' expr) +
// Parses a**b**c as single node

// List-like expression
arg_list ::= expr (',' expr)*
// Parses a,b,c,d as list

// Mixed operators at same level
add_expr ::= expr ('+' | '-') expr
```
- Binary: exactly two operands
- N-ary: two or more
- Plus after parens required
- Efficient for chains

## Complex Expressions

### Mixing Operator Types
```bnf
expr ::= assign_expr
  | prefix_group
  | infix_group  
  | postfix_group
  | primary_group

private prefix_group ::= neg_expr | not_expr | inc_expr
private infix_group ::= add_expr | mul_expr | and_expr
private postfix_group ::= inc_post | dec_post | index_expr

neg_expr ::= '-' expr
not_expr ::= '!' expr
inc_expr ::= '++' expr

add_expr ::= expr '+' expr
mul_expr ::= expr '*' expr
and_expr ::= expr '&&' expr

inc_post ::= expr '++'
dec_post ::= expr '--'
index_expr ::= expr '[' expr ']'
```
- Prefix before operand
- Infix between operands
- Postfix after operand
- All in one grammar

### Ternary Operators
```bnf
// Conditional expression
ternary_expr ::= expr '?' expr ':' expr
// Right associative like assignment

// Elvis operator (null coalescing)
elvis_expr ::= expr '?:' expr

// Between operator
between_expr ::= expr BETWEEN expr AND expr {
  methods=[testExpr="expr[0]"]
}

// Proper precedence placement
expr ::= assign_expr
  | ternary_expr  // Lower than assignment
  | or_expr
  | and_expr
  // ... other operators
```
- Three or more operands
- Usually right associative
- Custom methods for validation
- Careful precedence placement

### Function Calls and Indexing
```bnf
// Function calls
call_expr ::= ref_expr arg_list
arg_list ::= '(' [ !')' expr (',' expr)* ] ')' {pin(".*")=1}

// Method chaining
expr ::= call_expr
  | qualification_expr
  | index_expr
  | primary_expr

qualification_expr ::= expr '.' identifier
index_expr ::= expr '[' expr ']'

// Combined example
// obj.method(a, b)[0].field
```
- Calls higher than arithmetic
- Pin on opening paren
- Chaining via left recursion
- Natural precedence order

### Type Constraints
```bnf
// Type annotations in expressions
typed_expr ::= expr ':' type
cast_expr ::= expr AS type
instanceof_expr ::= expr IS type

// Generic type arguments
call_expr ::= ref_expr type_args? arg_list
type_args ::= '<' type (',' type)* '>'

// Precedence considerations
expr ::= cast_group
  | compare_group
  | add_group
  // ...

private cast_group ::= cast_expr | typed_expr
private compare_group ::= instanceof_expr | eq_expr
```
- Type operators need precedence
- Usually above arithmetic
- Below member access
- Consider parsing ambiguity

### Contextual Expressions
```bnf
// Lambda expressions
lambda_expr ::= param_list '=>' expr
  | identifier '=>' expr
param_list ::= '(' [ param (',' param)* ] ')'

// Let expressions
let_expr ::= LET binding IN expr
binding ::= identifier '=' expr

// Contextual precedence
expr ::= let_expr  // Lowest precedence
  | lambda_expr    // Above let
  | ternary_expr   // Above lambda
  | or_expr
  // ... rest of operators

// External/meta rules
external special_expr ::= parse_special_expr
meta parse_special_expr ::= 'special' '(' expr ')'
```
- Some expressions change context
- Lambdas bind loosely
- Let binds very loosely
- External for custom parsing

## Common Patterns

### Expression with Statements
```bnf
// Expression statements
stmt ::= expr_stmt
  | block_stmt
  | if_stmt

expr_stmt ::= expr ';'

// Restrict statement expressions
expr_stmt ::= stmt_expr ';'
stmt_expr ::= assign_expr
  | call_expr
  | inc_expr
  | dec_expr
```
- Not all expressions make statements
- Assignments and calls common
- Restrict to avoid confusion

### Optional Operators
```bnf
// Nullable/optional chaining
safe_call ::= expr '?.' identifier
safe_index ::= expr '?[' expr ']'

// Default values
default_expr ::= expr '??' expr

// Null-safe navigation
expr ::= safe_nav_group
  | call_expr
  | primary_expr

private safe_nav_group ::= safe_call | safe_index
```
- Modern operator patterns
- Handle null safely
- Higher than arithmetic
- Lower than regular access

## Anti-patterns

### Deep Grammar Nesting
```bnf
// DON'T DO THIS
expr ::= assignment
assignment ::= conditional
conditional ::= logical_or
logical_or ::= logical_and
logical_and ::= equality
equality ::= relational
relational ::= additive
additive ::= multiplicative
multiplicative ::= unary
unary ::= postfix
postfix ::= primary
primary ::= literal | identifier
```
- Creates 13-level deep PSI
- Hard to maintain
- Poor performance
- Use flat structure instead

### Missing Extends Attribute
```bnf
// DON'T DO THIS
expr ::= add_expr | mul_expr | primary
add_expr ::= expr '+' expr
mul_expr ::= expr '*' expr

// PSI has different types for each expression
// DO THIS
{
  extends(".*expr")=expr
}
```
- Without extends, deep PSI
- Each rule = new type
- Memory and performance impact
- Always use extends pattern

### Wrong Associativity
```bnf
// DON'T DO THIS
exp_expr ::= expr '^' expr  // Wrong! Should be right

// DON'T DO THIS  
assign_expr ::= expr '=' expr  // Wrong! Should be right

// DON'T DO THIS
minus_expr ::= expr '-' expr { rightAssociative=true } // Wrong!
```
- Assignment must be right
- Exponentiation usually right
- Subtraction must be left
- Test with multiple operators

### Bad Recovery Rules
```bnf
// DON'T DO THIS
expr ::= add_expr {recoverWhile=expr_recover}
expr_recover ::= true  // Consumes everything!

// DO THIS
private expr_recover ::= !(';' | '}' | ')')
```
- Over-broad recovery breaks parsing
- Consume until boundaries
- Not until anything
- Test error recovery

## Related Examples
- For basic grammar syntax → See Section 2.1
- For error recovery in expressions → See Section 2.4
- For attribute system details → See Section 3.1
- For parser generation → See Section 3.2
- For advanced PSI manipulation → See Section 4.3