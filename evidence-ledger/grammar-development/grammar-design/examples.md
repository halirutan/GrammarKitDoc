# Examples: Designing Grammar Rules

## Example 1: Well-Structured Grammar Template

A template showing good grammar organization: attributes, tokens, root rule, public rules, private helpers, and recovery.

```bnf
// 1. Global attributes
{
  parserClass="com.example.lang.parser.MyLangParser"
  parserUtilClass="com.example.lang.parser.MyLangParserUtil"

  psiClassPrefix="MyLang"
  psiImplClassSuffix="Impl"
  psiPackage="com.example.lang.psi"
  psiImplPackage="com.example.lang.psi.impl"

  elementTypeHolderClass="com.example.lang.psi.MyLangTypes"
  elementTypeClass="com.example.lang.psi.MyLangElementType"
  tokenTypeClass="com.example.lang.psi.MyLangTokenType"

  // Pattern-based attributes
  extends(".*_expr")=expr
  name(".*_expr")='expression'
  consumeTokenMethod(".*_recover")="consumeTokenFast"

  // 2. Token declarations
  tokens=[
    SEMI=';'
    COMMA=','
    EQ='='
    LP='('
    RP=')'
    LB='{'
    RB='}'

    space='regexp:\s+'
    comment='regexp://.*'
    number='regexp:\d+(\.\d*)?'
    id='regexp:\p{Alpha}\w*'
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"
  ]
}

// 3. Root rule (implicitly private)
root ::= item *

// 4. Top-level dispatch (private — no PSI node needed)
private item ::= !<<eof>> statement ';' {
  pin=1
  recoverWhile=item_recover
}
private item_recover ::= !(';' | id)

// 5. Statement alternatives (private dispatch)
private statement ::= assignment | function_call

// 6. Public rules (each generates a PSI node)
assignment ::= id '=' expr {pin=2}
function_call ::= id '(' [!')' expr (',' expr) *] ')' {pin(".*")=1}

// 7. Expression hierarchy
expr ::= add_group | mul_group | primary_group
private add_group ::= plus_expr | minus_expr
private mul_group ::= mul_expr | div_expr
private primary_group ::= literal_expr | ref_expr | paren_expr

plus_expr ::= expr '+' expr
minus_expr ::= expr '-' expr
mul_expr ::= expr '*' expr
div_expr ::= expr '/' expr
literal_expr ::= number | string
ref_expr ::= id
paren_expr ::= '(' expr ')' {pin=1}
```

**Design principles illustrated:**
- Global attributes and tokens are at the top.
- Root rule delegates to a private helper with a loop.
- `!<<eof>>` guard prevents infinite loop at end of file.
- Private rules dispatch to public rules (no unnecessary PSI nodes).
- Each public rule = one PSI node type.
- Recovery rules are near the rules they protect.
- Pattern-based attributes reduce repetition.

---

## Example 2: Common Pattern Library

### Comma-Separated List (Reusable Meta Rule)

```bnf
// Define once as a meta rule
meta comma_list ::= <<param>> (',' <<param>>) *

// Use for any comma-separated construct
import_list ::= <<comma_list import_item>>
param_list ::= <<comma_list param_decl>>
arg_list ::= <<comma_list expr>>
```

Source: ExternalRules.bnf line 38, README.md lines 155-156.

### Parenthesized List with Recovery

```bnf
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

**Why it works:**
- `pin(".*")=1` pins every sub-sequence at its first item.
- `!')'` lookahead before `item` prevents matching an empty list as an error.
- `recoverWhile` on each item skips garbage until `,` or `)`.

Source: AutoRecovery.bnf, pin.html, recoverWhile.html.

### Parenthesized List with #auto Recovery

```bnf
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile="#auto"}
```

`#auto` computes `! FOLLOWS(item)` automatically — equivalent to the manual predicate but maintained by the tool.

Source: AutoRecovery.bnf line 6.

### Trailing Comma Support

```bnf
element_list ::= '(' element (',' (element | &')'))* ')' {pin(".*")=1}
```

The `&')'` and-predicate allows a trailing comma: after the last `,`, seeing `)` is acceptable.

Source: HOWTO.md lines 386-395.

### Block Structure

```bnf
block ::= '{' statement * '}' {pin=1}
```

Pin on the opening brace ensures the block PSI node is created even if the body is malformed.

### Optional Constructs

```bnf
// Using ? quantifier
field_decl ::= type_ref id default_value? ';'

// Using bracket syntax (equivalent)
field_decl2 ::= type_ref id ['=' expr] ';'
```

### Declaration with Pin

```bnf
property ::= id '=' expr {pin=2}
```

Pin at position 2 (`=`): once the `=` is seen, the rule is committed. Missing `expr` produces an error but the `property` node is still created.

