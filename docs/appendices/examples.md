# Example Grammars

This appendix contains three complete Grammar-Kit grammars, each demonstrating a different set of features. You can paste any of these into a `.bnf` file in IntelliJ IDEA with the Grammar-Kit plugin installed and immediately use Live Preview (**Ctrl+Alt+P**) to test them.

## JSON Parser

This grammar parses JSON data: objects, arrays, strings, and numbers. It is the simplest complete grammar in Grammar-Kit's test suite and a good starting point for understanding the core mechanics.

```bnf
{
  tokens = [
    space='regexp:\s+'
    string = "regexp:\"[^\"]*\"|'[^']*'"
    number = "regexp:(\+|\-)?\p{Digit}*"
    id = "regexp:\p{Alpha}\w*"
    comma = ","
    colon = ":"
    brace1 = "{"
    brace2 = "}"
    brack1 = "["
    brack2 = "]"
  ]
  extends("array|object|json")=value
}

root ::= json
json ::= array | object  { hooks=[wsBinders="null, null"] }
value ::= string | number | json {name="value" hooks=[leftBinder="GREEDY_LEFT_BINDER"]}

array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1 extends=json}
private item ::= json {recoverWhile=recover}
object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1 extends=json}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}
name ::= id | string {name="name" hooks=[rightBinder="GREEDY_RIGHT_BINDER"]}
private recover ::= !(',' | ']' | '}' | '[' | '{')
```

Given this input:

```json
{
  "name": "Grammar-Kit",
  "version": 2023,
  "features": ["parsing", "generation"]
}
```

The parser produces a PSI tree like this:

```
root
  json (object)
    prop
      name: "name"
      value: "Grammar-Kit"
    prop
      name: "version"
      value: 2023
    prop
      name: "features"
      value (array)
        json: "parsing"
        json: "generation"
```

### Key features demonstrated

`extends("array|object|json")=value` creates a flat type hierarchy where `array`, `object`, and `json` all extend `value`. In generated PSI code, you can work with any of these as a `Value` element. For background on the `extends` attribute, see [Attributes System](../code-generation/attributes.md).

`pin(".*")=1` inside `array` and `object` tells the parser to commit after the opening bracket. Once the parser sees `[` or `{`, it reports errors for malformed contents rather than backtracking. See [Error Recovery and Pin](../grammar-development/error-recovery.md) for details.

`recoverWhile=recover` on `item` and `prop` limits how far the parser skips when it encounters invalid input. The `recover` rule stops at delimiters (`,`, `]`, `}`, `[`, `{`), so a single malformed entry does not consume the rest of the document.

The `hooks` attribute controls whitespace binding. `wsBinders="null, null"` on `json` detaches whitespace from both sides of the node, while `leftBinder="GREEDY_LEFT_BINDER"` on `value` and `rightBinder="GREEDY_RIGHT_BINDER"` on `name` pull whitespace into the node for formatting purposes.

The `name="value"` attribute overrides the rule name in error messages. Instead of reporting "expected json", the parser reports "expected value", which is clearer for users.

## Expression Calculator

This grammar handles arithmetic expressions with operator precedence, demonstrating Grammar-Kit's Pratt-style expression parsing. It covers binary, unary prefix, postfix, and n-ary operators across ten precedence levels.

