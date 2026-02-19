# Expression Parsing

Expression parsing handles constructs where operators combine values according to precedence and associativity rules. When parsing `2 + 3 * 4`, the parser must determine whether to compute `(2 + 3) * 4 = 20` or `2 + (3 * 4) = 14`. Grammar-Kit provides features for defining operator precedence and associativity to create readable and efficient expression grammars.

Expression parsing implements standard mathematical rules: multiplication before addition, left-to-right evaluation for most operators, and parentheses for explicit grouping. Programming languages extend these concepts with assignment operators, function calls, array indexing, and custom operators that require careful precedence design.

## Prerequisites

Before working with expression parsing, understand:

- [BNF Syntax](grammar-syntax.md) - Basic grammar notation
- [Rule Design](grammar-design.md) - Grammar structure principles
- PSI tree structure - How IntelliJ represents parsed code
- Operator precedence concepts - Mathematical expression evaluation order

## Expression Parsing Fundamentals

### Expression vs. Statement Parsing

Expressions and statements serve different purposes in language design. Expressions compute and return values: `2 + 3` evaluates to `5`, `x * y` produces a result, and `user.getName().length()` yields a value. Statements perform actions that change program state: they assign variables, control flow with loops and conditionals, or invoke procedures for side effects.

This distinction affects parser design because expressions can nest within other expressions, creating precedence challenges, while statements typically cannot. You can write `x = 2 + (3 * 4)` because arithmetic expressions nest, but you cannot write `x = (if (true) 5 else 6)` in most languages because if-statements don't produce values. Some languages treat everything as expressions, but parsers still handle these constructs differently.

```bnf
root ::= statement*
statement ::= expr ';'
  | assignment ';'

assignment ::= id '=' expr

expr ::= add_expr | mul_expr | primary
// expressions produce values

primary ::= number | id | '(' expr ')'
```

In grammars, statements require terminators like semicolons and form the top-level program structure. Expressions nest within statements (as in `return 2 + 3;`) and within other expressions (as in `array[index + 1]`). Most languages treat assignments as statements to prevent ambiguous constructs like `if (x = 5)` where the programmer might have intended comparison `==` instead of assignment `=`.

### Operator Types and Precedence

Operator precedence determines evaluation order, following standard mathematical rules (PEMDAS: Parentheses, Exponents, Multiplication/Division, Addition/Subtraction). When parsing `2 + 3 * 4`, precedence rules ensure multiplication happens first, yielding `2 + 12 = 14` rather than `5 * 4 = 20`.

Grammar-Kit implements precedence through rule ordering: rules listed first have lower precedence and are evaluated last. This ordering matches recursive descent parser behavior, starting with loosest-binding operations and proceeding to tighter-binding ones. Grammar-Kit supports all standard operator types:

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

In this grammar, `add_expr` appears before `mul_expr`, giving addition lower precedence than multiplication. The parser matches multiplication first when building the parse tree. Unary operators like negation (`-x`) appear later, giving them higher precedence than binary operations. This ordering ensures `-2 * 3` parses as `(-2) * 3` rather than `-(2 * 3)`. Parentheses in `primary_expr` override all precedence rules for explicit evaluation control.

The `extends(".*expr")=expr` attribute prevents deep PSI nesting. Without it, the PSI tree would contain different node types for each expression kind (AddExpr, MulExpr, etc.). With this attribute, all expression nodes share the same PSI type, creating a flatter, more efficient tree structure.

### Expression Grammar Patterns

Grammar-Kit uses a priority-based system that transforms grammar rules into an efficient precedence-climbing parser. Proper expression rule structure enables Grammar-Kit to generate optimized parsing code that handles complex precedence relationships without deep recursion.

