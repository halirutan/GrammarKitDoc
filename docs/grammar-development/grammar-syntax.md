# BNF Grammar Syntax

Grammar-Kit uses a [Parsing Expression Grammar (PEG)](https://en.wikipedia.org/wiki/Parsing_expression_grammar) dialect of BNF. A `.bnf` file contains an optional attributes block followed by rule definitions, where `::=` defines rules and ordered choice (`|`) means the first matching alternative wins. This page covers every syntax construct you can use in a Grammar-Kit grammar file.

## File Structure

A `.bnf` file has three parts: an optional global attributes block, rule definitions, and comments. Here is a minimal grammar:

```bnf
// Global attributes block
{
  parserClass="com.example.MyParser"
  tokens=[
    SEMI=';'
    EQ='='
    LP='('
    RP=')'
    space='regexp:\s+'
    id='regexp:\p{Alpha}\w*'
    number='regexp:\d+'
  ]
}

// First rule is implicitly private (grammar root)
root ::= statement *

// Public rule — generates PSI node and IElementType
statement ::= id '=' number ';'
```

The `{ }` block at the top holds global attributes as `name=value` pairs, separated by optional semicolons. The most common content is `tokens=[...]`, which declares the grammar's token vocabulary. See [Attributes System](../code-generation/attributes.md) for the full attribute catalog.

Rules follow the attributes block. Each rule has the form `rule_name ::= expression`, with an optional trailing `;`. The first rule in the file is implicitly private and serves as the grammar root. No PSI node is generated for it.

Line comments start with `//` and run to the end of the line. Block comments use `/* ... */`. Line comments require a line break after them.

### Grammar Sections

For large grammars, you can split generated code into multiple parser classes by inserting `;{` separators between groups of rules:

```bnf
// Main parser class: rules defined here go into MainParser
{
  parserClass="com.example.MainParser"
  tokens=[
    id='regexp:\w+'
    number='regexp:\d+'
  ]
}

root ::= (statement | expression) *
statement ::= id '=' number

// Semicolon-brace separator starts a new section.
// Rules after this go into ExpressionParser.
;{
  parserClass="com.example.ExpressionParser"
}

expression ::= id '+' id
complex_expr ::= expression ('*' expression) *

// Another section: rules go into UtilityParser
;{
  parserClass="com.example.UtilityParser"
}

utility_rule ::= id number
```

Each `;{` starts a new global attributes section. Rules after the separator generate methods in the specified parser class. This keeps generated code manageable when a grammar grows large.

## Tokens

### Declaring Tokens

Tokens are declared in the global `tokens` attribute as a list. Each entry takes one of three forms:

| Form | Syntax | Example |
|------|--------|---------|
| Name with string value | `NAME='value'` | `SEMI=';'` |
| Name with regexp value | `NAME='regexp:pattern'` | `id='regexp:\p{Alpha}\w*'` |
| Name only (no value) | `NAME` | `IDENTIFIER` |

Single and double quotes are interchangeable for token values. The `regexp:` prefix marks a regular expression pattern and supports full Java regex syntax. Regexp tokens are required for [Live Preview](live-preview.md) to work.

```bnf
{
  tokens=[
    // Named tokens with string values
    PLUS='+'
    MINUS='-'
    OP_EQ="="                    // double quotes work the same as single quotes

    // Regexp tokens (required for Live Preview)
    id='regexp:\p{Alpha}\w*'
    number="regexp:\d+(\.\d*)?"
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"

    // Whitespace/comment tokens (auto-detected in Live Preview)
    space='regexp:\s+'           // matches whitespace; treated as whitespace in Live Preview
    comment='regexp://.*'        // name ends with "comment"; treated as comment in Live Preview

    // Name-only token (no value or pattern)
    IDENTIFIER
  ]
}
```

In Live Preview, whitespace and comments are auto-detected: any space-matching regexp token not used in rules is treated as whitespace, and tokens whose names end with "comment" (case-insensitive) that are not used in rules are treated as comments. In generated parsers, whitespace and comment handling is configured in your `ParserDefinition` and skipped automatically by `PsiBuilder`.

### Referencing Tokens in Rules

You can reference tokens in rules by their quoted value or by their unquoted name:

```bnf
// Reference tokens by value (recommended for readability)
addition ::= number '+' number

// Reference tokens by name (resolves conflicts)
assignment ::= id OP_EQ number
```

Use quoted values (`'+'`) for readability. Use names (`OP_EQ`) when an unquoted value would conflict with a rule name.

Tokens that appear in rules but are not declared in the `tokens` block are implicit tokens. An unquoted implicit token (like `CREATE`) acts as a keyword where the token name equals its text value. A quoted implicit token (like `'begin'`) is matched by text rather than by `IElementType`, which is slower and can span multiple real lexer tokens. Rules, declared tokens, and text-matched tokens each have different editor colors, making it easy to spot which kind of reference you are using.

```bnf
// Implicit tokens (not declared in tokens block)
// Unquoted implicit tokens: name equals value
create_statement ::= CREATE TABLE id    // CREATE and TABLE are keyword tokens

// Quoted implicit tokens: matched by text (slower)
special ::= 'begin' id 'end'            // matched by text, not IElementType
```

## Rules and Expressions

### Sequences, Choices, and Quantifiers

A rule body is an expression built from sequences, choices, quantifiers, and grouping constructs:

```bnf
// Sequence: items separated by whitespace, all must match
import_statement ::= 'import' qualified_name ';'

// Ordered choice: alternatives separated by |, first match wins (PEG semantics)
literal ::= number | string | 'true' | 'false' | 'null'

// Quantifiers
argument_list ::= argument *              // zero or more
statements ::= statement +                // one or more
type_annotation ::= type_ref?             // zero or one (optional)

// Grouping with parentheses
repeated_pair ::= (id '=' number) *       // repeat the grouped sequence

// Optional with brackets: [expr] is shorthand for (expr)?
field_decl ::= type_ref id ['=' expr] ';'

// Choice with braces: { | | } alternative syntax for ( | | )
value ::= { number | string | 'null' }

// Combining constructs
param_list ::= '(' [!')' param (',' param) *] ')'
```

Sequences match left to right; every item must succeed. Ordered choice tries alternatives in declaration order and takes the first match (PEG semantics, not ambiguous). Quantifiers (`?`, `+`, `*`) apply as postfix to any expression. Parentheses `( )` group sub-expressions, brackets `[ ]` are shorthand for `( )?` (optional), and braces `{ | }` are an alternative choice syntax equivalent to `( | )`.

### Predicates

Predicates test the input without consuming any tokens. The and-predicate `&` is a positive lookahead that succeeds when its expression matches. The not-predicate `!` is a negative lookahead that succeeds when its expression does not match.

```bnf
// Not-predicate: succeeds if expression does NOT match, consumes nothing
// Common use: prevent consuming a closing delimiter
array ::= '[' [!']' item (',' item) *] ']'

// And-predicate: succeeds if expression matches, consumes nothing
// Common use: require a specific token ahead before committing
guarded_rule ::= &'class' class_declaration

// Combining predicates
statement ::= &required_keyword !forbidden_keyword rest_of_statement

// Recovery predicate — the most common use of not-predicates
private statement_recover ::= !(';' | 'class' | 'function')

// Not-at-end-of-file guard (built-in <<eof>>)
private root_item ::= !<<eof>> property ';'

// Edge cases: empty predicates
private always_true ::= &()    // and-predicate on empty always succeeds
private always_false ::= !()   // not-predicate on empty always fails
```

The most common use of not-predicates is in recovery rules that list boundary tokens the parser should stop at. The built-in `<<eof>>` external tests for end of input; `!<<eof>>` is a standard guard to prevent infinite loops at the end of a file. For more on recovery predicates, see [Error Recovery](error-recovery.md).

### Rule Modifiers

Seven modifiers control how a rule generates code and interacts with the PSI tree. Place modifiers before the rule name, and combine multiple modifiers when needed.

| Modifier | Effect |
|----------|--------|
| `private` | No PSI node created; children merge into the parent node |
| `left` | Takes the previous sibling AST node and wraps it (becomes its parent) |
| `inner` | Used with `left`; takes the previous sibling and injects into it (becomes its child) |
| `upper` | Takes the parent node and replaces it, adopting all its children |
| `meta` | Parametrized rule; accepts other parse functions as arguments |
| `external` | Hand-written parse function; no code generated |
| `fake` | Only PSI classes generated; no parsing code |

```bnf
// private: no PSI node — children merge into parent
private primary ::= literal_expr | ref_expr | paren_expr

// left: takes previous sibling and wraps it (becomes its parent)
// Used for binary operators in traditional expression parsing
left plus_expr ::= ('+' | '-') factor

// inner left: takes previous sibling and injects into it (becomes its child)
left inner leech ::= id

// private left: equivalent to private left inner
private left leech2 ::= id

// upper: takes parent node and replaces it, adopting all children
upper abc_one ::= just_b X {pin=1}

// meta: parametrized rule, accepts parse functions as arguments
meta comma_list ::= <<param>> (',' <<param>>) *

// external: hand-written parse function, no code generated
external my_rule ::= parseMyRule param1 param2

// fake: only PSI classes generated, no parsing code
fake ref_expr ::= expr? '.' identifier
```

A few constraints on combining modifiers: `inner` should only be used with `left`. Writing `private left` is equivalent to `private left inner`. Do not combine `fake` with `private`. By default, rules with no modifiers are public.

The `left` and `upper` modifiers restructure the AST during parsing. For a full explanation of how `left` rules work in expression grammars, see [Expression Parsing](expression-parsing.md). For guidance on when to use `private` and how it affects grammar design, see [Grammar Design](grammar-design.md).

## Advanced Constructs

### External Expressions and Rules

External expressions call hand-written Java methods from within grammar rules. The inline form is `<<methodName arg1 arg2>>`, and the declaration form is `external rule_name ::= methodName param1 param2`.

```bnf
{
  parserUtilClass="com.example.MyParserUtil"
  parserImports=["static com.example.ManualParsing.*"]
}

// External rule: hand-written parse function
external my_rule ::= parseMyRule false 10

// Using the external rule in another rule
content ::= header my_rule footer

// Inline external expression (equivalent to external rule but inline)
content2 ::= header <<parseMyRule true 5>> footer

// Built-in external: <<eof>> tests end of input
private root_item ::= !<<eof>> statement ';'

// Empty external expression (valid)
private empty_ext ::= <<>>

// Parameter passing in external expressions
// Double-quoted strings passed "as is": "1+1" passes the string 1+1
// Single-quoted strings are unquoted: '1+1' passes 1+1
// Rule references passed as Parser instances
external parameterized_rule ::= parseIt "qualified.Enum.VALUE" '1+1' some_rule
```

The corresponding Java implementation:

```java
public class MyParserUtil {
  // Required signature: PsiBuilder, int level, then extra parameters
  public static boolean parseMyRule(PsiBuilder builder, int level,
                                    boolean extraArg1, int extraArg2) {
    // Custom parsing logic
    return true;
  }
}
```

The method must be `public static`, return `boolean`, and take `PsiBuilder` and `int level` as its first two parameters. Any extra parameters follow. The method must live in the class specified by `parserUtilClass` or in a class imported via `parserImports`. Double-quoted string arguments are passed as-is, single-quoted strings are unquoted first, and rule references are passed as `Parser` instances (a functional interface).

### Meta Rules

Meta rules are parametrized rules that accept other parse functions as arguments. Mark a rule with the `meta` modifier and reference parameters with `<<param_name>>` in the rule body. Invoke a meta rule using the external expression syntax `<<meta_rule arg>>`.

```bnf
// Basic meta rule: the comma-separated list pattern
meta comma_list ::= <<param>> (',' <<param>>) *

// Using a meta rule — pass a rule reference as the argument
option_list ::= <<comma_list option>>

// Pass a choice expression as argument (in parentheses)
keyword_list ::= <<comma_list (SELECT | INSERT | DELETE)>>

// Meta rule with multiple parameters
meta two_params ::= <<a>> '=' <<b>>
assignment_list ::= <<two_params id number>>

// Pinned meta rule (comma-separated with recovery)
meta comma_list_pinned ::= <<head>> <<item>> (<<comma_list_tail <<item>>>>) *
meta comma_list_tail ::= ',' <<item>> {pin=1}

// Nested meta calls
nested_example ::= <<comma_list <<comma_list some_rule>>>>

// Meta rule with parenthesized list
private meta paren_list ::= '(' <<param>> (',' <<param>>) * ')' {pin=1}
function_args ::= <<paren_list expr>>

// Arguments can be: rule references, (choices), [optionals], {alt_choices}
usage1 ::= <<comma_list rule_ref>>
usage2 ::= <<comma_list (a | b | c)>>
usage3 ::= <<comma_list [optional_item]>>
usage4 ::= <<comma_list {alt1 | alt2}>>
```

The `comma_list` pattern shown above is the most common meta rule in practice. It factors out the repetitive "item, separator, item" structure so you can reuse it across your grammar. Arguments can be rule references, parenthesized choice expressions, bracket-wrapped optionals, or brace-wrapped alternatives. Meta rules can also be nested: `<<comma_list <<comma_list some_rule>>>>`.

### Attributes (Syntax Overview)

Attributes configure parser generation and PSI output. They appear in two places: global attributes in `{ }` blocks at the top of the file (or after a `;` separator), and rule-level attributes in `{ }` immediately after a rule expression.

```bnf
// Global attributes at top of file
{
  // Simple key=value pairs
  parserClass="com.example.MyParser"
  generatePsi=true

  // List values
  tokens=[PLUS='+' MINUS='-' id='regexp:\w+']
  parserImports=["static com.example.ManualParsing.*"]

  // Pattern-based attributes — regex matched against rule names
  extends(".*_expr")=expr               // all *_expr rules extend expr
  pin(".*_list(?:_\\d+)*")=1            // pin=1 on all *_list rules
  name(".*_expr")='expression'          // display name for error messages
  consumeTokenMethod(".*_recover")="consumeTokenFast"
}

// Rule-level attributes (placed after rule expression)
property ::= id '=' expr {pin=2}

// Rule-level attributes with multiple values
list_item ::= number {recoverWhile=item_recover elementType=my_type}

// Pattern attributes in global block target sub-expressions too
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
// pin(".*")=1 applies pin=1 to every sub-sequence in the rule
```

Attribute values can be identifiers, strings, numbers, or lists (`[item1 item2]`). Pattern-based attributes use Java regex matched against rule names, and they apply to sub-expressions within matching rules as well. The `name` attribute changes how a rule appears in error messages, and `pin` and `recoverWhile` control error recovery behavior (see [Error Recovery](error-recovery.md)).

This page covers attribute syntax only. For the full catalog of all 38+ attributes with their types, defaults, and effects, see [Attributes System](../code-generation/attributes.md).

## Complete Example

This JSON grammar demonstrates most syntax features working together. It is taken from Grammar-Kit's test data:

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

array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1}
private item ::= json {recoverWhile=recover}
object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}
name ::= id | string {name="name"}
private recover ::= !(',' | ']' | '}' | '[' | '{')
```

This grammar uses regexp tokens for Live Preview, pattern-based `extends` for PSI hierarchy, `pin(".*")=1` to pin all sub-sequences, not-predicates (`!']'`, `!'}' `) to prevent consuming closing delimiters, a shared `recover` predicate for both array items and object properties, and `name` attributes to improve error messages. For a full walkthrough of grammar design decisions like these, see [Grammar Design](grammar-design.md).

## Generated Method Names

Each rule generates a static method named after the rule. Sub-expressions within a rule generate helper methods with numeric suffixes: `rule_name_0(..)`, `rule_name_1_2(..)`, and so on. Avoid naming your own rules with these numeric suffix patterns (like `my_rule_0`) to prevent conflicts with generated helper methods.