```bnf
{
  generate=[psi="no"]
  classHeader="//header.txt"
  parserClass="org.intellij.grammar.expression.ExpressionParser"
  extends(".*expr")=expr
  elementTypeFactory="org.intellij.grammar.expression.ExpressionParserDefinition.createType"
  tokenTypeFactory="org.intellij.grammar.expression.ExpressionParserDefinition.createTokenType"
  elementTypeHolderClass="org.intellij.grammar.expression.ExpressionTypes"
  parserUtilClass="org.intellij.grammar.parser.GeneratedParserUtilBase"

  tokens=[
    space='regexp:\s+'
    comment='regexp://.*'
    number='regexp:\d+(\.\d*)?'
    id='regexp:\p{Alpha}\w*'
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"
    syntax='regexp:;|\.|\+|-|\*\*|\*|==|=|/|,|\(|\)|\^|\!=|\!|>=|<=|>|<'
  ]
}
root ::= element *
private element ::= expr ';'?  {recoverWhile=element_recover}
private element_recover ::= !('(' | '+' | '-' | '!' | 'multiply' | id | number)

expr ::= assign_expr
  | conditional_group
  | add_group
  | boolean_group
  | mul_group
  | unary_group
  | exp_expr
  | factorial_expr
  | call_expr
  | qualification_expr
  | primary_group
  {extraRoot=true}
private boolean_group ::= xor_expr | between_expr | is_not_expr

private conditional_group ::= elvis_expr | conditional_expr
private unary_group ::= unary_plus_expr | unary_min_expr | unary_not_expr
private mul_group ::= mul_expr | div_expr
private add_group ::= plus_expr | minus_expr
private primary_group ::= special_expr | simple_ref_expr | literal_expr | paren_expr

fake ref_expr ::= expr? '.' identifier
simple_ref_expr ::= identifier {extends=ref_expr elementType=ref_expr}
qualification_expr ::= expr '.' identifier {extends=ref_expr elementType=ref_expr}
call_expr ::= ref_expr arg_list
arg_list ::= '(' [ !')' expr  (',' expr) * ] ')' {pin(".*")=1}
literal_expr ::= number
identifier ::= id
unary_min_expr ::= '-' expr
unary_plus_expr ::= '+' expr
unary_not_expr ::= '!' expr
xor_expr ::= expr '^' expr
assign_expr ::= expr '=' expr { rightAssociative=true }
conditional_expr ::= expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr
div_expr ::= expr '/' expr
mul_expr ::= expr '*' expr
minus_expr ::= expr '-' expr
plus_expr ::= expr '+' expr
exp_expr ::= expr ('**' expr) +
factorial_expr ::= expr '!'
paren_expr ::= '(' expr ')'
elvis_expr ::= expr '?' expr ':' expr
is_not_expr ::= expr IS NOT expr
between_expr ::= expr BETWEEN add_group AND add_group {
  methods=[testExpr="expr[0]"]
}

external special_expr ::= meta_special_expr
meta_special_expr ::= 'multiply' '(' simple_ref_expr ',' mul_expr ')' {elementType="special_expr" pin=2}
```

Given this input:

```
x = 2 + 3 * 4;
y = (1 + 2)!;
z = a > b ? a : b;
```

The parser produces:

```
root
  element
    assign_expr (rightAssociative)
      ref_expr: x
      plus_expr
        literal_expr: 2
        mul_expr
          literal_expr: 3
          literal_expr: 4
  element
    assign_expr
      ref_expr: y
      factorial_expr (postfix)
        paren_expr
          plus_expr
            literal_expr: 1
            literal_expr: 2
  element
    assign_expr
      ref_expr: z
      elvis_expr (ternary)
        conditional_expr
          ref_expr: a
          ref_expr: b
        ref_expr: a
        ref_expr: b
```

### Operator precedence

The order of alternatives in the `expr` rule defines precedence, from lowest (top) to highest (bottom):

| Priority | Operators | Type |
|----------|-----------|------|
| 0 | `assign_expr` (`=`) | Binary, right-associative |
| 1 | `elvis_expr` (`?:`), `conditional_expr` (`<`, `>`, `==`) | Binary |
| 2 | `plus_expr`, `minus_expr` | Binary |
| 3 | `xor_expr` (`^`), `between_expr`, `is_not_expr` | Binary |
| 4 | `mul_expr`, `div_expr` | Binary |
| 5 | `unary_plus_expr`, `unary_min_expr`, `unary_not_expr` | Prefix |
| 6 | `exp_expr` (`**`) | N-ary |
| 7 | `factorial_expr` (`!`) | Postfix |
| 8 | `call_expr`, `qualification_expr` (`.`) | Postfix |
| 9 | `special_expr`, `simple_ref_expr`, `literal_expr`, `paren_expr` | Atom |

### Key features demonstrated

`extends(".*expr")=expr` is the pattern that activates Pratt-style expression parsing. Any rule matching `.*expr` is treated as an expression variant, and Grammar-Kit generates a single recursive descent method that handles all precedence levels. See [Expression Parsing](../grammar-development/expression-parsing.md) for the full explanation.

`rightAssociative=true` on `assign_expr` makes assignment bind right-to-left, so `a = b = c` parses as `a = (b = c)`.