Source: TUTORIAL.md line 112.

---

## Example 3: Before/After Refactoring

### Problem: Deep PSI Tree Without `extends`

```bnf
// BEFORE: no extends — deep AST
expr ::= factor plus_expr *
left plus_expr ::= ('+' | '-') factor
private factor ::= primary mul_expr *
left mul_expr ::= ('*' | '/') primary
private primary ::= literal_expr
literal_expr ::= number
```

Resulting AST for `42`:
```
FileNode
  Expr
    PlusExpr       (or MulExpr wrapping)
      LiteralExpr
        number: '42'
```

### Solution: Flatten with `extends`

```bnf
// AFTER: with extends — flat AST
{
  extends(".*_expr")=expr
}
expr ::= factor plus_expr *
left plus_expr ::= ('+' | '-') factor
private factor ::= primary mul_expr *
left mul_expr ::= ('*' | '/') primary
private primary ::= literal_expr
literal_expr ::= number
```

Resulting AST for `42`:
```
FileNode
  LiteralExpr
    number: '42'
```

The `extends` attribute collapses redundant wrapping nodes. The root expression rule (`expr`) never appears in AST.

Source: HOWTO.md lines 232-250.

### Problem: Verbose Repetitive Attributes

```bnf
// BEFORE: attributes repeated on each rule
plus_expr ::= expr '+' expr {extends=expr}
minus_expr ::= expr '-' expr {extends=expr}
mul_expr ::= expr '*' expr {extends=expr}
div_expr ::= expr '/' expr {extends=expr}
```

### Solution: Pattern-Based Attributes

```bnf
// AFTER: single pattern attribute covers all rules
{
  extends(".*_expr")=expr
}
plus_expr ::= expr '+' expr
minus_expr ::= expr '-' expr
mul_expr ::= expr '*' expr
div_expr ::= expr '/' expr
```

Source: README.md lines 122-128.

### Problem: Error Messages List All Tokens

```
// Error without name attribute:
// "'+', '-', '*', '/', number, id, '(' expected"
```

### Solution: Use `name` Attribute

```bnf
{
  name(".*_expr")='expression'
}
```

```
// Error with name attribute:
// "<expression> expected"
```

Source: README.md lines 199-200.

---

## Example 4: Anti-Patterns and Fixes

### Anti-Pattern 1: Left Recursion (Outside Expression Parsing)

```bnf
// BAD: left recursion causes StackOverflowError
expr ::= expr '+' term | term
```

**Fix — iterative form:**
```bnf
// GOOD: right-recursive / iterative
expr ::= term ('+' term) *
```

**Fix — expression parsing framework:**
```bnf
// GOOD: use extends-based expression parsing (left recursion is handled)
{
  extends(".*_expr")=expr
}
expr ::= plus_expr | literal_expr
plus_expr ::= expr '+' expr      // left recursion OK with extends
literal_expr ::= number
```

Left recursion is detected by the BnfLeftRecursion inspection. It is only valid within the expression parsing framework (rules with `extends` pointing to a common root).

### Anti-Pattern 2: Public Rules That Should Be Private

```bnf
// BAD: unnecessary PSI nodes
root ::= item *
item ::= !<<eof>> statement ';'         // item appears in PSI tree — useless
statement ::= assignment | function_call
```

**Fix:**
```bnf
// GOOD: private helper rules
root ::= item *
private item ::= !<<eof>> statement ';' {pin=1 recoverWhile=item_recover}
private item_recover ::= !(';' | id)
statement ::= assignment | function_call
```

Source: HOWTO.md line 232 — "Specify *private* attribute on any rule if you don't want it to be present in AST as early as possible."

### Anti-Pattern 3: No Pin on Rules with recoverWhile

```bnf
// BAD: recoverWhile without pin — recovery runs but rule never commits
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

**Fix:**
```bnf
// GOOD: pin must be present (somewhere in the rule or its sub-rules)
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

Source: recoverWhile.html — "That rule should always have *pin* attribute somewhere as well."

### Anti-Pattern 4: Recovery Predicate Not Private

```bnf
// BAD: recovery predicate is public — creates unwanted PSI node
item_recover ::= !(',' | ')')
```

**Fix:**
```bnf
// GOOD: recovery predicates must be private
private item_recover ::= !(',' | ')')
```

The BnfUnusedRuleInspection warns: "Non-private recovery rule."

### Anti-Pattern 5: Rule Name Conflicts with Generated Sub-Expression Names

```bnf
// BAD: rule name looks like a generated sub-expression name
my_rule ::= a b c
my_rule_0 ::= d e f    // conflicts with generated my_rule_0(..)
```

**Fix:** Avoid naming rules with the `rule_name_N1_N2_..._NX` pattern.

Source: README.md line 120.

