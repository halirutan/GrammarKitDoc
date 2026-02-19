# Section 5.3: Debugging Techniques — Code Evidence

## 1. Quick Documentation (Ctrl-Q)

**Source: `src/org/intellij/grammar/BnfDocumentationProvider.java:33-146`**

For any BNF rule, documentation shows:
- **Starts with**: FIRST set (tokens that can start the rule)
- **Followed by**: NEXT set (tokens that can follow the rule)
- **#auto recovery predicate**: the auto-generated recovery rule for `recoverWhile="#auto"`
- **Priority table**: for expression parsing rules (operator types and priorities)
- **Contains**: public rules, tokens, and external rules with cardinalities

For attributes: shows HTML description from `attributeDescriptions/<name>.html`.

## 2. BnfFirstNextAnalyzer

**Source: `src/org/intellij/grammar/analysis/BnfFirstNextAnalyzer.java:36-60`**

Core analysis tool computing FIRST and NEXT sets:
- `calcFirst(rule)` — which tokens can start parsing a rule
- `calcNext(rule)` — which tokens can follow after a rule matches
- Special markers: `MATCHES_EOF` (`-eof-`), `MATCHES_NOTHING` (`-never-matches-`), `MATCHES_ANY` (`-any-`)

Configuration options:
- `myBackward` — analyze in reverse direction
- `myPublicRuleOpaque` — treat public rules as opaque (don't recurse into them)
- `myPredicateLookAhead` — follow predicates

## 3. Live Preview for Grammar Debugging

**Source: `src/org/intellij/grammar/livePreview/LivePreviewHelper.java`**

Live Preview features for debugging:
- Real-time PSI tree in Structure View
- Grammar-at-caret highlighting (Ctrl-Alt-F7)
- Error elements shown with `CodeInsightColors.ERRORS_ATTRIBUTES`
- Auto-reparse on grammar changes (500ms debounce)

## 4. Grammar Highlighting Action

**Source: `src/org/intellij/grammar/livePreview/GrammarAtCaretPassFactory.java:36-120`**

When enabled, highlights BNF expressions that correspond to the caret position in the preview:
- **Matched expressions**: `EditorColors.SEARCH_RESULT_ATTRIBUTES`
- **Unmatched expressions**: `EditorColors.WRITE_SEARCH_RESULT_ATTRIBUTES`

## 5. Pin Marker Annotator

**Source: `src/org/intellij/grammar/editor/BnfPinMarkerAnnotator.java`**

Visually marks pinned elements in the grammar editor, helping developers understand which token commits the parser to a particular rule.

## 6. Recursion Line Markers

**Source: `src/org/intellij/grammar/editor/BnfRecursionLineMarkerProvider.java`**

Gutter icons indicating recursive rules, helping identify potential infinite recursion.

## 7. Rule Line Markers

**Source: `src/org/intellij/grammar/editor/BnfRuleLineMarkerProvider.java`**

Gutter navigation for rule hierarchies (extends relationships).

## 8. LightPsi for Isolated Testing

**Source: `src/org/intellij/grammar/LightPsi.java:49-82`**

Enables parsing in isolation without a full IDE environment:
```java
PsiFile file = LightPsi.parseFile("test.bnf", grammarText, new BnfParserDefinition());
```

Useful for debugging grammar issues outside the IDE.

## 9. LivePreviewParser Recursion Detection

**Source: `src/org/intellij/grammar/livePreview/LivePreviewParser.java:121-132`**

Live Preview detects endless recursion at runtime:
- Maintains a `BitSet` per input offset
- Each rule call at a given offset sets a bit
- If the bit is already set: reports `"Endless recursion detected for '<rule>'"`

## 10. Expression Parsing Debug Info

**Source: `src/org/intellij/grammar/BnfDocumentationProvider.java:109-128`**

For expression rules, the documentation provider dumps the priority table showing:
- Operator type (BINARY, N_ARY, PREFIX, POSTFIX, ATOM)
- Priority level
- Current rule highlighted in the table
