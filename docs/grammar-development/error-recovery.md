# Error Recovery

A Grammar-Kit parser without error recovery stops on the first unexpected token. Everything beyond that point loses its PSI structure, and IDE features like code completion and navigation break down. Two attributes make recovery possible: `pin` commits a rule after a recognizable prefix, and `recoverWhile` skips unexpected tokens to resynchronize. Together, they let the parser preserve PSI nodes even in broken code.

The two strategies address complementary problems. `pin` handles input that is *missing* parts (incomplete constructs), while `recoverWhile` handles input that *includes* unexpected tokens (extra garbage). This page explains how both work and shows the patterns for applying them.

Before reading this page, you should be comfortable with [BNF grammar syntax](grammar-syntax.md) (rule definitions, predicates, attributes) and [grammar design basics](grammar-design.md) (private rules, grammar architecture).

## Pin

The `pin` attribute applies to items of a grammar sequence expression. It does not apply to choices. Once the pinned item in a sequence matches, the parser considers the entire rule matched, even if later items fail. This prevents the parser from rolling back and discarding the partially-built PSI node.

### How pin works

The pin value is 1-indexed. `{pin=2}` means the second item in the sequence is the commit point. When the parser reaches and matches that item, it marks the rule as "pinned." If subsequent items fail, the parser records errors for the missing parts but keeps the node.

With `extendedPin=true` (the default), the parser still attempts to match the rest of the sequence after the pin point, recording errors along the way. This means a rule like `paren_expr ::= '(' expr ')' {pin=1}` with input `( )` produces a `paren_expr` node containing `(`, an error for the missing `expr`, and `)`. Without extended pin, the parser would stop after the failed `expr` and never match the closing `)`. In practice, the default is almost always correct and should not be changed.

Consider a property rule:

```bnf
property ::= id '=' expr {pin=2}
```

When the parser sees `x =` but `expr` is missing (say the next token is `;`), here is what happens:

1. `id` matches `x`.
2. `'='` matches, reaching pin=2. The rule is now committed.
3. `expr` fails. An error is recorded ("expression expected"), but the property node survives.

The result is a `property` PSI node with `id`, `=`, and a `PsiErrorElement` for the missing expression.

### Pin value formats

Grammar-Kit supports several ways to specify pin values.

Numeric pin sets the position directly:

```bnf
property ::= id '=' expr {pin=2}
```

Pattern pin matches a regex against item names in the sequence:

```bnf
create_table_statement ::= CREATE TEMP? TABLE table_ref '(' ')' {pin="table_ref"}
```

Sub-expression pin applies a pin value to all sub-sequences within a rule:

```bnf
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
```

This pins the outer sequence at `(`, the inner sequence at the `!')'` lookahead, and each `',' item` repetition at `,`.

Global pattern pin in the attributes block applies to all matching rules:

```bnf
{
  pin("create_.*_statement")=".*_ref"
  pin("drop_.*_statement")=".*_ref"
  pin("override.*")=1
}
```

Pinning the last item in a sequence has no effect and is ignored by the code generator.

The IDE highlights pinned expressions in the grammar editor. You can customize this color under **Settings > Colors and Fonts > "Pin marker"**. Hovering over a pinned expression shows a tooltip with the pin value.

## RecoverWhile

The `recoverWhile` attribute tells the parser to skip unexpected tokens after a rule completes (or fails), consuming input until a predicate says to stop. Where `pin` keeps a node alive despite missing parts, `recoverWhile` cleans up extra tokens so the parser can find the next valid construct.

### How recoverWhile works

The contract is:

1. The attributed rule is handled as usual (it either matches or fails).
2. Regardless of the result, the parser continues to consume tokens while the predicate rule matches.

This "regardless of the result" behavior is important. Even if the rule matched successfully, the parser still runs the recovery predicate to consume any trailing garbage before the next iteration.

Four usage rules apply:

- The rule with `recoverWhile` should be inside a loop, so there is a "next iteration" to resume at.
- That rule should have `pin` somewhere (otherwise recovery runs but the rule never commits, so the node is lost anyway).
- The value should be a predicate rule that does not consume input. It only tests whether the next token is a boundary.
- In most cases the predicate is a NOT expression: `!(token1 | token2 | ...)`.

### Writing recovery predicates

A recovery predicate lists the boundary tokens where the parser should stop skipping and resume normal parsing. It is always a NOT predicate, and it must be `private` (the IDE warns "Non-private recovery rule" otherwise).

