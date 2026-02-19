# Section 2.5: Live Preview — Examples

## Example 1: JSON Grammar for Live Preview

**Source: `testData/livePreview/Json.bnf`**

A complete JSON grammar demonstrating Live Preview features including hooks, extends, pin, and recovery:

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

Key features demonstrated:
- `space='regexp:\s+'` — whitespace token auto-detected (unused in rules)
- `hooks=[wsBinders="null, null"]` — whitespace binder hooks
- `pin(".*")=1` — pin on sub-expressions
- `recoverWhile=recover` — error recovery predicate
- `extends("array|object|json")=value` — type hierarchy

## Example 2: Tutorial Grammar with Expression Parsing

**Source: `testData/livePreview/LivePreviewTutorial.bnf`**

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

Key features:
- `comment='regexp://.*'` — auto-detected as comment (name ends in "comment")
- `left plus_expr` / `left mul_expr` — left-associative expression parsing
- `!<<eof>>` — built-in external predicate for end-of-file check
- `name(".*expr")='expression'` — custom error message names

## Example 3: Auto-Recovery in Live Preview

**Source: `testData/livePreview/AutoRecovery.bnf`**

```bnf
{
  tokens=[
    space='regexp:\s+'
    number='regexp:\d+'
  ]
}
root ::= item *
item ::= number {recoverWhile="#auto"}
```

Demonstrates `#auto` recovery: the parser automatically computes FIRST/NEXT sets and generates a predicate that consumes tokens until a token in the NEXT set is found.

## Example 4: Expression Parsing in Preview

**Source: `testData/livePreview/Case153.bnf`**

```bnf
{
  tokens=[
    space="regexp:\s+"
    number="regexp:\d+"
  ]
  extends(".*expr")=expr
}
root ::= expr +
expr ::= primary | add_group
private add_group ::= plus_expr
plus_expr ::= expr '+' expr
private primary ::= number
```

Tests basic Pratt-style expression parsing in Live Preview mode.

## Token Type Detection Summary

| Token Pattern | Auto-Detected Type | Highlighting |
|---|---|---|
| Matches `" "` or `"\n"` | `WHITE_SPACE` | None (hidden) |
| Matches `"1234"` | `NUMBER` | Number color |
| Matches `"\"sdf\""` or `"'sdf'"` | `STRING` | String color |
| Name ends with "comment" | `COMMENT` | Comment color |
| `StringUtil.isJavaIdentifier(text)` | `KEYWORD` | Keyword color |

## Workflow Example

1. Create a `.bnf` file with token definitions and grammar rules
2. Press **Ctrl-Alt-P** to open Live Preview
3. Type sample input in the preview pane
4. Observe real-time PSI tree in Structure tool window (Ctrl-F12)
5. Press **Ctrl-Alt-F7** to toggle grammar-at-caret highlighting
6. Modify grammar rules — preview auto-updates after 500ms
