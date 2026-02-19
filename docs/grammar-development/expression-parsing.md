# Expression Parsing

Grammar-Kit provides a compact, Pratt-style mechanism for expression parsing that handles operator precedence and associativity through rule ordering and attributes. Instead of requiring you to manually layer rules by precedence level, Grammar-Kit auto-detects operator types from left-recursive expression rules and generates an efficient iterative parser. The result is a flat PSI tree with no redundant wrapper nodes. This approach is a [procedural rewrite of the Pratt parsing technique](http://javascript.crockford.com/tdop/tdop.html).

This page uses the [`ExprParser.bnf`](https://github.com/JetBrains/Grammar-Kit/blob/master/testData/generator/ExprParser.bnf) grammar as its running example. Before reading further, you should be comfortable with [BNF Grammar Syntax](grammar-syntax.md), particularly rule modifiers (`private`, `fake`, `left`) and the `extends` attribute.

## How Expression Parsing Works

### The Expression Root

The expression root rule lists all expression alternatives as ordered choices. Grammar-Kit auto-detects a rule as an expression root when the rule is not `private`, not `fake`, has no direct content of its own, and its FIRST set contains its own name (left recursion). Priority increases from top to bottom in the choice list, so the first alternative has the lowest priority and the last has the highest.

Private rules group operators that share the same priority level. This keeps the root rule readable without affecting the generated priority assignments. The generator produces only two methods for the root rule: `expr()` and `expr_0()`.

Here is the expression root from the `ExprParser.bnf` grammar:

```bnf
{
  extends(".*_expr")=expr                          // all *_expr rules extend expr — flat AST
  consumeTokenMethod(".*_expr|expr")="consumeTokenFast"  // skip error info in expressions
  name(".*_expr")='expression'                     // clean error messages

  tokens=[
    space='regexp:\s+'
    number='regexp:\d+(\.\d*)?'
    id='regexp:\p{Alpha}\w*'
  ]
}

// Root: wrap expressions in a loop with recovery
root ::= element *
private element ::= expr ';'? {recoverWhile=element_recover}
private element_recover ::= !('(' | '+' | '-' | '!' | id | number)

// Expression root — priority increases top to bottom
// Left recursion + empty PSI children = expression root auto-detection
expr ::= assign_expr
  | add_group
  | mul_group
  | unary_group
  | exp_expr
  | factorial_expr
  | primary_group

// Private groups for same-priority operators
private add_group ::= plus_expr | minus_expr
private mul_group ::= mul_expr | div_expr
private unary_group ::= unary_plus_expr | unary_min_expr
private primary_group ::= ref_expr | literal_expr | paren_expr

// BINARY operators — two references to root expr
assign_expr ::= expr '=' expr {rightAssociative=true}   // right-associative
plus_expr ::= expr '+' expr                              // left-associative (default)
minus_expr ::= expr '-' expr
mul_expr ::= expr '*' expr
div_expr ::= expr '/' expr

// N_ARY operator — mandatory (<op> expr)+ syntax
exp_expr ::= expr ('**' expr) +

// PREFIX operators — root expr after operator token
unary_plus_expr ::= '+' expr
unary_min_expr ::= '-' expr

// POSTFIX operator — root expr before operator token
factorial_expr ::= expr '!'

// ATOM — no reference to root expr
literal_expr ::= number
ref_expr ::= id
paren_expr ::= '(' expr ')'                             // classified as PREFIX, not ATOM
```

The `extends(".*_expr")=expr` attribute is essential. It enables AST flattening and activates the expression parsing framework. Without it, you get a deep, unwieldy PSI tree (see [PSI Tree Shape and Performance](#psi-tree-shape-and-performance)).

The generator produces a priority table as a comment in the generated parser. This table confirms the precedence assignments:

```
// Expression root: expr
// Operator priority table:
// 0: BINARY(assign_expr)
// 1: BINARY(plus_expr) BINARY(minus_expr)
// 2: BINARY(mul_expr) BINARY(div_expr)
// 3: PREFIX(unary_plus_expr) PREFIX(unary_min_expr)
// 4: N_ARY(exp_expr)
// 5: POSTFIX(factorial_expr)
// 6: ATOM(ref_expr) ATOM(literal_expr) PREFIX(paren_expr)
```

### Operator Types

Grammar-Kit auto-detects five operator types from the structure of each expression rule. You do not declare the type explicitly; the generator infers it from how the rule references the root expression.

| Type | Pattern | Example | Description |
|------|---------|---------|-------------|
| ATOM | No reference to root expr | `literal_expr ::= number` | Leaf node, no operands |
| PREFIX | Root expr after operator | `unary_min_expr ::= '-' expr` | Unary prefix |
| POSTFIX | Root expr before operator | `factorial_expr ::= expr '!'` | Unary postfix |
| BINARY | Two root expr references | `plus_expr ::= expr '+' expr` | Standard infix |
| N_ARY | Uses `(<op> expr)+` syntax | `exp_expr ::= expr ('**' expr) +` | Consumes all operands at same level |

One subtlety: `paren_expr ::= '(' expr ')'` is classified as PREFIX, not ATOM, because it does not start with `expr`. The opening parenthesis acts as the "operator" in the PREFIX pattern.

## Precedence and Associativity

### Defining Precedence

The position of an operator in the root rule's choice list determines its priority. The first alternative has priority 0 (lowest, binds loosest) and the last has the highest priority (binds tightest). To group operators at the same priority level, use a `private` rule:

```bnf
private mul_group ::= mul_expr | div_expr
```

Both `mul_expr` and `div_expr` receive the same priority because they are alternatives within one private group.

Consider the input `1 + 2 * 3`. Because `mul_expr` (priority 2) has higher priority than `plus_expr` (priority 1), the parser produces the equivalent of `1 + (2 * 3)`:

| Priority | Type | Rule | Syntax | Behavior |
|----------|------|------|--------|----------|
| 0 (lowest) | BINARY | `assign_expr` | `expr '=' expr` | Right-assoc: `a = b = c` becomes `a = (b = c)` |
| 1 | BINARY | `plus_expr` | `expr '+' expr` | Left-assoc: `a + b + c` becomes `(a + b) + c` |
| 1 | BINARY | `minus_expr` | `expr '-' expr` | Left-assoc |
| 2 | BINARY | `mul_expr` | `expr '*' expr` | Left-assoc: binds tighter than `+` |
| 2 | BINARY | `div_expr` | `expr '/' expr` | Left-assoc |
| 3 | PREFIX | `unary_plus_expr` | `'+' expr` | Unary: `+ - 3` becomes `+(-(3))` |
| 3 | PREFIX | `unary_min_expr` | `'-' expr` | Unary |
| 4 | N_ARY | `exp_expr` | `expr ('**' expr) +` | `a ** b ** c` creates a single node with 3 children |
| 5 | POSTFIX | `factorial_expr` | `expr '!'` | Postfix: `3!` |
| 6 (highest) | ATOM | `ref_expr`, `literal_expr` | `id`, `number` | Leaf nodes |
| 6 | PREFIX | `paren_expr` | `'(' expr ')'` | Grouped expression |

### Associativity

All binary operators are left-associative by default. For `plus_expr`, the input `a + b + c` parses as `(a + b) + c`:

```
PlusExpr
  PlusExpr
    RefExpr('a')
    RefExpr('b')
  RefExpr('c')
```

To make an operator right-associative, add the `rightAssociative=true` attribute:

```bnf
assign_expr ::= expr '=' expr {rightAssociative=true}
```

With this attribute, `a = b = c` parses as `a = (b = c)`:

```
AssignExpr
  RefExpr('a')
  AssignExpr
    RefExpr('b')
    RefExpr('c')
```

The `rightAssociative` attribute is a per-rule boolean (default: `false`), so different operators at different priority levels can have different associativity. For example, `assign_expr` is right-associative at priority 0 while `plus_expr` is left-associative at priority 1.

Grammar-Kit has no explicit non-associativity attribute. Comparison operators at the same priority level approximate non-associative behavior, but they still parse left-associatively. For example, `conditional_expr ::= expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr` parses `a < b < c` as `(a < b) < c`.

## Complex Expression Patterns

### Ternary and Multi-Token Operators

The operator part of an expression rule can contain any valid BNF expression, including choices, sequences, and optional elements.

A ternary operator like the elvis/conditional expression is treated as BINARY with a "tail." The parser matches the first `expr ? expr` as a binary structure, then parses the `: expr` tail:

```bnf
elvis_expr ::= expr '?' expr ':' expr
```

Multi-token operators work the same way. The tokens between the two `expr` references form the operator:

```bnf
// Multi-token operator
is_not_expr ::= expr IS NOT expr

// Choice operator — multiple comparison operators at same priority
conditional_expr ::= expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr
```

### Function Calls and Qualification

Function calls are modeled as postfix operators with a type-constrained left operand. Instead of using the generic `expr` on the left, `call_expr` uses `ref_expr` to restrict which expressions can be "called":

```bnf
// call_expr uses ref_expr (not generic expr) as left operand
call_expr ::= ref_expr arg_list
arg_list ::= '(' [!')' expr (',' expr) *] ')' {pin(".*")=1}
```

The generated code checks that the left sibling is a `REF_EXPR` node before applying the call expression rule.

For member access (qualification), a `fake` rule defines the shared PSI interface while concrete rules map to the same element type:

```bnf
// fake rule defines the PSI interface
fake ref_expr ::= expr? '.' identifier

// simple reference and qualification share the same elementType
simple_ref_expr ::= identifier {extends=ref_expr elementType=ref_expr}
qualification_expr ::= expr '.' identifier {extends=ref_expr elementType=ref_expr}
```

Both `simple_ref_expr` and `qualification_expr` produce `REF_EXPR` element type nodes. The `fake ref_expr` rule generates PSI interface methods (`getExpr()`, `getIdentifier()`) but no parsing code. For more on `fake` rules and PSI interfaces, see [PSI Customization](../code-generation/psi-customization.md).

### Narrowing Operand Types

You can restrict what expressions are accepted as operands by referencing a specific expression rule or private group instead of the generic `expr`:

```bnf
// between_expr restricts operands to add-level priority or higher
between_expr ::= expr BETWEEN add_group AND add_group
```

Using `add_group` instead of `expr` for the range operands means only expressions at add-level priority or above are accepted. The input `a BETWEEN 1+2 AND 3*4` works, but `a BETWEEN b=c AND d` does not because assignment has lower priority than the add group.

### Multiple Expression Roots

A grammar can have multiple independent expression hierarchies. Each root generates its own pair of methods. The `extraRoot=true` attribute marks an expression root for inclusion in the `parse_extra_roots()` method:

```bnf
{
  extends(".*_expr")=expr
  extends(".*_type")=type
}

// First expression root
expr ::= add_expr | literal_expr {extraRoot=true}
add_expr ::= expr '+' expr
literal_expr ::= number

// Second expression root (must not intersect with first)
type ::= array_type | simple_type
array_type ::= type '[' ']'
simple_type ::= id
```

Expression hierarchies must not intersect. No rule can participate in more than one expression root.

## PSI Tree Shape and Performance

The `extends` attribute is what makes expression parsing produce a clean, flat PSI tree. Without it, every expression wraps its operands in intermediate nodes. With it, redundant nodes are collapsed and the root expression rule never appears in the AST.

Consider the input `42` parsed by a grammar without `extends`:

```
FileNode
  Expr
    MulExpr (or wrapping node)
      LiteralExpr
        number: '42'
```

The same input with `extends(".*_expr")=expr`:

```
FileNode
  LiteralExpr
    number: '42'
```

For a more complex input like `1 + 2 * 3`, the flat tree preserves the correct precedence structure without unnecessary nesting:

```
FileNode
  PlusExpr
    LiteralExpr
      number: '1'
    MulExpr
      LiteralExpr
        number: '2'
      LiteralExpr
        number: '3'
```

Two additional attributes improve the developer experience for expression grammars. The `consumeTokenMethod` attribute switches to a faster token matching method that skips error reporting information. In expression rules, recording every expected operator at every position adds overhead with no practical benefit, since no one really needs to know that `+`, `-`, `*`, `/` are expected at any offset:

```bnf
consumeTokenMethod(".*_expr|expr")="consumeTokenFast"
```

The `name` attribute replaces long token lists in error messages with a readable name. Instead of `'+', '-', '*', '/' expected`, the user sees `<expression> expected`:

```bnf
name(".*_expr")='expression'
```

The IDE also provides a Quick Documentation feature for expression rules. Press ++ctrl+q++ (++cmd+j++ on macOS) on any expression rule to see the priority table with operator types and the current rule highlighted. This is useful for verifying that your precedence assignments are correct.

### The Traditional Approach

Grammar-Kit also supports a traditional approach using the `left` modifier and manual precedence layering. Each precedence level is a separate rule chain:

```bnf
{
  extends(".*expr")=expr
  name(".*expr")='expression'
  tokens=[
    SEMI=';'
    EQ='='
    LP='('
    RP=')'
    space='regexp:\s+'
    number='regexp:\d+(\.\d*)?'
    id='regexp:\p{Alpha}\w*'
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"
  ]
}

// Root with property recovery
root ::= root_item *
private root_item ::= !<<eof>> property ';' {pin=1 recoverWhile=property_recover}
property ::= id '=' expr {pin=2}
private property_recover ::= !(';' | id '=')

// Expression with manual layering
// Each precedence level is a separate rule chain
expr ::= factor plus_expr *
left plus_expr ::= plus_op factor                // add/subtract (lowest)
private plus_op ::= '+' | '-'
private factor ::= primary mul_expr *
left mul_expr ::= mul_op primary                 // multiply/divide (higher)
private mul_op ::= '*' | '/'
private primary ::= primary_inner factorial_expr ?
left factorial_expr ::= '!'                      // factorial (highest unary)
private primary_inner ::= literal_expr | ref_expr | paren_expr

// Atoms
paren_expr ::= '(' expr ')' {pin=1}
ref_expr ::= id
literal_expr ::= number | string
```

This approach is more verbose and requires you to manually wire each precedence level. The Pratt approach is recommended for new grammars because it is more compact, easier to maintain, and produces the same flat PSI tree. The traditional approach may still appear in older grammars.

For details on the `left` modifier and other rule modifiers, see [BNF Grammar Syntax](grammar-syntax.md). For error recovery with `pin` and `recoverWhile` (used in the `element` wrapper at the top of expression grammars), see [Error Recovery](error-recovery.md).
