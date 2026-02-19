# Examples: Expression Parsing

## Example 1: Complete Expression Grammar (Pratt/Priority Approach)

The recommended approach for expression parsing. Based on ExprParser.bnf with annotations.

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

**Generated priority table** (appears as comment in generated parser):
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

**Key points:**
- Priority 0 (assign) = lowest; priority 6 (atoms) = highest.
- All operators in a private group share the same priority level.
- The generator produces only 2 methods: `expr()` and `expr_0()`.
- `paren_expr` is classified as PREFIX because it starts with `(`, not with `expr`.

Source: ExprParser.bnf, HOWTO.md lines 121-223.

---

## Example 2: Operator Precedence Table

How different operators map to priority levels and types.

| Priority | Type | Rule | Syntax | Parsing Behavior |
|----------|------|------|--------|------------------|
| 0 (lowest) | BINARY | `assign_expr` | `expr '=' expr` | Right-assoc: `a = b = c` → `a = (b = c)` |
| 1 | BINARY | `plus_expr` | `expr '+' expr` | Left-assoc: `a + b + c` → `(a + b) + c` |
| 1 | BINARY | `minus_expr` | `expr '-' expr` | Left-assoc |
| 2 | BINARY | `mul_expr` | `expr '*' expr` | Left-assoc: binds tighter than `+` |
| 2 | BINARY | `div_expr` | `expr '/' expr` | Left-assoc |
| 3 | PREFIX | `unary_plus_expr` | `'+' expr` | Unary: `+ - 3` → `+(-(3))` |
| 3 | PREFIX | `unary_min_expr` | `'-' expr` | Unary |
| 4 | N_ARY | `exp_expr` | `expr ('**' expr) +` | N-ary: `a ** b ** c` → single node with 3 children |
| 5 | POSTFIX | `factorial_expr` | `expr '!'` | Postfix: `3!` → `factorial(3)` |
| 6 (highest) | ATOM | `ref_expr` | `id` | Leaf node |
| 6 | ATOM | `literal_expr` | `number` | Leaf node |
| 6 | PREFIX | `paren_expr` | `'(' expr ')'` | Grouped expression |

**Reading the table:**
- Higher priority = binds tighter.
- `1 + 2 * 3` → `1 + (2 * 3)` because `mul_expr` (priority 2) > `plus_expr` (priority 1).
- `a = b = c` → `a = (b = c)` because `assign_expr` has `rightAssociative=true`.
- `2 ** 3 ** 4` creates a single N_ARY node with three children (not nested binary).

Source: ExprParser.expected.java priority table, HOWTO.md lines 203-213.

---

## Example 3: PSI Tree Comparison — Deep vs Flat

### Without `extends` (Deep Tree)

```bnf
// No extends attribute
expr ::= factor plus_expr *
left plus_expr ::= ('+' | '-') factor
private factor ::= primary mul_expr *
left mul_expr ::= ('*' | '/') primary
private primary ::= literal_expr
literal_expr ::= number
```

Input: `42`

PSI tree (deep):
```
FileNode
  Expr
    MulExpr (or wrapping node)
      LiteralExpr
        number: '42'
```

Input: `1 + 2 * 3`

PSI tree (deep):
```
FileNode
  Expr
    PlusExpr
      LiteralExpr
        number: '1'
      MulExpr
        LiteralExpr
          number: '2'
        LiteralExpr
          number: '3'
```

### With `extends` (Flat Tree)

```bnf
{
  extends(".*_expr")=expr
}
// Same rules as above, but with extends
```

Input: `42`

PSI tree (flat):
```
FileNode
  LiteralExpr
    number: '42'
```

Input: `1 + 2 * 3`

PSI tree (flat):
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

**Key difference:** With `extends`, redundant wrapping nodes are collapsed. A standalone `42` is just `FileNode/LiteralExpr`, not `FileNode/Expr/LiteralExpr`. The root expression rule (`Expr`) never appears in AST.

Source: HOWTO.md lines 232-250.

---

## Example 4: Traditional Approach (left Modifier)

The older approach using manual precedence layering. From TUTORIAL.md.

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

**Comparison with Pratt approach:**
- Traditional: each precedence level is a separate rule chain (`expr` → `factor` → `primary`).
- Pratt: all operators listed in one root rule; priority determined by position.
- Traditional: more verbose but explicit about precedence structure.
- Pratt: compact and easier to maintain; recommended for new grammars.

Source: TUTORIAL.md lines 115-127, LivePreviewTutorial.bnf.

---

## Example 5: Right Associativity

```bnf
{
  extends(".*_expr")=expr
}

expr ::= assign_expr | add_group | primary_group
private add_group ::= plus_expr
private primary_group ::= literal_expr

// Right-associative: a = b = c parses as a = (b = c)
assign_expr ::= expr '=' expr {rightAssociative=true}

// Left-associative (default): a + b + c parses as (a + b) + c
plus_expr ::= expr '+' expr

literal_expr ::= number
```

**How it works:**
- For left-associative `+`: the right operand requires *higher* priority, so same-level recursion is not allowed. `a + b + c` → `(a + b) + c`.
- For right-associative `=`: the right operand allows *same-or-higher* priority, enabling same-level recursion. `a = b = c` → `a = (b = c)`.
- `rightAssociative` is a per-rule boolean attribute (default: `false`).

Source: ExprParser.bnf line 58, rightAssociative.html.

---

## Example 6: Complex Expression Patterns

### Ternary / Elvis Operator

```bnf
elvis_expr ::= expr '?' expr ':' expr
```

Treated as BINARY with a "tail" (the `: expr` part). The parser matches the first `expr ? expr` as a binary structure, then parses the `: expr` tail.

Source: ExprParser.bnf line 67.

