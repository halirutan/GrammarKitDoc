# Expression Parsing

Expression parsing handles mathematical-like constructs where operators combine values according to specific rules. Unlike parsing simple sequences or nested structures, expression parsing must resolve complex ambiguities: when you see `2 + 3 * 4`, the parser needs to know whether to compute `(2 + 3) * 4 = 20` or `2 + (3 * 4) = 14`. Grammar-Kit provides specialized features that solve these operator precedence and associativity challenges, letting you define expression grammars that are both readable and efficient.

Think of expression parsing as teaching the computer the same rules you learned in math class: multiplication before addition, operations proceeding left to right (usually), and parentheses overriding everything else. But programming languages add complexity with assignment operators, function calls, array indexing, and custom operators that all need their proper place in the precedence hierarchy.

## Prerequisites

Before working with expression parsing, understand:

- [BNF Syntax](grammar-syntax.md) - Basic grammar notation
- [Rule Design](grammar-design.md) - Grammar structure principles
- PSI tree structure - How IntelliJ represents parsed code
- Operator precedence concepts - Mathematical expression evaluation order

## Expression Parsing Fundamentals

### Expression vs. Statement Parsing

Understanding the difference between expressions and statements is crucial for parser design. Expressions are constructs that compute and return values: `2 + 3` evaluates to `5`, `x * y` produces a result, and even complex constructs like `user.getName().length()` ultimately yield a value. Statements, on the other hand, perform actions that change program state: they assign variables, control flow with loops and conditionals, or invoke procedures for their side effects.

