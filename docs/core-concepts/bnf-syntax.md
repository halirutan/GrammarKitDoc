# BNF Grammar Syntax

Grammar-Kit uses an extended BNF (Backus-Naur Form) syntax for defining language grammars. This syntax combines standard BNF notation with PEG-like features such as predicates and quantifiers.

## Grammar Structure

A Grammar-Kit BNF file contains three main parts: header attributes, token definitions, and grammar rules. Header attributes configure parser generation. Tokens define lexical elements. Rules specify the grammar structure.

### File Organization

BNF files follow this structure:

- Header attributes: `{ ... }` at file start
- Token definitions: `tokens = [ ... ]` in header
- Grammar rules: `rule_name ::= expression`
- Rule attributes: `{pin=1 recoverWhile=...}` after rule
- Comments: `// line comment`, `/* block comment */`

```bnf
{
  tokens = [
    PLUS='+'
    id='regexp:\\w+'
  ]
}

root ::= expression
expression ::= id '+' id
```

Comments use Java syntax: `//` for line comments and `/* */` for block comments. Semicolons between rules are optional.

### Header Attributes

The header block appears at the beginning of the file, enclosed in braces. It contains global configuration attributes that control parser generation and PSI structure. Common attributes include `parserClass` for the generated parser class name, `psiPackage` for the PSI classes package, and `tokens` for lexical token definitions.

Pattern-based attributes apply settings to multiple rules matching a pattern. For example, `extends(".*_expr")=expr` makes all rules ending with `_expr` extend a common expression class.

### Token Definitions

Tokens represent the lexical elements of your language. Define them in the `tokens` array within the header block. Grammar-Kit supports three token types: literal tokens (quoted strings), named tokens (uppercase identifiers), and regexp tokens (regular expressions).

```bnf
tokens = [
  // Named tokens
  EQ='='
  LPAREN='('
  
  // Regexp tokens
  id='regexp:[a-zA-Z]+'
  string='regexp:"[^"]*"'
  
  // Keywords
  IF='if'
  THEN='then'
]
```

Token declaration order determines precedence in Live Preview. Live Preview requires regexp tokens to function.

### Grammar Rules

Rules define the syntactic structure of your language. Each rule follows the format `rule_name ::= expression`. Rule names use lowercase with underscores. The expression specifies what the rule matches.

```bnf
assignment ::= id '=' expression
if_stmt ::= 'if' expr 'then' statement
```

Rules can reference other rules and tokens. The first rule typically serves as the root rule for parsing.

### Rule Modifiers

Rule modifiers control PSI node generation and parsing behavior. Place modifiers before the rule name:

- `private`: Skip PSI node creation for internal rules
- `external`: Delegate to hand-written parser method
- `meta`: Create parameterized rule template
- `inner`: Inject result into left sibling
- `left`: Wrap left sibling for left-associative parsing
- `upper`: Replace parent node with this rule's result
- `fake`: Define PSI structure without parsing

```bnf
expr ::= private_term (op private_term)*
private private_term ::= number | id

external parse_string ::= parseStringContents

meta list ::= <<item>> (',' <<item>>)*
numbers ::= <<list number>>
```

## Rule Syntax

Grammar-Kit provides operators for composing rules. These operators express sequences, alternatives, repetition, and lookahead patterns.

### Sequences and Choices

Sequences list elements that must appear in order, separated by spaces. The choice operator `|` specifies alternatives.

```bnf
// Sequence
assignment ::= id '=' expression

// Choice
value ::= number | string | boolean
boolean ::= 'true' | 'false'

// Combined
statement ::= assignment | if_stmt | while_stmt
if_stmt ::= 'if' expr 'then' statement
```

Grammar-Kit tries each alternative in order until one succeeds.

### Quantifiers

Quantifiers specify how many times an element can appear:

- `?` makes an element optional (zero or one)
- `+` requires one or more occurrences
- `*` allows zero or more occurrences