```bnf
private statement_recover ::= !(';' | SELECT | DELETE | INSERT)
```

The tokens inside the `!(...)` are boundaries. When the parser encounters one of these tokens during recovery, it stops consuming and lets the next loop iteration begin.

Common patterns for boundary tokens:

- Statement recovery: delimiters and statement-starting keywords, e.g., `!(';' | SELECT | DELETE | INSERT | CREATE)`.
- List item recovery: separators and closing brackets, e.g., `!(',' | ')')`.
- Property recovery: delimiters and next-property indicators, e.g., `!(';' | id '=')`.
- JSON structural recovery: all structural delimiters, e.g., `!(',' | ']' | '}' | '[' | '{')`.

### Automatic recovery with #auto

Instead of writing a predicate by hand, you can use `recoverWhile="#auto"`. Grammar-Kit computes the FOLLOWS set of the rule (the tokens that can legally appear after it) and generates a predicate equivalent to `! FOLLOWS(rule)`.

```bnf
item ::= number {recoverWhile="#auto"}
```

The generated predicate uses `nextTokenIsFast` to test against the computed token set. You can verify what `#auto` produces by pressing Ctrl+Q (Cmd+J on macOS) on the rule. Quick Documentation shows a section labeled "#auto recovery predicate:" with the expanded `!(...tokens...)` expression.

Use `#auto` when the FOLLOWS set naturally covers the right boundary tokens. Write a manual predicate when you need additional boundaries that are not in the FOLLOWS set, such as statement-starting keywords.

## Recovery Patterns

The patterns below combine `pin` and `recoverWhile` into reusable structures. Each includes a walkthrough of what happens on broken input.

### Statement-level recovery

This pattern handles a sequence of statements separated by delimiters:

```bnf
{
  consumeTokenMethod(".*_recover")="consumeTokenFast"
  tokens=[
    SEMI=';'
    space='regexp:\s+'
    id='regexp:\p{Alpha}\w*'
    number='regexp:\d+'
  ]
}

script ::= script_item *
private script_item ::= !<<eof>> statement ';' {
  pin=1
  recoverWhile=statement_recover
}
private statement_recover ::= !(';' | SELECT | DELETE | INSERT)
private statement ::= select_statement | delete_statement | insert_statement

select_statement ::= SELECT id (',' id) * {pin=1}
delete_statement ::= DELETE id {pin=1}
insert_statement ::= INSERT id '=' number {pin=1}
```

Given this input:

```
SELECT a, b;
DELETE @#$;
INSERT x = 42;
```

Here is what happens:

1. `SELECT a, b;` parses normally.
2. `DELETE @#$;`: `DELETE` matches, reaching pin=1 on `delete_statement`. The `@#$` fails to match `id`. Pin keeps the `DELETE` statement node. `statement_recover` skips `@#$` because none of those characters are `;`, `SELECT`, `DELETE`, or `INSERT`. Recovery stops at `;`.
3. `INSERT x = 42;` parses normally.

The design decisions here are worth noting. `!<<eof>>` at the start of `script_item` prevents an infinite loop at end of file. `pin=1` on `script_item` commits once a statement keyword is found. `recoverWhile` is on the loop item (not on individual statements), so it skips garbage between statements.

Each concrete statement also has `pin=1` to commit at its keyword. The recovery predicate lists both delimiters and statement-starting keywords.

### List recovery

This pattern handles a parenthesized, comma-separated list:

```bnf
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

The `pin(".*")=1` pins all sub-sequences at their first item. The `!')'` lookahead prevents matching an empty list as an error. The `recoverWhile` on each item skips garbage until a `,` or `)` is found.

Given the input `(1, -, , 3, )`, the PSI tree looks like this:

```
LIST
  '('
  ITEM
    number: '1'
  ','
  PsiErrorElement: "number expected, got '-'"
    BAD_CHARACTER: '-'
  ','
  PsiErrorElement: "number expected, got ','"
  ','
  ITEM
    number: '3'
  ','
  PsiErrorElement: "number expected, got ')'"
  ')'
```

Walking through each token:

1. `(` matches. `pin(".*")=1` commits the list.
2. `1` matches as an item.
3. `,` matches as a separator.
4. `-` does not match `number`. `item_recover` skips it (since `-` is not `,` or `)`). An error element is created.
5. `,` is a boundary token, so recovery stops. The next item is attempted.
6. Another `,` appears immediately. The empty item produces an error for the missing `number`.
7. `3` matches as an item.
8. `,` then `)`. The trailing comma starts a new item, but `)` does not match `number`. Error recorded, then the list closes.

You can replace the manual predicate with `#auto`:

```bnf
item ::= number {recoverWhile="#auto"}
```

The generated predicate is equivalent to `!(',' | ')' | ';')`, computed from the FOLLOWS set.

To allow trailing commas without an error, use an and-predicate:

```bnf
element_list ::= '(' element (',' (element | &')'))* ')' {pin(".*")=1}
element ::= id {recoverWhile=element_recover}
private element_recover ::= !(',' | ')')
```

The `&')'` and-predicate succeeds when the next token is `)`, accepting a trailing comma without consuming the closing parenthesis.

### Nested recovery

Real grammars often need recovery at multiple levels. The JSON grammar demonstrates several techniques working together:

```bnf
{
  extends("array|object|json")=value
}

root ::= json
json ::= array | object
value ::= string | number | json {name="value"}

array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1 extends=json}
private item ::= json {recoverWhile=recover}

object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1 extends=json}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}
name ::= id | string {name="name"}

private recover ::= !(',' | ']' | '}' | '[' | '{')
```

The `prop ::= []` construct deserves explanation. `[]` is an empty optional that always matches. With `pin=1`, the pin is always reached because `[]` always succeeds. This makes `name` effectively optional during error recovery: a property node is created even when the name is missing. Without `[]`, a missing name would prevent the prop node from being created at all.

Both `item` and `prop` share the same `recover` predicate, which stops at any structural delimiter. This works because JSON's structural tokens (`{`, `}`, `[`, `]`, `,`) serve as natural boundaries at every level.

Here is how several broken inputs produce PSI trees:

Input `{ : 1}` (missing property name):

```
OBJECT
  '{'
  PROP
    PsiErrorElement: "<name> expected, got ':'"
    ':'
    VALUE
      number: '1'
  '}'
```

The PROP node is preserved because `[]` reached the pin point. The error message shows `<name> expected` because the `name` rule has `{name="name"}`.

Input `{ a }` (missing colon and value):

```
OBJECT
  '{'
  PROP
    NAME
      id: 'a'
    PsiErrorElement: "':' expected, got '}'"
  '}'
```

Input `{k : 5 6}` (extra token after value):

```
OBJECT
  '{'
  PROP
    NAME
      id: 'k'
    ':'
    VALUE
      number: '5'
    PsiErrorElement: "'6' unexpected"
      number: '6'
  '}'
```

The `recover` predicate keeps consuming tokens until a structural delimiter is found. `6` is not a delimiter, so it gets wrapped in the error element inside the PROP.

When building multi-level recovery, keep inner recovery boundaries as a subset of outer boundaries. If inner recovery consumes tokens that outer recovery needs, the outer level cannot resynchronize properly.

## Error Messages

The parser generates error messages automatically based on what it expected to find. Without any configuration, messages list all expected token alternatives:

```
'+', '-', '*', '/' expected, got 'x'
```

The `name` attribute replaces these token lists with a descriptive label. Apply it per-rule or with a pattern:

```bnf
value ::= string | number | json {name="value"}
```

This changes the error from `"string, number, '{', '[' expected, got 'x'"` to `"<value> expected, got 'x'"`. Pattern-based names apply to all matching rules:

```bnf
{
  name(".*_expr")='expression'
}
```

Setting `name=""` (empty string) suppresses the short error message entirely, which can be useful for helper rules that should not produce their own errors.

For performance, use `consumeTokenFast` in recovery predicates and expression rules. Recovery predicates only test tokens and never produce user-visible errors, so recording error information is wasted work. Expression operator rules similarly produce unhelpful "expected" messages listing every operator.

```bnf
{
  consumeTokenMethod(".*_recover")="consumeTokenFast"
  consumeTokenMethod(".*_expr|expr")="consumeTokenFast"
}
```

The default `consumeToken` method records error reporting information (token variants). `consumeTokenFast` skips this recording for better performance at the cost of less detailed error messages in those specific rules.

You can test recovery behavior interactively using [Live Preview](live-preview.md). Open it with Ctrl+Alt+P (Cmd+Alt+P on macOS), type broken input, and inspect the PSI tree in the Structure tool window to verify that nodes are preserved and error elements appear where expected. Quick Documentation (Ctrl+Q / Cmd+J) on any rule shows its FIRST and FOLLOWS sets, which helps when designing recovery predicates or verifying what `#auto` generates.
