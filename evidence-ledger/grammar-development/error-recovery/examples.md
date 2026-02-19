# Examples: Error Recovery

## Example 1: Statement Parsing with Recovery

The fundamental pattern for parsing a sequence of statements with error recovery between them.

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

// Root: loop of statements
script ::= script_item *

// Private loop item with recovery
private script_item ::= !<<eof>> statement ';' {
  pin=1
  recoverWhile=statement_recover
}

// Recovery predicate: stop at ';' or any statement-starting keyword
private statement_recover ::= !(';' | SELECT | DELETE | INSERT)

// Statement dispatch
private statement ::= select_statement | delete_statement | insert_statement

// Each statement type pinned at its keyword
select_statement ::= SELECT id (',' id) * {pin=1}
delete_statement ::= DELETE id {pin=1}
insert_statement ::= INSERT id '=' number {pin=1}
```

**How recovery works on broken input:**

Input:
```
SELECT a, b;
DELETE @#$;
INSERT x = 42;
```

1. `SELECT a, b;` — parses normally.
2. `DELETE @#$;` — `DELETE` matches (pin=1 reached), `@#$` fails to match `id`. Pin keeps the `DELETE` statement node. `statement_recover` skips `@#$` until `;` is found.
3. `INSERT x = 42;` — parses normally.

**Key design decisions:**
- `!<<eof>>` prevents infinite loop at end of file.
- `pin=1` on `script_item`: once a statement keyword is found, the item is committed.
- `recoverWhile` on the loop item (not on individual statements): skips garbage between statements.
- Pin on each concrete statement: each statement commits at its keyword.
- Recovery predicate lists delimiters AND statement-starting keywords.

Source: HOWTO.md lines 88-93.

---

## Example 2: List Parsing with Recovery

### Parenthesized List (Manual Recovery Predicate)

```bnf
{
  tokens=[number="regexp:\\d+" COMMA="," PAREN1="(" PAREN2=")"]
}

list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

**How it works on broken input:**

Input: `(1, -, , 3, )`

PSI tree (from AutoRecovery.txt):
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

**What happened step by step:**
1. `(` matched — pin(".*")=1 commits the list.
2. `1` matched as an item.
3. `,` matched as separator.
4. `-` does not match `number`. `item_recover` skips it (since `-` is not `,` or `)`). Error element created.
5. `,` is a boundary token — recovery stops. Next item attempted.
6. `,` immediately — empty item, error element for missing `number`.
7. `3` matched as an item.
8. `,` then `)` — empty trailing item produces error, then list closes.

Source: testData/generator/AutoRecovery.bnf, testData/livePreview/AutoRecovery.txt.

### Parenthesized List (#auto Recovery)

```bnf
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile="#auto"}
```

`#auto` computes the FOLLOWS set of `item` and generates: `!nextTokenIsFast(builder_, PAREN2, COMMA, SEMI)`. Equivalent to the manual predicate but automatically maintained.

Source: AutoRecovery.bnf line 6, AutoRecovery.expected.java.

---

## Example 3: Property/Assignment Recovery

The TUTORIAL.md pattern for parsing key-value properties.

```bnf
{
  tokens=[
    SEMI=';'
    EQ='='
    space='regexp:\s+'
    number='regexp:\d+(\.\d*)?'
    id='regexp:\p{Alpha}\w*'
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"
  ]
  extends(".*expr")=expr
  name(".*expr")='expression'
}

root ::= root_item *
private root_item ::= !<<eof>> property ';' {pin=1 recoverWhile=property_recover}

property ::= id '=' expr {pin=2}
private property_recover ::= !(';' | id '=')
```

**How recovery works on broken input:**

Input:
```
expr=1 * 2 + 3;
test_pin_results=;
some garbage to test error recovering
recovered=1/2
```

1. `expr=1 * 2 + 3;` — parses normally.
2. `test_pin_results=;` — `id` and `=` match (pin=2 reached). Missing `expr` after `=` creates an error, but the property node is kept. `;` matches.
3. `some garbage to test error recovering` — no `id '='` pattern found. `property_recover` skips tokens until `;` or `id '='`.
4. `recovered=1/2` — parses as property. Missing `;` at EOF.

**Two levels of recovery:**
- Inner: `pin=2` on property commits the property node after `=`.
- Outer: `recoverWhile=property_recover` on root_item skips garbage between properties.

Source: TUTORIAL.md lines 110-113, LivePreviewTutorial.bnf.

---

## Example 4: JSON Object/Array Recovery

A complex real-world recovery pattern from the JSON grammar.

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
json ::= array | object
value ::= string | number | json {name="value"}

array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1 extends=json}
private item ::= json {recoverWhile=recover}

object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1 extends=json}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}
name ::= id | string {name="name"}

