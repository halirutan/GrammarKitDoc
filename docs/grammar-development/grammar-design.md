# Designing Grammar Rules

Writing syntactically correct BNF is only the first step. A working parser requires deliberate decisions about rule organization, PSI tree shape, and error handling hooks. As the Grammar-Kit documentation puts it: "Writing a grammar doesn't mean the generated parser will work. The tricky part is to *tune* some raw grammar into a *working* grammar."

This page covers the architectural principles, common patterns, and pitfalls that turn a raw grammar into a robust parser. It assumes you already know the BNF syntax covered in [Grammar Syntax](grammar-syntax.md).

## Grammar Architecture

A Grammar-Kit grammar has a predictable top-down structure. The decisions you make about that structure determine what the generated parser produces and what the resulting PSI tree looks like.

### Top-Down Structure

The first rule in the file is the grammar root. Grammar-Kit treats it as implicitly private, so no PSI class is generated for it. The root typically delegates to a private helper that loops over top-level constructs:

```bnf
root ::= item *
```

Each public rule produces one PSI node and one `IElementType` constant. Private rules produce neither. Their matched content merges into the parent node instead. This distinction is the primary tool for controlling what appears in your PSI tree.

The following template shows a well-organized grammar. Read the inline comments for the role of each section:

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

The key principles at work here: global attributes and tokens go at the top, the root rule delegates to a private helper with a loop, the `!<<eof>>` guard prevents an infinite loop at end of file, private rules dispatch to public rules so no unnecessary PSI nodes are created, and recovery rules sit near the rules they protect.

### Choosing Private vs. Public

Rules are public by default. Every public rule generates a PSI class and an `IElementType` constant, which means every public rule creates a node in the PSI tree. Use `private` when a rule is structural plumbing that should not appear in the tree.

Common uses for `private` rules:

- Root loop items (`private item ::= ...`)
- Dispatch rules that group alternatives (`private statement ::= select | delete | ...`)
- Recovery predicates (`private item_recover ::= !(';' | id)`)
- Operator priority groups in expressions (`private mul_group ::= mul_expr | div_expr`)

The Grammar-Kit guidance is direct: "Specify *private* attribute on any rule if you don't want it to be present in AST as early as possible."

!!! warning "Public helper rules create noise"
    If you leave helper rules public, the PSI tree fills with nodes that carry no semantic meaning. Compare:

    ```bnf
    // Unnecessary PSI nodes for 'item' and 'statement'
    root ::= item *
    item ::= !<<eof>> statement ';'
    statement ::= assignment | function_call
    ```

    ```bnf
    // Clean tree — only 'assignment' and 'function_call' appear
    root ::= item *
    private item ::= !<<eof>> statement ';' {pin=1 recoverWhile=item_recover}
    private item_recover ::= !(';' | id)
    statement ::= assignment | function_call
    ```

### Flattening with `extends`

Without `extends`, expression grammars produce deeply nested PSI trees. A simple literal like `42` might be wrapped in several layers:

```
FileNode
  Expr
    PlusExpr
      LiteralExpr
        number: '42'
```

Adding `extends(".*_expr")=expr` collapses the redundant wrapping nodes. The root expression rule never appears in the tree, and the AST becomes flat:

```
FileNode
  LiteralExpr
    number: '42'
```

Here is the before and after in grammar form:

```bnf
// BEFORE: no extends — deep AST
expr ::= factor plus_expr *
left plus_expr ::= ('+' | '-') factor
private factor ::= primary mul_expr *
left mul_expr ::= ('*' | '/') primary
private primary ::= literal_expr
literal_expr ::= number
```

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

For the full expression parsing framework, including priority tables and associativity, see [Expression Parsing](expression-parsing.md).

## Common Patterns

These patterns are reusable building blocks. Adapt them to your language rather than designing from scratch.

### Lists and Separators

A comma-separated list appears in almost every grammar. Define it once as a meta rule and reuse it:

```bnf
// Define once as a meta rule
meta comma_list ::= <<param>> (',' <<param>>) *

// Use for any comma-separated construct
import_list ::= <<comma_list import_item>>
param_list ::= <<comma_list param_decl>>
arg_list ::= <<comma_list expr>>
```

For parenthesized lists that need error recovery, use this pattern:

```bnf
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

The `pin(".*")=1` pins every sub-sequence at its first item. The `!')'` lookahead before `item` prevents matching an empty list as an error. The `recoverWhile` on each item skips unrecognized tokens until `,` or `)`.

You can simplify the recovery predicate by using `#auto`, which computes `!FOLLOWS(item)` automatically:

```bnf
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile="#auto"}
```

To allow trailing commas, use an and-predicate that accepts `)` after the last comma:

```bnf
element_list ::= '(' element (',' (element | &')'))* ')' {pin(".*")=1}
```

The `&')'` and-predicate allows a trailing comma: after the last `,`, seeing `)` is acceptable.

For full details on `pin`, `recoverWhile`, and `#auto`, see [Error Recovery](error-recovery.md).

### Declarations and Blocks

The property or assignment pattern pins on the operator. Once the `=` is seen, the rule is committed. A missing right-hand side produces an error, but the PSI node is still created:

```bnf
property ::= id '=' expr {pin=2}
```

Block structures pin on the opening delimiter:

```bnf
block ::= '{' statement * '}' {pin=1}
```

For optional elements, use the `?` quantifier or bracket syntax (they are equivalent):

```bnf
// Using ? quantifier
field_decl ::= type_ref id default_value? ';'

// Using bracket syntax (equivalent)
field_decl2 ::= type_ref id ['=' expr] ';'
```

Nested structures use lookahead negation to avoid consuming the closing delimiter. The JSON grammar demonstrates this clearly with `!'}' ` and `!']'` guards before list items.

### Statement-Level Design

Statement-oriented languages follow a consistent pattern: a root loop, a private dispatch rule, and individual pinned statements. Here is a complete example:

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

The design decisions here: `extends(".*_statement")=statement` creates a PSI hierarchy with `Statement` as the base type. The pattern-based pin `pin("create_.*")=2` pins all create statements at position 2. Statement recovery stops at `;` or any statement-starting keyword. Each statement type gets its own PSI class through public rules, and `column_list` is public because it carries semantic meaning in the tree.

### JSON Grammar Walkthrough

The JSON grammar from Grammar-Kit's test data demonstrates several patterns working together. Read the annotations for each design decision:

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

// Array: pinned parenthesized list with item recovery
array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1 extends=json}
private item ::= json {recoverWhile=recover}

// Object: pinned parenthesized list with property recovery
object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1 extends=json}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}
name ::= id | string {name="name"}

// Shared recovery predicate — stops at structural delimiters
private recover ::= !(',' | ']' | '}' | '[' | '{')
```

Several patterns are at work here. The `item` rule is private, so only `json`, `array`, and `object` appear in the PSI tree. One `recover` rule serves both array items and object properties. The `!']'` and `!'}' ` lookahead guards prevent consuming closing delimiters.

The `prop ::= []` trick with `pin=1` makes `name` optional in error scenarios because the empty optional always matches, so the pin is always reached. The `name` attribute on `value` improves error messages from a raw token list to the readable `<value> expected`. The nested `extends` chain (`array` and `object` extend `json`, which extends `value`) builds a clean PSI hierarchy.

## Reducing Repetition

As grammars grow, repeated attributes and structural patterns become a maintenance burden. Grammar-Kit provides two mechanisms to address this: pattern-based attributes and meta rules.

Pattern-based attributes apply a single attribute to every rule whose name matches a regex. Compare the verbose approach to the concise one:

```bnf
// BEFORE: attributes repeated on each rule
plus_expr ::= expr '+' expr {extends=expr}
minus_expr ::= expr '-' expr {extends=expr}
mul_expr ::= expr '*' expr {extends=expr}
div_expr ::= expr '/' expr {extends=expr}
```

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

The same approach works for `pin`, `name`, and `consumeTokenMethod`:

- `pin(".*_list(?:_\\d+)*")=1` pins all list rules and their sub-expressions.
- `name(".*_expr")='expression'` makes error messages say `<expression> expected` instead of listing every token.
- `consumeTokenMethod(".*_recover")="consumeTokenFast"` skips error-reporting overhead in recovery predicates.

!!! tip "Cleaner error messages with `name`"
    Without the `name` attribute, a failed expression match produces something like: `'+', '-', '*', '/', number, id, '(' expected`. With `name(".*_expr")='expression'`, the message becomes: `<expression> expected`.

Meta rules extract reusable structural patterns. The `comma_list` meta rule shown in the [Lists and Separators](#lists-and-separators) section is the most common example.

For large grammars that generate thousands of lines of code, split the parser across multiple classes using `;{ parserClass="..." }` section separators:

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

Each `;{parserClass="..."}` section generates methods in the named class.

## Pitfalls and Inspections

Grammar-Kit's IDE integration catches many common mistakes through inspections. Knowing these pitfalls upfront saves debugging time.

### Left Recursion

Left recursion causes a `StackOverflowError` in recursive descent parsers. The `BnfLeftRecursion` inspection detects it with the message: `'<ruleName>' employs left-recursion unsupported by generator`.

```bnf
// BAD: left recursion causes StackOverflowError
expr ::= expr '+' term | term
```

There are two fixes. Refactor to an iterative form:

```bnf
// GOOD: iterative
expr ::= term ('+' term) *
```

Or use the expression parsing framework, where left recursion is handled automatically through the `extends` mechanism:

```bnf
// GOOD: expression parsing framework handles left recursion
{
  extends(".*_expr")=expr
}
expr ::= plus_expr | literal_expr
plus_expr ::= expr '+' expr
literal_expr ::= number
```

Left recursion is only valid within the expression parsing framework (rules with `extends` pointing to a common root). See [Expression Parsing](expression-parsing.md) for details.

### Unreachable Choice Branches

Grammar-Kit uses [PEG](https://en.wikipedia.org/wiki/Parsing_expression_grammar) ordered choice: the first matching branch wins. A branch preceded by one that can match empty input is never reached. The `BnfUnreachableChoiceBranch` and `BnfIdenticalChoiceBranches` inspections detect these problems:

```bnf
// BAD: identical branches
value ::= number | string | number    // third branch is identical to first