Operator precedence increases from top to bottom in the grammar file. Each precedence layer can contain operations from all layers below it. The parser generates a priority table in comments showing the precedence interpretation:

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
```

The priority table shows assignment (priority 0) binding most loosely and primary expressions (priority 4) binding most tightly. When parsing `a = b + c * d`, the parser produces `a = (b + (c * d))` based on these priorities.

The `extraRoot` attribute marks expression boundaries, indicating the top-level entry point for expression parsing. This enables parser optimization and improves error recovery at expression boundaries.

## Implementing Precedence

### Traditional Precedence Climbing

The traditional approach creates explicit nesting levels that mirror the precedence hierarchy. This method directly encodes precedence relationships in the grammar structure. Each precedence level becomes a separate rule that can only reference higher-precedence rules:

```bnf
expr ::= term ('+' term | '-' term)*
term ::= factor ('*' factor | '/' factor)*
factor ::= unary | primary
unary ::= '-' factor | '+' factor
primary ::= number | '(' expr ')'
```

Each level handles specific operators, with lower grammar levels having higher precedence. The `expr` rule handles addition and subtraction but calls `term` for operands, forcing multiplication and division to parse first. Similarly, `term` calls `factor`, ensuring unary operators bind tighter than binary ones.

While conceptually clear, this approach creates deep PSI trees with many intermediate nodes. Parsing `2 + 3 * 4` generates nodes for expr, term, factor, and primary at various levels, even though only addition and multiplication operations need representation. This depth impacts performance and complicates PSI traversal in IDE features.

### Layer-Based Approach

Grammar-Kit's layer-based approach uses private groups to organize operators of the same precedence. Instead of creating intermediate rules solely for precedence, this pattern groups related operators and uses Grammar-Kit's priority system for precedence relationships. This approach improves both maintainability and efficiency:

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

Private groups (`add_group`, `mul_group`) organize operators of the same priority without creating PSI nodes. They exist only in the grammar to indicate which operators share precedence. When addition and subtraction have the same precedence level, they group in `add_group` rather than requiring separate precedence levels.

The `extends(".*expr")=expr` attribute ensures all expression types (`plus_expr`, `minus_expr`, `mul_expr`, etc.) appear in the PSI as generic `expr` nodes. This creates a flat PSI structure where `2 + 3 * 4` generates just three nodes (two operators and their operands) rather than deeply nested structures. The result improves performance and simplifies analysis.

### Priority Attributes and Tables

Understanding Grammar-Kit's priority assignment helps debug precedence issues and optimize grammars. Grammar-Kit assigns a priority number to each alternative in the main expression rule. These priorities drive the parsing algorithm that handles operator precedence without deep recursion.

The parser generates a priority table in comments showing the exact precedence assignments:

```bnf
expr ::= assign_expr    // priority 0
  | add_group          // priority 1
  | mul_group          // priority 2
  | unary_expr         // priority 3
  | primary_expr       // priority 4
```

Lower priority numbers indicate lower precedence (evaluated last). The generated parser uses a priority-driven while loop in the `expr_0` method, starting with lowest-priority operators. When finding an addition operator, it parses the right operand with higher priority to ensure multiplication happens first.

Rule order determines precedence in Grammar-Kit expression grammars. Moving a rule up or down in expression alternatives changes its priority and precedence. The parser generator converts this ordering into efficient code that handles complex expressions without backtracking or excessive recursion.

## Associativity Control

### Left Associative Operators

Associativity determines how operators of the same precedence combine. The expression `5 - 3 - 1` can be evaluated as `(5 - 3) - 1 = 1` or `5 - (3 - 1) = 3`. Arithmetic operators use left-to-right evaluation, yielding the first interpretation. Grammar-Kit makes left associativity the default behavior.

Most operators are left associative by default, parsing from left to right:

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

The `left` modifier enables left recursion optimization, creating flat PSI trees for efficient chain parsing. Instead of building nested nodes for `1 + 2 + 3 + 4`, left recursion produces a flat structure. This optimization benefits long operation chains, such as string concatenation or numeric addition sequences.

### Right Associative Operators

Some operators associate right-to-left. Assignment demonstrates this: `a = b = c = 5` evaluates as `c` gets 5, then `b` gets `c`'s value, then `a` gets `b`'s value, ensuring all variables receive 5. Exponentiation follows the same pattern: `2^3^2` means `2^(3^2) = 2^9 = 512`, not `(2^3)^2 = 8^2 = 64`.

Assignment and exponentiation typically parse right-to-left:

```bnf
// Assignment and exponentiation
assign_expr ::= expr '=' expr { rightAssociative=true }
// a=b=c parsed as a=(b=c)

exp_expr ::= expr '^' expr { rightAssociative=true }
// 2^3^4 parsed as 2^(3^4)
```

The `rightAssociative` attribute changes parsing direction for specific operators. Grammar-Kit generates different parsing code that builds the parse tree from right to left, preserving mathematical conventions and ensuring assignment chains work correctly.

### Non-Associative Operators

Some operators cannot be chained meaningfully. In most programming languages, `a < b < c` is either an error or has special meaning different from two separate comparisons. Non-associative operators require special grammar treatment:

```bnf
// Comparison operators
compare_expr ::= expr '<' expr
  | expr '>' expr
  | expr '==' expr

// Prevent chaining: a < b < c is error
expr ::= compare_expr
  | add_expr
  | primary