private recover ::= !(',' | ']' | '}' | '[' | '{')
```

**The `prop ::= []` trick:**
- `[]` is an empty optional that always matches.
- With `pin=1`, the pin is always reached (because `[]` always succeeds).
- This means `name` is effectively optional during error recovery.
- Without `[]`, a missing name would prevent the prop node from being created.

**How recovery handles broken JSON:**

Input: `{ : 1}` (missing name)

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

The PROP node is preserved despite the missing name, because `[]` reached the pin point.

Input: `{ a }` (missing colon and value)

```
OBJECT
  '{'
  PROP
    NAME
      id: 'a'
    PsiErrorElement: "':' expected, got '}'"
  '}'
```

Input: `{k : 5 6}` (extra token)

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

The `recover` predicate `!(',' | ']' | '}' | '[' | '{')` keeps consuming tokens until a structural delimiter is found. Token `6` is not a delimiter, so it gets wrapped in the error element inside the PROP.

Source: testData/livePreview/Json.bnf, testData/livePreview/JsonRecovery.txt.

---

## Example 5: Pin Attribute Variants

### Numeric Pin

```bnf
// Pin at position 2: commit after '='
property ::= id '=' expr {pin=2}
```

### Pattern Pin

```bnf
// Pin at the item matching the regex pattern
create_table_statement ::= CREATE TEMP? TABLE table_ref '(' ')' {pin="table_ref"}
```

### Sub-Expression Pin

```bnf
// pin(".*")=1 applies pin=1 to ALL sub-sequences in the rule
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
```

This pins:
- The `'(' ...` outer sequence at `(`.
- The `!')' item ...` inner sequence at `!')' `.
- The `',' item` repetition at `,`.

### Global Pattern Pin

```bnf
{
  pin("create_.*_statement")=".*_ref"     // pin create statements at the ref
  pin("drop_.*_statement")=".*_ref"       // pin drop statements at the ref
  pin("override.*")=1                      // pin override rules at first item
}
```

Pattern-based pins in the global attributes block apply to all matching rules.

Source: Autopin.bnf lines 6-8, README.md lines 188-193, pin.html.

---

## Example 6: ExtendedPin Behavior

`extendedPin` (default: true) controls whether the parser attempts to match the rest of a sequence after the pin point, even when parts fail.

```bnf
// With extendedPin=true (default):
paren_expr ::= '(' expr ')' {pin=1}
```

Input: `( )`

With extendedPin=true:
1. `(` matches — pin reached, rule committed.
2. `expr` fails — error recorded, but parsing continues.
3. `)` matches.
4. Result: `paren_expr` node with `(`, error for missing `expr`, and `)`.

With extendedPin=false (hypothetical):
1. `(` matches — pin reached, rule committed.
2. `expr` fails — parsing stops here.
3. `)` never attempted.
4. Result: `paren_expr` node with `(` only. `)` would be consumed by recovery.

In practice, `extendedPin=true` (the default) is almost always correct. The attribute description says: "should not be changed."

Source: extendedPin.html, TUTORIAL.md lines 11-12.

---

## Example 7: The `name` Attribute for Error Messages

### Without `name`

```bnf
value ::= string | number | json
```

Error: `"string, number, '{', '[' expected, got 'x'"`

### With `name`

```bnf
value ::= string | number | json {name="value"}
```

Error: `"<value> expected, got 'x'"`

### Pattern-Based name

```bnf
{
  name(".*_expr")='expression'
}
```

Applies to all `*_expr` rules. Error messages show `<expression> expected` instead of listing individual tokens.

### Empty name (Suppress Error)

```bnf
// Setting name="" suppresses the short error message entirely
helper_rule ::= token1 | token2 {name=""}
```

Source: name.html, README.md lines 199-200, Json.bnf lines 19, 25.

---

## Example 8: consumeTokenMethod for Performance

```bnf
{
  // Skip error reporting in recovery rules (they don't generate user-visible errors)
  consumeTokenMethod(".*_recover")="consumeTokenFast"

  // Skip error reporting in expression parsing
  // (no one needs to know that + - * / are expected at every offset)
  consumeTokenMethod(".*_expr|expr")="consumeTokenFast"
}
```

**Two methods:**
- `consumeToken` (default): records error reporting information (token variants).
- `consumeTokenFast`: skips error reporting — better performance, but no error messages for failures in these rules.

Use `consumeTokenFast` for:
- Recovery predicate rules (they only test, never produce user-visible errors).
- Expression operator rules (listing all operators as "expected" is not helpful).

Source: consumeTokenMethod.html, HOWTO.md lines 192-196.

---

## Example 9: Multi-Level Recovery

Demonstrates inner and outer recovery working together.

```bnf
{
  consumeTokenMethod(".*_recover")="consumeTokenFast"
}

// Outer level: script recovery between top-level items
script ::= top_item *
private top_item ::= !<<eof>> (function_def | statement ';') {
  pin=1
  recoverWhile=top_recover
}
private top_recover ::= !(';' | FUNCTION | id)

// Inner level: parameter list recovery within a function
function_def ::= FUNCTION id '(' param_list ')' block {pin=1}
param_list ::= [!')' param (',' param) *] {pin(".*")=1}
param ::= id ':' type_ref {pin=2 recoverWhile=param_recover}
private param_recover ::= !(',' | ')')

// Statement level
statement ::= id '=' expr {pin=2}

// Block
block ::= '{' statement * '}' {pin=1}
```

**How levels interact:**

Input:
```
function foo(a: int, @garbage, b: str) {
  x = 1
  @more garbage
  y = 2
}
```

1. `function` keyword triggers `function_def`.
2. `a: int` parses as param.
3. `@garbage` fails. `param_recover` skips until `,`. Error element created.
4. `,` resumes. `b: str` parses as param.
5. Inside block: `x = 1` parses. `@more garbage` fails; outer recovery skips until next `id` or `}`.
6. `y = 2` parses.

Inner recovery boundaries (`','` and `')'`) are a subset of outer boundaries. This ensures inner recovery doesn't consume tokens that outer recovery needs.

---

## Example 10: Test Cases for Broken Code

Based on the actual test data from Grammar-Kit's Live Preview tests.

### AutoRecovery Test Cases

Grammar:
```bnf
file ::= list (';' list) * {pin(".*")=1}
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile="#auto"}
```

| Input | Expected Behavior |
|-------|-------------------|
| `(1, 2, 3)` | Normal parse: 3 items |
| `;` alone | Error: `'(' expected, got ';'` — empty list node |
| `(-, , 3, )` | `-` skipped (bad character), empty items at `,` positions, `3` parsed, trailing `,` produces empty item |
| `(1)` | Single item, normal parse |

Source: testData/livePreview/AutoRecovery.live.txt, AutoRecovery.txt.

### JsonRecovery Test Cases

Grammar: Json.bnf (see Example 4)

| Input | Error Type | Result |
|-------|-----------|--------|
| `{ : 1}` | Missing name | PROP created (pin trick), error `<name> expected, got ':'`, value `1` parsed |
| `{ a }` | Missing colon + value | PROP with NAME `a`, error `':' expected, got '}'` |
| `{ b: }` | Missing value | PROP with NAME `b` and `:`, error `<value> expected, got '}'` |
| `{ b:, }` | Missing value before comma | PROP with NAME `b` and `:`, error for missing value, second PROP with error |
| `{ 'd':, e:2 }` | Missing value, then valid prop | First PROP error, second PROP `e:2` parses normally |
| `{f::3,:}` | Double colon | PROP with NAME `f`, first `:`, error for second `:`, value `3`; second PROP error |
| `{g# :4}` | Bad character in property | PROP with NAME `g`, error for `#`, recovery continues to find `:` and `4` |
| `{k : 5 6}` | Extra token after value | PROP with value `5`, error `'6' unexpected` |
| `{v : { } }` | Nested object (valid) | PROP with nested OBJECT value |
| `{a, , , b}` | Multiple commas, missing colons | Multiple PROP nodes with errors, last PROP has NAME `b` |

Source: testData/livePreview/JsonRecovery.live.txt, JsonRecovery.txt.

---

## Example 11: Trailing Comma Pattern with Recovery

```bnf
element_list ::= '(' element (',' (element | &')'))* ')' {pin(".*")=1}
element ::= id {recoverWhile=element_recover}
private element_recover ::= !(',' | ')')
```

Input: `(a, b, c, )`

The `&')'` and-predicate after the last `,` succeeds (seeing `)`), so the trailing comma is accepted without error.

Input: `(a, b, , c)`

After the extra `,`, `element` fails, but `&')'` also fails (next token is not `)`). This produces an error for the missing element. Recovery skips nothing (`,` is a boundary), and `,` resumes the list.

Source: HOWTO.md lines 386-395.

---

## Example 12: Recovery Predicate Design Guidelines

### Rule: Predicate Lists Boundary Tokens

The recovery predicate should list tokens where the parser should stop skipping and resume normal parsing.

```bnf
// Statement-level: stop at delimiters and statement-starting keywords
private statement_recover ::= !(';' | SELECT | DELETE | INSERT | CREATE)

// List item: stop at separator and closing bracket
private item_recover ::= !(',' | ')')

// Property: stop at delimiter and next property start
private property_recover ::= !(';' | id '=')

// JSON: stop at any structural delimiter
private recover ::= !(',' | ']' | '}' | '[' | '{')
```

### Rule: Recovery Predicates Must Be Private

```bnf
// CORRECT: private recovery predicate
private item_recover ::= !(',' | ')')

// WRONG: public recovery predicate — triggers inspection warning
item_recover ::= !(',' | ')')    // Warning: "Non-private recovery rule"
```

### Rule: Use Quick Documentation to Design #auto Predicates

Press Ctrl-Q / Cmd-J on a rule with `recoverWhile="#auto"` to see:
- **Starts with:** (FIRST set)
- **Followed by:** (FOLLOWS set)
- **#auto recovery predicate:** — the expanded `!(...tokens...)` predicate

If the auto-generated predicate doesn't match your needs, write a manual predicate based on the FOLLOWS set shown in Quick Documentation.

Source: recoverWhile.html, BnfDocumentationProvider.java.