### Anti-Pattern 6: Identical or Unreachable Choice Branches

```bnf
// BAD: identical branches
value ::= number | string | number    // third branch is identical to first

// BAD: unreachable branch (preceded by branch matching empty)
item ::= optional_thing? | concrete_thing  // first branch always matches (empty)
```

The BnfIdenticalChoiceBranches and BnfUnreachableChoiceBranch inspections detect these.

---

## Example 5: Statement-Level Grammar Design

A complete example showing how to design a statement-oriented language grammar.

```bnf
{
  extends(".*_statement")=statement
  pin("create_.*")=2
  consumeTokenMethod(".*_recover")="consumeTokenFast"
  tokens=[
    SEMI=';'
    LP='('
    RP=')'
    space='regexp:\s+'
    id='regexp:\p{Alpha}\w*'
    number='regexp:\d+'
  ]
}

// Root with loop
script ::= script_item *

// Private loop item with recovery
private script_item ::= !<<eof>> statement ';' {
  pin=1
  recoverWhile=statement_recover
}
private statement_recover ::= !(';' | CREATE | DROP | SELECT)

// Statement dispatch (private — structural grouping)
statement ::= create_statement | drop_statement | select_statement

// Individual statements (public — each gets a PSI node)
create_statement ::= CREATE TABLE id '(' column_list ')' {pin=2}
drop_statement ::= DROP TABLE id {pin=2}
select_statement ::= SELECT column_list FROM id {pin=1}

// Shared sub-rules
column_list ::= column_def (',' column_def) *
column_def ::= id id {pin=1}           // name type
```

**Design decisions:**
- `extends(".*_statement")=statement` creates a PSI hierarchy with `Statement` as the base.
- Pattern-based pin `pin("create_.*")=2` pins all create statements at position 2.
- Statement recovery stops at `;` or any statement-starting keyword.
- Each statement type gets its own PSI class via public rules.
- `column_list` is public because it's meaningful in the PSI tree.

Source: based on Autopin.bnf pattern, HOWTO.md lines 88-93.

---

## Example 6: JSON Grammar Design Walkthrough

Annotated walkthrough of the Json.bnf grammar from Grammar-Kit's test data.

```bnf
{
  tokens = [
    space='regexp:\s+'                            // auto-detected as whitespace (not used in rules)
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
  extends("array|object|json")=value              // array, object, json all extend value
}

root ::= json                                     // root delegates to json
json ::= array | object                           // structural dispatch

value ::= string | number | json {name="value"}   // name attribute: errors say "<value> expected"

// Array: pinned parenthesized list with item recovery
array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1 extends=json}
private item ::= json {recoverWhile=recover}       // private — no PSI node for "item"

// Object: pinned parenthesized list with property recovery
object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1 extends=json}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}   // [] makes name optional (always pinned)
name ::= id | string {name="name"}                         // name attribute: errors say "<name> expected"

// Shared recovery predicate — stops at structural delimiters
private recover ::= !(',' | ']' | '}' | '[' | '{')
```

**Design patterns in this grammar:**
1. **Private dispatch**: `item` is private; only `json`, `array`, `object` appear in PSI.
2. **Shared recovery**: One `recover` rule serves both array items and object properties.
3. **Lookahead guards**: `!']'` and `!'}' ` prevent consuming the closing delimiter.
4. **Optional pinning trick**: `prop ::= []` with `pin=1` — the empty optional always matches, so pin is always reached. This makes `name` optional in error scenarios.
5. **`name` attribute**: Improves error messages from token lists to `<value> expected`.
6. **Nested extends**: `array` and `object` extend `json`, which extends `value`.

Source: testData/livePreview/Json.bnf (verbatim with annotations).

---

## Example 7: Splitting Large Grammars Across Parser Classes

```bnf
// Main parser handles top-level structure
{
  parserClass="com.example.MainParser"
  tokens=[...]
}

root ::= (statement | expression) *
statement ::= var_decl | assignment

// Expression rules go into a separate parser class
;{
  parserClass="com.example.ExpressionParser"
}

meta comma_list ::= <<param>> (',' <<param>>) *
expression ::= binary_expr | unary_expr | atom_expr
binary_expr ::= expression ('+' | '-' | '*' | '/') expression
unary_expr ::= ('-' | '!') expression
atom_expr ::= id | number | '(' expression ')'

// Utility parsing goes into a third class
;{
  parserClass="com.example.UtilityParser"
}

type_ref ::= id ('.' id) *
qualified_name ::= id ('.' id) *
```

Each `;{parserClass="..."}` section generates methods in the named class. Useful when a grammar produces thousands of lines of generated code.

Source: ExternalRules.bnf lines 84-99 (3 classes), PsiGen.bnf lines 39-41, 57-59 (3 classes).