// BAD: unreachable branch (preceded by branch matching empty)
item ::= optional_thing? | concrete_thing  // first branch always matches (empty)
```

### Public Recovery Predicates

Recovery predicates should always be `private`. A public recovery rule creates an unwanted PSI node. The `BnfUnusedRuleInspection` warns with "Non-private recovery rule."

```bnf
// BAD: creates unwanted PSI node
item_recover ::= !(',' | ')')

// GOOD: recovery predicates must be private
private item_recover ::= !(',' | ')')
```

### Missing Pin with recoverWhile

A `recoverWhile` attribute without a corresponding `pin` (on the rule itself or somewhere in its sub-rules) means recovery runs but the rule never commits. The node is not created in the PSI tree.

```bnf
// BAD: recoverWhile without pin — recovery runs but rule never commits
item ::= number {recoverWhile=item_recover}

// GOOD: pin must be present somewhere
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

### Rule Name Conflicts

Grammar-Kit generates internal methods named `rule_name_0`, `rule_name_N1_N2_NX` for sub-expressions. Naming your own rules with this pattern causes conflicts:

```bnf
// BAD: conflicts with generated sub-expression name
my_rule ::= a b c
my_rule_0 ::= d e f
```

Avoid naming rules with the `rule_name_N1_N2_..._NX` pattern.

### Token Conflicts

Prefer declared tokens over text-matched (quoted) tokens. Text-matched tokens are matched by text at parse time and can span multiple lexer tokens, which is both slower and can produce unexpected behavior. The `BnfSuspiciousToken` inspection highlights tokens that look like they should be rule references.

!!! note "IDE inspections"
    Grammar-Kit provides inspections for left recursion, unused rules, duplicate rules, unresolved references, identical and unreachable choice branches, suspicious tokens, and unused attributes. Use **Quick Documentation** (++ctrl+q++ / ++cmd+j++) to see FIRST/FOLLOWS sets, recovery predicate expansions, and expression priority tables for any rule. Use **Live Preview** (++ctrl+alt+p++) to test your grammar interactively without generating code. See [Live Preview](live-preview.md) for the full workflow.

The naming conventions for rules follow `snake_case` (`property_recover`, `root_item`, `literal_expr`). Generated PSI class names derive from rule names via CamelCase conversion: `literal_expr` becomes `LiteralExpr`. Generated parser methods follow the rule name directly: `static boolean literal_expr(..)`.

For the complete attribute catalog, including `extends`, `pin`, `name`, and `consumeTokenMethod`, see the [Attributes System](../code-generation/attributes.md). For error recovery mechanics, see [Error Recovery](error-recovery.md).