```bnf
// Optional
function ::= 'def' id params? body
params ::= '(' param_list ')'

// One or more
param_list ::= param (',' param)+
block ::= '{' statement+ '}'

// Zero or more
program ::= statement*
args ::= arg (',' arg)*
```

Square brackets `[expression]` provide alternative syntax for optional elements.

### Grouping with Parentheses

Parentheses group elements together. Apply quantifiers to the entire group or group alternatives within a larger expression.

```bnf
// Simple grouping
expr ::= term ('+' term)*

// Group alternatives
declaration ::= ('var' | 'const') id ('=' value)?

// Nested groups
list ::= '[' (value (',' value)*)? ']'
```

Braces `{expression}` provide alternative grouping syntax. External expression syntax `<<expression>>` invokes external parsing methods or meta rules.

### Predicates

Predicates perform lookahead without consuming input. The and-predicate `&` succeeds if the pattern matches at the current position. The not-predicate `!` succeeds if the pattern does not match.

```bnf
// And predicate - positive lookahead
keyword_id ::= &keyword id
keyword ::= 'if' | 'then' | 'else'

// Not predicate - negative lookahead
expr_end ::= !'+' !'-'
safe_id ::= !keyword id

// EOF predicate
file ::= item* !<<eof>>
item ::= !<<eof>> statement
```

The `<<eof>>` predicate checks for end of file.

## Token Types

Grammar-Kit supports three token types for different purposes in your grammar.

### Literal Tokens

Literal tokens match exact strings. Enclose them in single or double quotes. Grammar-Kit matches these tokens by their text value.

```bnf
rule ::= 'keyword' | "symbol"
```

Define named literal tokens in the tokens array:

```bnf
tokens = [
  SEMI=';'
  PLUS='+'
  KEYWORD='if'
]
```

Named tokens improve readability. Reference the same literal by name or value.

### Named Tokens

Named tokens use uppercase identifiers with underscores. Define them in the tokens array with their corresponding literal or regexp value. Reference them in rules by name.

```bnf
tokens = [
  OP_EQ="="
  OP_IS="::="
]

rule_def ::= id OP_IS expression
```

### Regexp Tokens

Regexp tokens match patterns using regular expressions. Prefix the pattern with `regexp:` in the token definition. Live Preview requires these tokens.

```bnf
tokens = [
  id='regexp:\\w+'
  number='regexp:\\d+'
  space='regexp:\\s+'
  string='regexp:('([^'\\\\]|\\\\.)*'|"([^"\\\\]|\\\\"|\\\\\'|\\\\)*")'
  line_comment='regexp://.*'
  block_comment='regexp:/\\*(.|\n)*\\*/'
]
```

Use standard regular expression syntax, escaping backslashes as needed.

### Token Precedence in Live Preview

Live Preview requires regexp tokens. Token declaration order determines precedence when multiple tokens could match the same input. Place more specific tokens before general ones.

Keyword tokens (where name equals value) receive special handling for efficiency. Text-matched tokens are slower than regexp tokens. Prefer regexp tokens when possible.

## Common Patterns

Common patterns in Grammar-Kit grammars include optional trailing separators:
```bnf
rule ::= id '::=' expr ';'?
```

Lists with separators:
```bnf
list ::= item (',' item)*
```

Block structures:
```bnf
block ::= '{' statement* '}'
```

## Common Mistakes

Avoid these errors when writing BNF grammars. Missing regexp prefix causes Live Preview to fail:
```bnf
tokens = [
  id='\\w+'  // WRONG: needs regexp:
]
```

Quantifiers must appear on elements, not between them:
```bnf
rule ::= id? '::=' expr  // WRONG
rule ::= id '::='? expr  // WRONG
```

Token names must follow naming conventions:
```bnf
tokens = [
  my-token='-'  // WRONG: use MY_TOKEN
  123='123'     // WRONG: start with letter
]
```

Choice order matters. The first matching alternative wins:
```bnf
expr ::= id | id '=' value  // WRONG: second alternative unreachable
```

## Next

Explore [Grammar Attributes](attributes.md) to control parser generation behavior, or try the [Live Preview](live-preview.md) tool to test your grammar interactively.