`fake ref_expr` declares a PSI interface without generating any parsing code. Both `simple_ref_expr` and `qualification_expr` use `extends=ref_expr elementType=ref_expr` to share the same element type and PSI base class. This is useful when multiple syntax forms should appear identical in the PSI tree.

`exp_expr ::= expr ('**' expr) +` uses the `+` quantifier to create an n-ary operator, collecting chains like `2 ** 3 ** 4` into a single flat node rather than nesting them.

`external special_expr ::= meta_special_expr` delegates parsing to a meta rule. Meta rules accept other rules as parameters, enabling reusable parsing patterns. See [Grammar Syntax](../grammar-development/grammar-syntax.md) for details on external and meta rules.

`{extraRoot=true}` on `expr` marks it as an extra root, allowing the parser to parse standalone expressions without requiring the full `root` rule context. This is useful for features like expression evaluation in debuggers.

## Simple Scripting Language

This grammar comes from the Grammar-Kit tutorial and implements a small scripting language with property assignments, arithmetic expressions, and a factorial operator. It uses the `left` rule pattern for expression parsing rather than the Pratt-style approach.

```bnf
{
  tokens=[
    SEMI=';'
    EQ='='
    LP='('
    RP=')'

    space='regexp:\s+'
    comment='regexp://.*'
    number='regexp:\d+(\.\d*)?'
    id='regexp:\p{Alpha}\w*'
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"

    op_1='+'
    op_2='-'
    op_3='*'
    op_4='/'
    op_5='!'
  ]

  name(".*expr")='expression'
  extends(".*expr")=expr
}

root ::= root_item *
private root_item ::= !<<eof>> property ';' {pin=1 recoverWhile=property_recover}

property ::= id '=' expr  {pin=2}
private property_recover ::= !(';' | id '=')

expr ::= factor plus_expr *
left plus_expr ::= plus_op factor
private plus_op ::= '+'|'-'
private factor ::= primary mul_expr *
left mul_expr  ::= mul_op primary
private mul_op ::= '*'|'/'
private primary ::= primary_inner factorial_expr ?
left factorial_expr ::= '!'
private primary_inner ::= literal_expr | ref_expr | paren_expr
paren_expr ::= '(' expr ')' {pin=1}
ref_expr ::= id
literal_expr ::= number | string | float
```

Given this input:

```
x = 10 + 20 * 3;
y = (5 + 2)!;
name = "hello";
```

The parser produces:

```
root
  property
    id: x
    expr
      literal_expr: 10
      plus_expr
        literal_expr: 20
        mul_expr
          literal_expr: 3
  property
    id: y
    expr
      paren_expr
        expr
          literal_expr: 5
          plus_expr
            literal_expr: 2
      factorial_expr
  property
    id: name
    literal_expr: "hello"
```

### Key features demonstrated

The `left` keyword on `plus_expr`, `mul_expr`, and `factorial_expr` marks these as left rules. A left rule extends the preceding expression rather than wrapping it, producing a left-associative parse tree. The expression `10 + 20 * 3` parses with multiplication binding tighter because `mul_expr` appears deeper in the grammar's call chain (`expr` calls `factor`, which calls `primary`). See [Expression Parsing](../grammar-development/expression-parsing.md) for more on left rules.

`name(".*expr")='expression'` sets the display name for all expression rules in error messages. Instead of "expected plus_expr", the parser reports "expected expression".

The recovery strategy uses two levels. At the top level, `property_recover` stops at semicolons and the start of the next property (`id '='`), so a syntax error in one property does not prevent parsing the rest of the file. Within a property, `pin=2` on the `property` rule commits after seeing the `=` sign. See [Error Recovery and Pin](../grammar-development/error-recovery.md).

`!<<eof>>` in `root_item` is a predicate that prevents the parser from entering the `property` rule at end-of-file, avoiding a spurious "expected property" error on trailing whitespace or comments.

## Further Reading

Grammar-Kit's test suite at `testData/generator/` contains 29 additional grammars, each focused on a specific feature. Notable examples include `AutoRecovery.bnf` for `#auto` recovery patterns, `ExternalRules.bnf` for external and meta rule usage, `Stub.bnf` for stub index integration, and `PsiAccessors.bnf` for path-based PSI accessor methods. See the [Grammar-Kit repository](https://github.com/JetBrains/Grammar-Kit) for the full collection.
