# Code Evidence: BNF Grammar Syntax

## Scope Information
This evidence covers section 2.1: BNF Grammar Syntax

## Grammar Structure

### File Organization
- Header attributes: `{ ... }` at file start
- Token definitions: `tokens = [ ... ]` in header
- Grammar rules: `rule_name ::= expression`
- Rule attributes: `{pin=1 recoverWhile=...}` after rule
- Comments: `// line comment`, `/* block comment */`

### Header Attributes Block
- Global attributes: `{ generate=[...] }`
- Parser class: `parserClass="package.ClassName"`
- PSI configuration: `psiPackage=`, `psiClassPrefix=`
- Token configuration: `tokens = [ ... ]`
- Pattern-based attributes: `extends(".*_expr")=expr`

## Rule Syntax

### Basic Rule Definition
- Rule format: `rule_name ::= expression`
- Alternative syntax: `rule_name ::= expression ;`
- Rule separator: semicolon optional
- Rule naming: lowercase with underscores

### Sequences and Choices
- Sequence: `rule_A rule_B rule_C`
- Choice operator: `|`
- Choice syntax: `rule ::= option1 | option2 | option3`
- Alternative choice: `{ option1 | option2 }`

### Quantifiers
- Optional: `?` suffix
- One or more: `+` suffix
- Zero or more: `*` suffix
- Optional brackets: `[ expression ]`

### Grouping Constructs
- Parentheses: `( expression )`
- Braces: `{ expression }`
- Brackets: `[ expression ]`
- External expression: `<< expression >>`

### Predicates
- And predicate: `& expression`
- Not predicate: `! expression`
- Predicate rule: `predicate ::= predicate_sign simple`
- EOF predicate: `!<<eof>>`

## Rule Modifiers
- `private`: Skip PSI node creation
- `external`: Hand-written parse function
- `meta`: Parametrized rule
- `inner`: Inject into left sibling
- `left`: Enclose left sibling
- `upper`: Replace parent node
- `fake`: PSI shaping only

## Token Types

### Literal Tokens
- Single quotes: `'keyword'`
- Double quotes: `"symbol"`
- Text-matched: matched by string value
- Implicit tokens: unquoted literals

### Named Tokens
- Token declaration: `PLUS='+'`
- Token reference: `PLUS` or `'+'`
- Token naming: UPPER_CASE convention

### Regexp Tokens
- Regexp syntax: `id="regexp:\\w+"`
- Regexp prefix: `regexp:` required
- Live Preview requirement: regexp tokens needed
- Pattern examples: `space='regexp:\\s+'`

### Token Declaration Syntax
```
tokens = [
  OP_EQ="="
  OP_IS="::="
  id="regexp:\\w+"
  string="regexp:('([^'\\\\]|\\\\.)*'|\"([^\"\\\\]|\\\\\"|\\\\\'|\\\\)*\")"
  line_comment="regexp://.*"
  block_comment="regexp:/\\*(.|\n)*\\*/"
]
```

## Special Operators

### Meta Rules
- Meta definition: `meta rule_name ::= <<param>>`
- Meta application: `<<rule_name argument>>`
- Parameter syntax: `<<p1>>`, `<<p2>>`
- Inline parameters: `<<list rule_D>>`

### External Expressions
- External syntax: `<< methodName args >>`
- EOF check: `<<eof>>`
- Empty external: `<<>>`
- Parser reference: rule names as parameters

### Special Tokens
- End of file: `<<eof>>`
- Rule start operator: `::=`
- Assignment operator: `=` in attributes

## Token Precedence in Live Preview
- Regexp tokens: Required for Live Preview
- Token order: Declaration order matters
- Keyword tokens: Name equals value
- Text tokens: Slower, matched by text
- Token conflicts: Use names to resolve

## Example Locations
- `grammars/Grammar.bnf`: Complete BNF self-definition
- `testData/livePreview/Json.bnf`: JSON grammar example
- `testData/generator/ExternalRules.bnf`: Meta rules, external expressions
- `testData/generator/ExprParser.bnf`: Expression parsing, precedence
- `testData/livePreview/LivePreviewTutorial.bnf`: Tutorial grammar

## Out of Scope
Features found but excluded (belong to other sections):
- Pin attribute details → Section 2.2
- RecoverWhile attribute → Section 2.2
- Live Preview interface usage → Section 2.3
- Expression parsing patterns → Section 3.2
- Parser generation process → Section 4.1