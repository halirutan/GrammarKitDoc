# Section 6.2: Grammar Syntax Reference — Code Evidence

## 1. Grammar.bnf: Self-Describing Grammar

**Source: `grammars/Grammar.bnf:1-123`**

The BNF grammar syntax is defined by Grammar-Kit itself. Key constructs:

### File Structure
```
grammar ::= grammar_element *
grammar_element ::= attrs | rule
```

### Rule Syntax
```
rule ::= modifier* id '::=' expression attrs? ';'?
modifier ::= 'private' | 'external' | 'meta' | 'inner' | 'left' | 'upper' | 'fake'
```

### Expression Syntax
```
expression ::= sequence choice?
sequence ::= option *
choice ::= ( '|' sequence ) +            // left rule
option ::= predicate | paren_opt | simple quantified?
quantified ::= quantifier                 // left rule
quantifier ::= '?' | '+' | '*'
predicate ::= predicate_sign simple
predicate_sign ::= '&' | '!'
```

### Parenthesized Expressions
```
paren_expression ::= '(' expression ')' | '{' alt_choice_element '}'
paren_opt_expression ::= '[' expression ']'    // equivalent to (expression)?
```

### External Expressions
```
external_expression ::= '<<' reference_or_token option * '>>'
```

### Literals and References
```
reference_or_token ::= id
literal_expression ::= string_literal_expression | number
string_literal_expression ::= string
```

### Attribute Blocks
```
attrs ::= '{' attr * '}'
attr ::= id attr_pattern? '=' attr_value ';'?
attr_pattern ::= '(' string_literal_expression ')'
value_list ::= '[' list_entry * ']'
list_entry ::= (id ('=' string)? | string) ';'?
```

## 2. BnfConstants: Reserved Identifiers

**Source: `src/org/intellij/grammar/generator/BnfConstants.java:10-43`**

| Constant | Value | Usage |
|---|---|---|
| `REGEXP_PREFIX` | `"regexp:"` | Prefix for regexp token definitions |
| `RECOVER_AUTO` | `"#auto"` | Auto-recovery sentinel value |
| `TOKEN_SET_HOLDER_NAME` | `"TokenSets"` | Inner class name for token sets |
| `CLASS_HEADER_DEF` | `"// This is a generated file..."` | Default file header |

## 3. Token Definition Syntax

**Source: `attributeDescriptions/tokens.html`, `README.md:172-186`**

```bnf
{
  tokens = [
    id="regexp:\\w+"     // regexp token (has regexp: prefix)
    string               // name only, no value
    PLUS_OP="+"          // simple token (text value)
    SWITCH="switch"      // keyword token (name equals value after unquoting)
  ]
}
```

Three token types:
1. **Explicit named**: `NAME="value"` or `NAME="regexp:pattern"`
2. **Implicit keyword**: Used in rules, unquoted, name equals value
3. **Implicit text-matched**: Quoted string in rule body not in tokens list

## 4. Rule Modifiers

**Source: `README.md:131-147`**

| Modifier | Effect |
|---|---|
| `private` | No AST node; children fold into parent |
| `external` | Hand-written parse function; no parsing code generated |
| `meta` | Parametrized rule; takes parse functions as parameters |
| `left` | Takes previous sibling, becomes its parent |
| `inner` | Used with `left`; takes previous sibling, becomes its child |
| `upper` | Takes parent node, replaces it |
| `fake` | Only PSI classes generated, no parsing code |

## 5. Operators and Special Symbols

**Source: `grammars/Grammar.bnf:22-39`**

| Symbol | Token | Meaning |
|---|---|---|
| `=` | `OP_EQ` | Attribute assignment |
| `::=` | `OP_IS` | Rule definition |
| `\|` | `OP_OR` | Choice (alternative) |
| `?` | `OP_OPT` | Optional (zero or one) |
| `+` | `OP_ONEMORE` | One or more |
| `*` | `OP_ZEROMORE` | Zero or more |
| `&` | `OP_AND` | Positive lookahead predicate |
| `!` | `OP_NOT` | Negative lookahead predicate |
| `;` | `SEMICOLON` | Statement terminator |
| `<<` | `EXTERNAL_START` | External expression start |
| `>>` | `EXTERNAL_END` | External expression end |
| `(` `)` | Parens | Grouping |
| `{` `}` | Braces | Attribute blocks or choice grouping |
| `[` `]` | Brackets | Optional group (equivalent to `(...)? `) |

## 6. Comment Syntax

**Source: `grammars/Grammar.bnf:45-46`**

```bnf
line_comment="regexp://.*"
block_comment="regexp:/\\*(.|\n)*\\*/"
```

Both `//` line comments and `/* ... */` block comments are supported.
