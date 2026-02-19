# Grammar Syntax Reference

This page is a complete reference for Grammar-Kit's BNF grammar syntax. For a tutorial-style introduction, see [Grammar Syntax](../grammar-development/grammar-syntax.md).

## File Structure

A `.bnf` file consists of an optional attribute header block followed by rule definitions:

```bnf
{
  // attribute header block
  parserClass="com.example.MyParser"
}

// rule definitions
root ::= item *
item ::= id '=' value
```

The formal structure:

```
grammar     ::= grammar_element *
grammar_element ::= attrs | rule
```

## Rules

A rule associates a name with an expression. It may have modifiers, inline attributes, and an optional trailing semicolon:

```
rule ::= modifier* id '::=' expression attrs? ';'?
```

### Rule modifiers

| Modifier | Effect |
|---|---|
| `private` | No AST node generated. Child nodes fold into the parent. |
| `external` | No parsing code generated. The parse function is hand-written. |
| `meta` | Parametrized rule that takes parse functions as arguments. |
| `left` | Takes the previous sibling and becomes its parent (for left-associative operators). |
| `inner` | Used with `left`. Takes the previous sibling and becomes its child. |
| `upper` | Takes the parent node and replaces it. |
| `fake` | Only PSI classes are generated. No parsing code is produced. |

Multiple modifiers can combine on a single rule:

```bnf
private meta list_of ::= <<p>> (',' <<p>>) *
left inner assign_expr ::= '=' expr
```

## Expressions

The right-hand side of a rule is an expression built from sequences, choices, and quantified terms:

```
expression ::= sequence ('|' sequence)*
sequence   ::= option+
option     ::= predicate | quantified | paren_expr | simple
```

### Choices

The `|` operator separates alternatives. The parser tries each branch in order:

```bnf
value ::= number | string | object | array
```

### Sequences

Adjacent terms form a sequence that must match in order:

```bnf
pair ::= key ':' value
```

### Quantifiers

| Operator | Meaning | Example |
|---|---|---|
| `?` | Zero or one (optional) | `';'?` |
| `*` | Zero or more | `item *` |
| `+` | One or more | `item +` |

```bnf
item_list ::= item (',' item) *
optional_semi ::= ';'?
arguments ::= expr (',' expr) +
```

### Predicates

Predicates test without consuming input. They are used for lookahead:

| Operator | Meaning | Example |
|---|---|---|
| `&` | Positive lookahead (succeeds if the expression matches) | `&'}'` |
| `!` | Negative lookahead (succeeds if the expression does not match) | `!'}'` |

```bnf
private item_recover ::= !(")" | ",")
private items ::= [!")" item (',' item) *]
```

## Grouping

### Parentheses `( )`

Group expressions with standard precedence:

```bnf
list ::= '(' item (',' item) * ')'
```

### Brackets `[ ]`

Brackets denote an optional group, equivalent to `(...)?`:

```bnf
// These two forms are equivalent:
optional_items ::= [item (',' item) *]
optional_items ::= (item (',' item) *)?
```

### Braces `{ }` in expressions

Within a rule body, braces create an alternative grouping. At the top level, braces delimit attribute blocks.

## Tokens and Literals

### String literals

Quoted strings match literal text. Both single and double quotes work:

```bnf
plus ::= '+'
keyword ::= "while"
```

### Token references

Unquoted identifiers reference other rules or declared tokens:

```bnf
expr ::= number PLUS number
```

### Token declarations

The `tokens` attribute in the header block declares tokens with optional values:

```bnf
{
  tokens = [
    id="regexp:\w+"       // regexp token (regexp: prefix)
    string                // name only
    PLUS_OP="+"           // text-matched token
    SWITCH="switch"       // keyword token
  ]
}
```

Tokens have three categories:

- Regexp tokens use the `regexp:` prefix and define a lexer pattern. Required for Live Preview.
- Text-matched tokens have a quoted string value (e.g., `PLUS_OP="+"`).
- Name-only tokens have no value and are matched by the lexer based on external configuration.

## External Expressions

External expressions invoke methods not defined in the grammar. They are enclosed in `<< >>`:

```bnf
root ::= <<parseRoot item>>
meta comma_list ::= <<p>> (',' <<p>>) *
usage ::= <<comma_list expr>>
```

The first identifier inside `<< >>` is the method name. Subsequent items are arguments passed to it. External expressions work with `meta` rules to implement parametrized parsing.

## Attribute Blocks

Attribute blocks appear in curly braces. The header block at the top of the file sets global attributes. Inline attribute blocks on rules set rule-level attributes:

```bnf
{
  parserClass="com.example.MyParser"
  extends(".*_expr")=expr
}

item ::= number {pin=1 recoverWhile=item_recover}
```

Attribute syntax:

```
attrs       ::= '{' attr* '}'
attr        ::= id attr_pattern? '=' attr_value ';'?
attr_pattern ::= '(' string ')'
attr_value  ::= string | number | boolean | value_list | id
value_list  ::= '[' list_entry* ']'
list_entry  ::= (id ('=' string)? | string) ';'?
```

For the complete list of attributes, see [Attribute Reference](attributes.md).

## Comments

Grammar-Kit supports both comment styles:

```bnf
// Line comment: everything after // to end of line

/* Block comment:
   can span multiple lines */
```

## Operators Summary

| Symbol | Name | Meaning |
|---|---|---|
| `::=` | Definition | Defines a rule |
| `\|` | Choice | Separates alternatives |
| `?` | Optional | Zero or one |
| `*` | Repetition | Zero or more |
| `+` | One-or-more | One or more |
| `&` | And-predicate | Positive lookahead |
| `!` | Not-predicate | Negative lookahead |
| `=` | Assignment | Assigns an attribute value |
| `( )` | Parentheses | Groups expressions |
| `[ ]` | Brackets | Optional group (same as `(...)?`) |
| `{ }` | Braces | Attribute blocks |
| `<< >>` | External | External expression call |
| `//` | Line comment | Comment to end of line |
| `/* */` | Block comment | Multi-line comment |
| `;` | Semicolon | Optional statement terminator |

## Reserved Identifiers

Grammar-Kit reserves these identifiers for internal use:

| Identifier | Usage |
|---|---|
| `regexp:` | Prefix for regexp token definitions in the `tokens` attribute |
| `#auto` | Value for `recoverWhile` that means "not in NEXT set of this rule" |
| `TokenSets` | Generated inner class name for token set constants |