### Function Call (Type-Constrained Postfix)

```bnf
// call_expr uses ref_expr (not generic expr) as left operand
call_expr ::= ref_expr arg_list
arg_list ::= '(' [!')' expr (',' expr) *] ')' {pin(".*")=1}
```

The left operand is narrowed to `ref_expr` — only reference expressions can be called. The generated code uses `leftMarkerIs(builder_, REF_EXPR)` to check the type of the left sibling.

Source: ExprParser.bnf lines 50-51.

### Qualification / Member Access

```bnf
// fake rule defines the PSI interface
fake ref_expr ::= expr? '.' identifier

// simple reference and qualification share the same elementType
simple_ref_expr ::= identifier {extends=ref_expr elementType=ref_expr}
qualification_expr ::= expr '.' identifier {extends=ref_expr elementType=ref_expr}
```

Both `simple_ref_expr` and `qualification_expr` produce `REF_EXPR` element type. The `fake ref_expr` rule defines the PSI interface with `getExpr()` and `getIdentifier()` methods, but generates no parsing code.

Source: ExprParser.bnf lines 47-49, HOWTO.md lines 171-175.

### Narrowing to Specific Expression Level

```bnf
// between_expr restricts operands to add-level priority or higher
between_expr ::= expr BETWEEN add_group AND add_group
```

Using `add_group` instead of `expr` for the range operands restricts parsing to add-priority expressions and above. This means `a BETWEEN 1+2 AND 3*4` works, but `a BETWEEN b=c AND d` does not (assignment has lower priority).

Source: ExprParser.bnf lines 69-71.

### Multi-Token and Choice Operators

```bnf
// Multi-token operator
is_not_expr ::= expr IS NOT expr

// Choice operator — multiple comparison operators at same priority
conditional_expr ::= expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr
```

The operator part of an expression rule can contain any valid BNF expression: choices, sequences, or even optional elements.

Source: ExprParser.bnf lines 59, 68. HOWTO.md line 183.

### External Expression in Expression Hierarchy

```bnf
// External rule treated as ATOM
external special_expr ::= meta_special_expr

// Meta rule provides actual parsing logic
meta_special_expr ::= 'multiply' '(' simple_ref_expr ',' mul_expr ')' {
  elementType="special_expr"
  pin=2
}
```

External rules in expression hierarchies are treated as ATOM type. The `elementType` attribute on the meta rule maps the generated PSI to `special_expr`.

Source: ExprParser.bnf lines 74-75.

---

## Example 7: Minimal Expression Grammar

The simplest possible expression grammar with operator precedence.

```bnf
{
  tokens = [
    WS = "regexp:\\s+"
    ID = 'regexp:\\w+'
    PLUS = '+'
  ]
  extends(".*expr")="expr"
}

root ::= expr

expr ::= primary | add_group
private add_group ::= plus_expr
plus_expr ::= expr '+' expr
primary ::= ID
```

This grammar parses `a + b + c` with left-associative `+` and a flat PSI tree.

Source: testData/livePreview/Case153.bnf (adapted).

---

## Example 8: Multiple Expression Roots

A grammar can have multiple independent expression hierarchies.

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

**Key constraints:**
- Expression hierarchies must not intersect — no rule can participate in both.
- `extraRoot=true` marks an expression root for the `parse_extra_roots()` method.
- Each root generates its own `expr()` / `expr_0()` and `type()` / `type_0()` method pairs.

Source: HOWTO.md line 189, ExprParser.bnf line 37 (`extraRoot=true`).

---

## Example 9: Associativity Comparison

How the same input parses differently based on associativity.

### Left-Associative (Default)

```bnf
plus_expr ::= expr '+' expr
```

Input: `a + b + c`

Parse tree:
```
PlusExpr
  PlusExpr
    RefExpr('a')
    RefExpr('b')
  RefExpr('c')
```

Equivalent to: `(a + b) + c`

### Right-Associative

```bnf
assign_expr ::= expr '=' expr {rightAssociative=true}
```

Input: `a = b = c`

Parse tree:
```
AssignExpr
  RefExpr('a')
  AssignExpr
    RefExpr('b')
    RefExpr('c')
```

Equivalent to: `a = (b = c)`

### Non-Associative (Comparison Pattern)

```bnf
// All comparisons at the same priority level, no rightAssociative
conditional_expr ::= expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr
```

Input: `a < b < c`

Since comparisons are left-associative by default, this parses as `(a < b) < c`. There is no explicit non-associativity attribute in Grammar-Kit.

Source: ExprParser.bnf lines 58-59, rightAssociative.html.

---

## Example 10: IDE Quick Documentation Priority Table

When you press Ctrl-Q / Cmd-J on an expression rule, the IDE shows a priority table. The current rule is highlighted.

For the ExprParser.bnf grammar, hovering over `mul_expr` shows:

```
Expression root: expr
Operator priority table:
  0: BINARY(assign_expr)
  1: BINARY(conditional_expr)
  2: BINARY(plus_expr) BINARY(minus_expr)
  3: BINARY(xor_expr) BINARY(between_expr) BINARY(is_not_expr)
  4: BINARY(mul_expr) BINARY(div_expr)        ← current rule highlighted
  5: PREFIX(unary_plus_expr) PREFIX(unary_min_expr) PREFIX(unary_not_expr)
  6: N_ARY(exp_expr)
  7: POSTFIX(factorial_expr)
  8: POSTFIX(call_expr) POSTFIX(qualification_expr)
  9: ATOM(special_expr) ATOM(simple_ref_expr) ATOM(literal_expr) PREFIX(paren_expr)
```

This table is generated from the grammar structure and helps verify that precedence is correct.

Source: BnfDocumentationProvider.dumpPriorityTable(), HOWTO.md lines 203-213.