```

The grammar structure prevents comparison chaining by ensuring comparison expressions cannot appear as operands of other comparisons. To check multiple conditions, users must use logical operators (`a < b && b < c`) or parentheses. This design prevents bugs where `a < b < c` might be misinterpreted as checking whether `b` is between `a` and `c`.

### Mixed Associativity

Programming languages combine operators with different associativity rules in the same expression grammar. Assignment flows right-to-left, arithmetic goes left-to-right, and comparisons don't chain. Grammar-Kit allows per-operator associativity specification:

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

Each operator can have its own associativity rule without affecting others at different precedence levels. The parser handles mixed types correctly, ensuring `a = b + c * d` respects multiplication's higher precedence while handling assignment's right associativity. This flexibility enables accurate language modeling while maintaining grammar readability.

## Expression Optimization

### Avoiding Deep PSI Trees

PSI tree structure directly impacts IDE performance. Each node consumes memory, and deep nesting slows traversal. Code completion and refactoring operations require more recursive calls with deep PSI trees. Grammar-Kit provides techniques to keep PSI trees flat and efficient.

Deep nesting creates performance problems:

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

The "bad" example creates six levels of indirection to parse a simple number. Each level becomes a PSI node without semantic value. The "good" example defines operators directly at the expression level, creating nodes only for actual operations. This flatter structure improves parsing speed, reduces memory usage, and simplifies PSI traversal.

Precedence doesn't require deep nesting. Grammar-Kit's priority system handles precedence through rule ordering, allowing flat PSI structures while maintaining correct expression parsing.

### Using Extends for Flat Structure

The `extends` attribute optimizes PSI structure. By default, each grammar rule generates its own PSI element type. This means `plus_expr`, `minus_expr`, and `mul_expr` would create PlusExpr, MinusExpr, and MulExpr nodes in your PSI tree. For complex expressions, this diversity of node types complicates analysis and slows traversal.

The `extends` attribute changes this behavior fundamentally:

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

With `extends(".*expr")=expr`, all rules matching the pattern `.*expr` generate the same PSI element type: `expr`. The PSI tree contains only generic expression nodes, simplifying traversal. IDE features work with a single, unified type instead of checking multiple node types.

Fake rules like `fake ref_expr` define PSI interfaces without parsing rules. They establish common structures that multiple concrete rules implement. The `elementType` attribute allows different parsing rules to share the same PSI type. Both `simple_ref_expr` and `qualified_expr` appear as `ref_expr` nodes in the PSI, despite parsing different syntax. This technique creates clean PSI APIs while maintaining parsing flexibility.

### The Expression Parsing Idiom

Grammar-Kit provides a standard pattern that combines all expression parsing optimizations. This pattern represents the recommended approach for expression parsing. Understanding this idiom helps you implement efficient expression parsers:

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

This idiom combines multiple optimizations. The `extends` attribute creates a flat PSI, private groups organize precedence levels, and `extraRoot` marks expression boundaries for error recovery. The `consumeTokenMethod="consumeTokenFast"` attribute prevents PSI node creation for operator tokens, further reducing tree size.

The pattern supports two operator definition styles. Left recursion (`left plus_expr ::= plus_op factor`) provides efficient parsing for left-associative operators in chains. The binary style (`binary_plus ::= expr '+' expr`) offers simpler syntax for all operators. Choose based on performance requirements and grammar complexity.

### Binary and N-ary Operations

Not all operators combine exactly two operands. While addition is typically binary (`a + b`), some operations handle multiple operands in a single expression. Grammar-Kit distinguishes between binary operations (exactly two operands) and N-ary operations (two or more operands):

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

The plus modifier after parentheses (`('**' expr) +`) defines N-ary operations. This syntax parses `a**b**c**d` as a single N-ary exponentiation node with four operands, rather than nested binary operations. This representation improves efficiency and matches the semantic meaning of chainable operations.

N-ary syntax suits operations like string concatenation, where `"a" + "b" + "c" + "d"` represents a single operation joining multiple strings. The parser optimizes these chains, and PSI visitors handle all operands in one pass instead of recursively traversing binary nodes.

## Complex Expressions

### Mixing Operator Types

Programming languages combine prefix operators (before operands, like `-x` or `!flag`), infix operators (between operands, like `a + b`), and postfix operators (after operands, like `x++` or `array[i]`). Grammar-Kit handles all operator types within a unified expression grammar:

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

Organizing operators into prefix, infix, and postfix groups reflects their interaction patterns. Prefix operators typically bind tighter than infix operators (`-a + b` means `(-a) + b`), while postfix operators bind even tighter (`a++.field` means `(a++).field`). Grouping by type and precedence creates correct, maintainable grammars.

This unified approach handles complex expressions like `-array[index]++ + value` correctly, applying operators in order: array indexing, postfix increment, prefix negation, then addition.

### Ternary Operators

Ternary operators involve three or more operands with separators between them. The conditional operator (`a ? b : c`) must parse `?` and `:` as a unit, not as independent operators. Grammar-Kit provides techniques for handling multi-part operators:

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

Ternary operators are typically right associative: `a ? b : c ? d : e` parses as `a ? b : (c ? d : e)`. This right-to-left grouping matches nested conditional interpretation. The `methods` attribute adds custom validation methods to the generated PSI for semantic checks like type compatibility.

The between operator demonstrates handling operators with multiple keywords. Using `BETWEEN` and `AND` as delimiters creates natural syntax while maintaining precedence. The `testExpr="expr[0]"` method provides programmatic access to the first expression for validation.

### Function Calls and Indexing

Member access operations (method calls, field access, array indexing) are fundamental to object-oriented and structured programming. These operations bind tighter than arithmetic operators because expressions like `array[i] + 1` must index the array before adding. Incorrect precedence creates confusing parse trees and misinterpretation:

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

Function calls bind tighter than arithmetic operators, ensuring `f(a) + b` calls the function before adding, not passing `a + b` as an argument. The pin attribute on the opening parenthesis ensures error recovery: once the parser sees `f(`, it commits to parsing a function call even with malformed arguments, preventing cascading errors.

Left recursion enables efficient method chaining. When parsing `obj.method1().method2().field`, left recursion builds a flat chain of member access nodes. This structure simplifies implementing features like "go to definition" or type inference that traverse chains left to right.

### Type Constraints and Contextual Expressions

Modern languages introduce operators that work with type information and expressions that create new scopes or contexts. These constructs require careful precedence design to avoid ambiguity:

```bnf
// Type annotations in expressions
typed_expr ::= expr ':' type
cast_expr ::= expr AS type
instanceof_expr ::= expr IS type

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
```

Type operators sit above arithmetic but below member access, so `x as String.length` parses as `(x as String).length`, not `x as (String.length)`. This placement matches programmer expectations: type operations before property access but after mathematical calculations.

Lambda and let expressions bind loosely, allowing flexibility in their bodies. In `let x = a + b in x * x`, loose binding captures the entire `a + b` as the binding value and `x * x` as the body. This precedence design enables natural code without excessive parentheses while maintaining clear binding boundaries.

## Common Patterns and Anti-Patterns

### Expression with Statements

Not all expressions make sense as standalone statements. While `5 + 3;` may be syntactically valid, the computed value is discarded, making it meaningless. Language design should restrict which expressions can appear as statements:

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

Limiting statement expressions to those with side effects (assignments, calls, increments) prevents meaningless code. This restriction improves error messages: instead of accepting `x + 1;` as a no-op statement, the parser can suggest "Did you mean `x += 1;`?" Such grammar design improves language usability and reduces errors.

### Common Mistakes to Avoid

Common mistakes include deep grammar nesting, which creates performance and maintenance problems. Each intermediate rule becomes a PSI node that slows traversal and complicates analysis. Use the `extends` attribute for expression rules to maintain flat, efficient PSI structures.

Incorrect associativity breaks conventions and expectations. Assignment must be right associative (`a = b = 5` assigns 5 to both variables), exponentiation is typically right associative (`2^3^2` equals 512, not 64), and arithmetic operators must be left associative (`10 - 5 - 2` equals 3, not 7). Test grammars with operator chains to verify associativity.

Error recovery requires balance. Over-broad recovery rules skip important code, while narrow rules create cascading errors. Test error recovery with malformed expressions to ensure parsing resumes at appropriate boundaries like semicolons or closing braces.

## Next Steps

Learn about [Error Recovery](error-recovery.md) for robust expression parsing. Explore the [Attributes System](../reference/attributes.md) for advanced control. Study [Parser Generation](../code-generation/parser-generation.md) to understand the output. Review complete examples in the Grammar-Kit testData directory.

## Editorial Notes
- Missing from docs: Expression helper classes (ExpressionHelper.java, ExpressionGeneratorHelper.java) that implement the priority-based parsing algorithm
- Missing from docs: Expression info caching mechanism that optimizes repeated parsing
- Missing from docs: Operator conflict resolution strategies when multiple operators could match
- Missing from docs: The expression marker annotation (BnfExpressionMarkerAnnotator) that provides IDE support for expression rules
- Not in evidence: Specific performance metrics comparing deep vs. flat PSI trees (docs mention performance but evidence doesn't quantify it)