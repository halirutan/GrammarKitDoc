A macOS-style IDE window (red, yellow, green window buttons) shows a dark-themed editor open on the file `.../grammars/Grammar.bnf` from JetBrains “Grammar-Kit”. The screenshot is used in the project README as an “Editor support” illustration.

The editor contains an excerpt of Grammar-Kit’s own BNF grammar (a PEG-style grammar used to describe and parse `.bnf` files and generate IntelliJ parser and PSI code). Syntax highlighting distinguishes rules, tokens, and quoted text. Large yellow labels on the right point to specific lines, each label connected by a thin yellow arrow. ([GitHub][1])

## Yellow callouts and what they point to

* **Tokens** → two token definitions using regex-based token declarations for comments:

    * `line_comment="regexp://.*"`
    * `block_comment="regexp:/\*(.|\n)*\*/"`
      These live inside a global attributes block (the code shows a closing `]` after the token list).

* **PSI mix-in classes** → global mappings that bind grammar rules to PSI interfaces/implementations (Java class names shown in quotes), using `implements(...)`, `extends(...)`, and `mixin(...)`.

* **Matched rules** → a pattern-based mapping that applies to multiple rules at once:

    * `extends("paren_.*expression")=parenthesized`
      This demonstrates that Grammar-Kit can apply attributes by rule-name pattern.

* **Pinned predicate w/ external call** → the root rule is declared `external` and calls a hand-written method, then the next rule begins with a predicate:

    * `external grammar ::= parseGrammar grammar_element`
    * `private grammar_element ::= !<<eof>> (attrs | rule) { pin=1 recoverWhile=grammar_element_recover }`
      This combines an external entry point with a negative lookahead predicate and error-recovery attributes.

* **Pin marker** → a rule attribute block containing `{pin=...}`:

    * `rule ::= rule_start expression attrs? ';'? {pin=2}`
      (Pin is an error-recovery hint that treats a sequence as “committed” once the pinned item is reached.)

* **Match by text** → string-literal keywords matched as implicit “text-matched tokens”:

    * `modifier ::= 'private' | 'external' | 'meta' | 'inner' | 'left' | 'upper' | 'fake'`
      The label emphasizes matching by literal text rather than by a lexer token type.

* **Match by token type** → token-type-based matching using a token like `=` (as produced by the lexer), inside an attribute-start rule:

    * `private attr_start ::= id (attr_pattern '=' | '=')`
      This contrasts with quoted text matching.

* **PSI accessor renamed** → a `methods=[...]` directive that renames a generated PSI accessor for a child rule:

    * `methods=[literalExpression="string_literal_expression"]`

* **Optimized PSI** → use of `extends=expression` in a rule attribute block to shape or reuse PSI structure:

    * `value_list ::= '[' list_entry* ']' {pin=1 extends=expression}`

* **Recover predicate** → `recoverWhile=...` points at a predicate rule used to skip tokens during recovery:

    * `sequence ::= option* { extends=expression recoverWhile=sequence_recover }`
    * `private sequence_recover ::= !( ... ) grammar_element_recover`
      (The negated group lists terminators like `;`, `|`, `||`, `}`, `]`, `)`, `,`.)

* **Pin sub-expressions** → pinning applied to nested sequences via a target pattern:

    * `left choice ::= ('||' sequence)+ {pin(".*")=1 extends=expression}`
      This demonstrates applying pin not only to a top-level sequence but also to sub-expressions.

## BNF excerpt shown (transcribed from the screenshot)

```bnf
line_comment="regexp://.*"
block_comment="regexp:/\*(.|\n)*\*/"

implements("rule[attr]")="org.intellij.grammar.psi.BnfNamedElement"
extends("rule[attr]")="org.intellij.grammar.psi.impl.BnfNamedImpl"
mixin("reference_or_token")="org.intellij.grammar.psi.impl.BnfRefOrTokenImpl"
mixin("string_literal_expression")="org.intellij.grammar.psi.impl.BnfStringImpl"
extends("paren_.*expression")=parenthesized

external grammar ::= parseGrammar grammar_element

private grammar_element ::= !<<eof>> (attrs | rule)
  { pin=1 recoverWhile=grammar_element_recover }
private grammar_element_recover ::= !( '{' | rule_start )

rule ::= rule_start expression attrs? ';'? {pin=2}
private rule_start ::= modifier* id '::='?
modifier ::= 'private' | 'external' | 'meta'
         | 'inner' | 'left' | 'upper' | 'fake'

attrs ::= '{' attr* '}' {pin=1}
attr ::= attr_start attr_value ';'?
  { pin=1 recoverWhile=attr_recover }
private attr_start ::= id (attr_pattern '=' | '=')
  { pin(".*")="attr_pattern" }
private attr_start_simple ::= id attr_pattern? '='
private attr_recover ::= !('}' | attr_start)
private attr_value ::= attr_value_inner ';'?
private attr_value_inner ::= reference_or_token
                         | literal_expression
                         | value_list

attr_pattern ::= '(' string_literal_expression ')'
  { pin=1
    methods=[literalExpression="string_literal_expression"] }

value_list ::= '[' list_entry* ']' {pin=1 extends=expression}
list_entry ::= (id list_entry_tail? | string_literal_expression) ';'?
  { recoverWhile=list_entry_recover
    methods=[getReferences literalExpression="string_literal_expression"] }
private list_entry_tail ::= '=' string_literal_expression {pin=1}
private list_entry_recover ::= !(']' | '}' | id | string)

expression ::= sequence choice?
sequence ::= option* { extends=expression recoverWhile=sequence_recover }
private sequence_recover ::= !(';' | '|' | '||' | '}' | ']' | ')' | ',') grammar_element_recover
private option ::= predicate | paren_opt_expression | simple quantified?

left choice ::= ('||' sequence)+ {pin(".*")=1 extends=expression}
left quantified ::= quantifier {extends=expression}
quantifier ::= '?' | '+' | '*'

predicate ::= predicate_sign simple {extends=expression}
predicate_sign ::= '&' | '!'
```

## Context the screenshot assumes

Grammar-Kit is an IntelliJ IDEA plugin that adds BNF/JFlex editing and generates parsers and PSI trees from `.bnf` grammars; this image highlights the Grammar-Kit-specific syntax features that support PSI customization and error recovery (`pin`, `recoverWhile`, external rules, token declarations, and pattern-applied attributes). ([GitHub][1])

[1]: https://github.com/JetBrains/Grammar-Kit "GitHub - JetBrains/Grammar-Kit: Grammar files support & parser/PSI generation for IntelliJ IDEA"