This distinction matters because expressions can appear within other expressions (creating the precedence challenges we're addressing), while statements typically cannot. You can write `x = 2 + (3 * 4)` because arithmetic expressions nest, but you cannot write `x = (if (true) 5 else 6)` in most languages because if-statements don't produce values. Some languages blur this line by making everything an expression, but the parser still needs different strategies for each construct type.

```bnf
root ::= statement*
statement ::= expr ';'
  | assignment ';'

assignment ::= id '=' expr

expr ::= add_expr | mul_expr | primary
// expressions produce values

primary ::= number | id | '(' expr ')'
```

In your grammar, this distinction appears clearly. Statements require terminators like semicolons and form the top-level structure of your program. Expressions nest within statements (as in `return 2 + 3;`) and within other expressions (as in `array[index + 1]`). Most languages treat assignments as statements to avoid confusing constructs like `if (x = 5)` where the programmer might have meant comparison `==` instead of assignment `=`.

### Operator Types and Precedence

Before diving into Grammar-Kit's syntax, let's understand what we're building. Operator precedence determines the order of operations, just like PEMDAS (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction) from mathematics. When the parser sees `2 + 3 * 4`, precedence rules ensure multiplication happens first, giving us `2 + 12 = 14` rather than `5 * 4 = 20`.

Grammar-Kit implements precedence through rule ordering: rules listed first in your grammar have lower precedence and are evaluated last. This might seem backwards at first, but it matches how recursive descent parsers naturally work, starting with the loosest-binding operations and drilling down to the tightest. Here's how Grammar-Kit supports all standard operator types:

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

In this grammar, `add_expr` appears before `mul_expr`, meaning addition has lower precedence than multiplication. The parser will try to match multiplication first when building the parse tree. Unary operators like negation (`-x`) appear even later, giving them higher precedence than binary operations. This ordering ensures `-2 * 3` is parsed as `(-2) * 3` rather than `-(2 * 3)`. Parentheses in `primary_expr` override all precedence rules, letting users explicitly control evaluation order.

The `extends(".*expr")=expr` attribute is crucial here. Without it, your PSI tree would have different node types for each expression kind (AddExpr, MulExpr, etc.), creating deep nesting. With this attribute, all expression nodes share the same PSI type, resulting in a flatter, more efficient tree structure that's easier to traverse and analyze.

### Expression Grammar Patterns

Grammar-Kit's expression parsing is built on a priority-based system that transforms your grammar rules into an efficient precedence-climbing parser. When you structure your expression rules properly, Grammar-Kit generates optimized parsing code that handles complex precedence relationships without the deep recursion of naive implementations.

The key insight is that operator precedence increases from top to bottom in your grammar file. Think of it as defining layers of operations, where each layer can contain operations from all the layers below it. The parser automatically generates a priority table in comments to show you exactly how it interprets your precedence rules:

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

The generated priority table shows that assignment (priority 0) binds most loosely, while primary expressions (priority 4) bind most tightly. When parsing `a = b + c * d`, the parser recognizes this as `a = (b + (c * d))` based on these priorities.

The `extraRoot` attribute marks expression boundaries, telling Grammar-Kit that this rule represents the top-level entry point for expression parsing. This helps the parser generator optimize the expression parsing code and provides better error recovery at expression boundaries.

## Implementing Precedence

### Traditional Precedence Climbing

The traditional approach to precedence parsing creates explicit nesting levels that mirror the precedence hierarchy. This method, familiar from many compiler textbooks, directly encodes precedence relationships in the grammar structure. Each precedence level becomes a separate rule that can only reference higher-precedence rules:

```bnf
expr ::= term ('+' term | '-' term)*
term ::= factor ('*' factor | '/' factor)*
factor ::= unary | primary
unary ::= '-' factor | '+' factor
primary ::= number | '(' expr ')'
```

Each level handles specific operators with lower grammar levels having higher precedence. The `expr` rule handles addition and subtraction, but when it needs an operand, it calls `term`. This forces multiplication and division to be parsed first. Similarly, `term` calls `factor`, ensuring unary operators bind tighter than binary ones.

While this approach is conceptually clear and maps directly to precedence rules, it has a significant drawback: it creates deep PSI trees with many intermediate nodes. Parsing `2 + 3 * 4` generates nodes for expr, term, factor, and primary at various levels, even though we ultimately just want to represent addition and multiplication operations. This depth impacts performance, complicates tree traversal, and makes the PSI harder to work with in IDE features.

### Layer-Based Approach

Grammar-Kit's layer-based approach revolutionizes expression parsing by using private groups to organize operators of the same precedence. Instead of creating intermediate rules that exist only to establish precedence, this pattern groups related operators together and lets Grammar-Kit's priority system handle the precedence relationships. This approach is both more maintainable and more efficient:

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

The magic happens through the combination of private groups and the `extends` attribute. Private groups (`add_group`, `mul_group`) organize operators of the same priority without creating nodes in the PSI tree. They exist only in the grammar to tell the parser which operators belong together. When you have both addition and subtraction at the same precedence level, you group them in `add_group` rather than creating separate precedence levels.

The `extends(".*expr")=expr` attribute ensures all expression types (`plus_expr`, `minus_expr`, `mul_expr`, etc.) appear in the PSI as generic `expr` nodes. This creates a flat PSI structure where `2 + 3 * 4` generates just three nodes (two operators and their operands) rather than the deeply nested structure from traditional parsing. The result is cleaner, more maintainable code that performs better and is easier to analyze.

### Priority Attributes and Tables

Understanding how Grammar-Kit assigns priorities helps you debug precedence issues and optimize your grammar. When Grammar-Kit processes your expression rules, it assigns a priority number to each alternative in your main expression rule. These priorities drive a sophisticated parsing algorithm that efficiently handles operator precedence without deep recursion.

The parser generates a priority table in comments showing the exact precedence assignments:

```bnf
expr ::= assign_expr    // priority 0
  | add_group          // priority 1
  | mul_group          // priority 2
  | unary_expr         // priority 3
  | primary_expr       // priority 4
```

Lower priority numbers mean lower precedence (evaluated last), which might seem counterintuitive but makes sense when you consider how the parser works. The generated parser uses a priority-driven while loop in the `expr_0` method that starts by trying to match the lowest-priority operators first. If it finds an addition operator, it knows it needs to parse the right operand with higher priority to ensure multiplication happens first.

This priority system is why rule order matters so much in Grammar-Kit expression grammars. Moving a rule up or down in your expression alternatives changes its priority and thus its precedence. The parser generator turns this simple ordering into efficient code that handles complex expressions without backtracking or excessive recursion.

## Associativity Control

### Left Associative Operators

Associativity determines how operators of the same precedence combine. When you write `5 - 3 - 1`, should it be `(5 - 3) - 1 = 1` or `5 - (3 - 1) = 3`? For arithmetic operators, we expect left-to-right evaluation, giving us the first interpretation. This left associativity is so common that Grammar-Kit makes it the default behavior.

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

The `left` modifier enables an optimization called left recursion, which creates flat PSI trees for efficient chain parsing. Instead of building nested nodes for `1 + 2 + 3 + 4`, left recursion produces a flat structure that's faster to parse and traverse. This optimization is particularly valuable for long chains of operations, like concatenating many strings or adding many numbers.

### Right Associative Operators

Some operators naturally associate right-to-left. The classic example is assignment: when you write `a = b = c = 5`, you expect `c` to get 5 first, then `b` to get `c`'s value, and finally `a` to get `b`'s value. This right-to-left evaluation ensures all variables end up with the value 5. Exponentiation follows the same pattern: `2^3^2` means `2^(3^2) = 2^9 = 512`, not `(2^3)^2 = 8^2 = 64`.

Assignment and exponentiation typically parse right-to-left:

```bnf
// Assignment and exponentiation
assign_expr ::= expr '=' expr { rightAssociative=true }
// a=b=c parsed as a=(b=c)

exp_expr ::= expr '^' expr { rightAssociative=true }
// 2^3^4 parsed as 2^(3^4)
```

The `rightAssociative` attribute changes parsing direction for specific operators. When Grammar-Kit sees this attribute, it generates different parsing code that builds the parse tree from right to left. This ensures mathematical conventions are preserved and assignment chains work as programmers expect.

### Non-Associative Operators

Some operators make no sense when chained. In mathematics and most programming languages, writing `a < b < c` is either an error or has special meaning different from two separate comparisons. These non-associative operators require special grammar treatment to prevent confusing constructs:

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

The grammar structure prevents comparison chaining by ensuring comparison expressions cannot appear as operands of other comparisons. If users want to check multiple conditions, they must use logical operators (`a < b && b < c`) or parentheses to make their intent clear. This design choice prevents subtle bugs where `a < b < c` might be misunderstood as checking whether `b` is between `a` and `c`.

### Mixed Associativity

Real programming languages combine operators with different associativity rules in the same expression grammar. This complexity reflects the diverse operations languages support: assignment flows right-to-left, arithmetic goes left-to-right, and comparisons don't chain at all. Grammar-Kit handles this elegantly by letting you specify associativity per operator:

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

Each operator can have its own associativity rule without affecting others at different precedence levels. The parser handles mixed types seamlessly, ensuring that `a = b + c * d` still respects multiplication's higher precedence while also handling assignment's right associativity. This flexibility lets you model real language semantics accurately while keeping your grammar readable and maintainable.

## Expression Optimization

### Avoiding Deep PSI Trees

The structure of your PSI tree directly impacts IDE performance. Every node in the tree consumes memory, and deep nesting makes traversal slower. When code completion needs to understand an expression's type or when refactoring needs to analyze data flow, a deep PSI tree means more recursive calls and slower operations. Grammar-Kit provides several techniques to keep your PSI trees flat and efficient.

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

The "bad" example creates six levels of indirection just to parse a simple number. Each level becomes a node in the PSI tree, even though they carry no semantic information. The "good" example defines operators directly at the expression level, creating nodes only for actual operations. This flatter structure parses faster, uses less memory, and makes PSI traversal more efficient.

The key insight is that precedence doesn't require deep nesting. Grammar-Kit's priority system handles precedence through rule ordering, so you can keep your PSI structure flat while still parsing expressions correctly.

### Using Extends for Flat Structure

The `extends` attribute is Grammar-Kit's secret weapon for PSI optimization. By default, each grammar rule generates its own PSI element type. This means `plus_expr`, `minus_expr`, and `mul_expr` would create PlusExpr, MinusExpr, and MulExpr nodes in your PSI tree. For complex expressions, this diversity of node types complicates analysis and slows traversal.

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

With `extends(".*expr")=expr`, all rules matching the pattern `.*expr` generate the same PSI element type: `expr`. Your PSI tree contains only generic expression nodes, making traversal simpler and more efficient. Instead of checking for multiple node types when analyzing expressions, IDE features can work with a single, unified type.

Fake rules like `fake ref_expr` define PSI interfaces without creating parsing rules. They establish a common structure that multiple concrete rules can implement. The `elementType` attribute takes this further by letting different parsing rules share the exact same PSI type. Both `simple_ref_expr` and `qualified_expr` appear in the PSI as `ref_expr` nodes, even though they parse different syntax. This technique is invaluable for creating clean APIs for your PSI while maintaining parsing flexibility.

### The Expression Parsing Idiom

After years of evolution, the Grammar-Kit community has developed a standard pattern that combines all expression parsing optimizations into a clean, efficient idiom. This pattern has proven itself across numerous language implementations and represents the best practice for expression parsing in Grammar-Kit. Understanding this idiom will save you from reinventing solutions to common problems:

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

This idiom achieves multiple optimizations simultaneously. The `extends` attribute creates a flat PSI, private groups organize precedence levels cleanly, and `extraRoot` marks the expression boundary for better error recovery. The `consumeTokenMethod="consumeTokenFast"` attribute tells Grammar-Kit to skip creating PSI nodes for operator tokens themselves, further reducing tree size.

The pattern supports two styles for defining operators. Left recursion (`left plus_expr ::= plus_op factor`) creates the most efficient parsing for left-associative operators, especially in chains. The binary style (`binary_plus ::= expr '+' expr`) is simpler to read and works well for all operators. Choose based on your performance needs and grammar complexity.

### Binary and N-ary Operations

Not all operators combine exactly two operands. While addition is typically binary (`a + b`), some operations naturally handle multiple operands in a single expression. Grammar-Kit distinguishes between binary operations (exactly two operands) and N-ary operations (two or more operands), providing specialized syntax for each:

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

The key to N-ary operations is the plus modifier after parentheses: `('**' expr) +`. This syntax tells Grammar-Kit to parse `a**b**c**d` as a single N-ary exponentiation node with four operands, rather than nested binary operations. This representation can be more efficient and better matches the semantic meaning of operations that naturally chain.

N-ary syntax is particularly useful for operations like string concatenation, where `"a" + "b" + "c" + "d"` is conceptually a single operation joining multiple strings. The parser can optimize these chains, and your PSI visitors can handle all operands in one pass rather than recursively traversing binary nodes.

## Complex Expressions

### Mixing Operator Types

Modern programming languages aren't limited to simple binary arithmetic. They combine prefix operators (appearing before their operand, like `-x` or `!flag`), infix operators (between operands, like `a + b`), and postfix operators (after their operand, like `x++` or `array[i]`). Grammar-Kit handles all these operator types within a unified expression grammar:

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

The organization into prefix, infix, and postfix groups isn't just for clarity, it reflects how these operators interact. Prefix operators typically bind tighter than infix operators (so `-a + b` means `(-a) + b`), while postfix operators often bind even tighter (so `a++.field` means `(a++).field`). By grouping operators by both type and precedence level, you create a grammar that's both correct and maintainable.

This unified approach means the parser can handle complex expressions like `-array[index]++ + value` correctly, applying operators in the right order: first the array indexing, then the postfix increment, then the prefix negation, and finally the addition.

### Ternary Operators

Ternary operators present unique parsing challenges because they involve three or more operands with separators between them. The classic conditional operator (`a ? b : c`) must ensure the `?` and `:` are parsed as a unit, not as independent operators. Grammar-Kit provides several techniques for handling these multi-part operators:

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

Ternary operators are typically right associative, meaning `a ? b : c ? d : e` parses as `a ? b : (c ? d : e)`. This right-to-left grouping matches how programmers think about nested conditionals. The `methods` attribute adds custom validation methods to the generated PSI, letting you implement semantic checks like ensuring the condition expression is boolean or that both branches have compatible types.

The between operator shows how Grammar-Kit handles operators with multiple keywords. By using `BETWEEN` and `AND` as delimiters, you create a natural syntax while maintaining proper precedence. The `testExpr="expr[0]"` method gives you programmatic access to the first expression for validation.

### Function Calls and Indexing

Member access operations (method calls, field access, array indexing) form the backbone of object-oriented and structured programming. These operations typically bind very tightly, tighter than any arithmetic operator, because expressions like `array[i] + 1` must index the array before adding, not add to the index. Getting their precedence wrong leads to confusing parse trees and incorrect program interpretation:

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

Function calls bind tighter than arithmetic operators, ensuring `f(a) + b` calls the function before adding, not passing `a + b` as an argument. The pin attribute on the opening parenthesis ensures proper error recovery: once the parser sees `f(`, it commits to parsing a function call even if the arguments are malformed. This prevents cascading errors in IDE features.

Left recursion is essential for method chaining. When parsing `obj.method1().method2().field`, left recursion builds a flat chain of member access nodes rather than deep nesting. This structure makes it easier to implement features like "go to definition" or type inference, where you need to traverse the chain from left to right.

### Type Constraints and Contextual Expressions

Modern languages increasingly blur the line between expressions and types, introducing operators that work with type information and expressions that create new scopes or contexts. These constructs require careful precedence design to avoid ambiguity while maintaining intuitive syntax:

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

Type operators typically sit above arithmetic but below member access, so `x as String.length` parses as `(x as String).length`, not `x as (String.length)`. This placement feels natural to programmers who expect type operations to happen before property access but after mathematical calculations.

Lambda and let expressions bind very loosely, allowing maximum flexibility in their bodies. When you write `let x = a + b in x * x`, the loose binding ensures the entire `a + b` expression is captured as the binding value, and the entire `x * x` expression becomes the body. This precedence design lets programmers write natural code without excessive parentheses while maintaining clear boundaries between the binding and the body.

## Common Patterns and Anti-Patterns

### Expression with Statements

While expressions compute values, not all expressions make sense as standalone statements. Writing `5 + 3;` as a statement is legal in many languages but meaningless, the computed value is discarded. Good language design restricts which expressions can appear as statements, guiding programmers toward meaningful code:

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

By limiting statement expressions to those with side effects (assignments that change variables, calls that might perform I/O, increments that modify state), you help programmers avoid meaningless code. This restriction also improves error messages: instead of silently accepting `x + 1;` as a statement that does nothing, the parser can suggest "Did you mean `x += 1;`?" This kind of thoughtful grammar design makes languages more learnable and less error-prone.

### Common Mistakes to Avoid

Experience has shown several patterns that seem reasonable but cause problems in practice. Deep grammar nesting creates performance and maintenance problems, each intermediate rule becomes a PSI node that slows traversal and complicates analysis. Always use the `extends` attribute for expression rules to keep your PSI flat and efficient.

Wrong associativity breaks mathematical conventions and programmer expectations. Assignment must be right associative (`a = b = 5` assigns 5 to both variables), exponentiation is typically right associative (`2^3^2` equals 512, not 64), and arithmetic operators must be left associative (`10 - 5 - 2` equals 3, not 7). Test your grammar with chains of the same operator to ensure correct associativity.

Error recovery requires balance. Recovery rules that consume too much input can skip over important code, while rules that consume too little create cascading errors. Test error recovery with malformed expressions to ensure the parser resumes at sensible boundaries like semicolons or closing braces.

## Next Steps

Learn about [Error Recovery](error-recovery.md) for robust expression parsing. Explore the [Attributes System](../reference/attributes.md) for advanced control. Study [Parser Generation](../code-generation/parser-generation.md) to understand the output. Review complete examples in the Grammar-Kit testData directory.

## Editorial Notes
- Missing from docs: Expression helper classes (ExpressionHelper.java, ExpressionGeneratorHelper.java) that implement the priority-based parsing algorithm
- Missing from docs: Expression info caching mechanism that optimizes repeated parsing
- Missing from docs: Operator conflict resolution strategies when multiple operators could match
- Missing from docs: The expression marker annotation (BnfExpressionMarkerAnnotator) that provides IDE support for expression rules
- Not in evidence: Specific performance metrics comparing deep vs. flat PSI trees (docs mention performance but evidence doesn't quantify it)