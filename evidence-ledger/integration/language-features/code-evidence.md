# Section 4.1.2: Language Features — Code Evidence

## 1. Syntax Highlighting

**Source: `src/org/intellij/grammar/editor/BnfSyntaxHighlighter.java:23-83`**

16 text attribute keys defined:

| Key | Based On | Used For |
|---|---|---|
| `BNF_ILLEGAL` | `INVALID_STRING_ESCAPE` | Bad characters |
| `BNF_COMMENT` | `LINE_COMMENT` | Comments |
| `BNF_STRING` | `STRING` | String literals |
| `BNF_PATTERN` | `INSTANCE_FIELD` | Attribute patterns |
| `BNF_NUMBER` | `NUMBER` | Numbers |
| `BNF_KEYWORD` | `MARKUP_ATTRIBUTE` | Keywords/modifiers |
| `BNF_TOKEN` | `STRING` | Explicit tokens |
| `BNF_IMPLICIT_TOKEN` | `STATIC_FIELD` | Implicit tokens |
| `BNF_RULE` | `KEYWORD` | Rule names |
| `BNF_META_RULE` | `KEYWORD` | Meta rule names |
| `BNF_META_RULE_PARAM` | (custom) | Meta parameters |
| `BNF_ATTRIBUTE` | `INTERFACE_NAME` | Attribute names |
| `BNF_EXTERNAL` | `STATIC_METHOD` | External references |
| `BNF_PIN` | `REASSIGNED_LOCAL_VARIABLE` | Pin markers |
| `BNF_RECOVER_MARKER` | (custom) | Recovery markers |
| `BNF_OP_SIGN` | `OPERATION_SIGN` | Operators |

## 2. Annotator-Based Highlighting

**Source: `src/org/intellij/grammar/editor/BnfAnnotator.java:31-169`**

The `BnfAnnotator` (implements `DumbAware`) provides semantic highlighting:
- Rule names: `BnfSyntaxHighlighter.RULE` or `META_RULE` based on `Rule.isMeta()`
- Attributes: `BnfSyntaxHighlighter.ATTRIBUTE`
- Modifiers: `BnfSyntaxHighlighter.KEYWORD`
- Method mix-ins in `methods` attribute: `BnfSyntaxHighlighter.EXTERNAL`
- External references: `BnfSyntaxHighlighter.EXTERNAL` or `META_PARAM`
- Explicit tokens: `BnfSyntaxHighlighter.EXPLICIT_TOKEN`
- Implicit tokens: `BnfSyntaxHighlighter.IMPLICIT_TOKEN`
- Attribute values/patterns: `BnfSyntaxHighlighter.PATTERN`
- Text-matched tokens: warning "Tokens matched by text are slower than tokens matched by types"
- Recovery rules: `BnfSyntaxHighlighter.RECOVER_MARKER` overlay

Additional annotators:
- `BnfPinMarkerAnnotator` — highlights pinned expressions
- `BnfExpressionMarkerAnnotator` — highlights expression parsing markers

## 3. Code Completion

**Source: `src/org/intellij/grammar/BnfCompletionContributor.java:46-152`**

Three completion providers:
1. **Attribute completion**: In `{...}` blocks, suggests all `KnownAttribute` names with icons. Filters global attributes when inside a rule.
2. **Token/identifier completion**: Outside attributes, suggests explicit tokens and unresolved token references from all rules.
3. **Rule reference completion**: Suggests rule names with icons (bold for public, strikethrough for fake). In external contexts, suggests only meta rules and static methods from `parserUtilClass`.

The contributor also implements **parser-based keyword completion** using `GeneratedParserUtilBase.CompletionState` to suggest context-aware keywords.

## 4. Structure View

**Source: `src/org/intellij/grammar/BnfStructureViewFactory.java:32-149`**

Shows:
- File name as root
- `BnfAttrs` blocks (shown as "Attributes { first_attr & N more... }")
- `BnfRule` entries (shown by name)
- `BnfAttr` entries within attrs blocks (shown as "name(pattern) = value")

Rules and attributes are always leaves; attribute groups always show the plus icon.

## 5. Find Usages

**Source: `src/org/intellij/grammar/BnfFindUsagesProvider.java:20-50`**

- `canFindUsagesFor()` returns true for `BnfRule` and `BnfAttr` instances.
- Type/name descriptions delegate to `ElementDescriptionUtil`.
- Pattern reference searches via `BnfAttrPatternRefSearcher`.

## 6. Navigation and Documentation

**Source: `src/org/intellij/grammar/BnfDocumentationProvider.java:33-146`**

Quick documentation (Ctrl-Q) for rules shows:
- **Starts with**: FIRST set tokens
- **Followed by**: NEXT set tokens
- **#auto recovery predicate**: generated predicate for `recoverWhile="#auto"`
- **Priority table**: for expression parsing rules
- **Contains**: public rules, tokens, and external rules with cardinalities

For attributes: shows the HTML description from `attributeDescriptions/<name>.html`.

## 7. Refactoring Support

**Source: `src/org/intellij/grammar/refactor/`**

- `BnfRefactoringSupportProvider` — enables in-place rename for `BnfNamedElement`
- `BnfInlineRuleActionHandler` / `BnfInlineRuleProcessor` — inline rule refactoring
- `BnfIntroduceRuleAction` / `BnfIntroduceRuleHandler` — extract rule (uses shortcut of ExtractMethod)
- `BnfIntroduceTokenAction` / `BnfIntroduceTokenHandler` — extract token (uses shortcut of IntroduceConstant)
- `BnfNamesValidator` — validates rule/token names
- `BnfUnwrapDescriptor` — unwrap parentheses/brackets
- `BnfExpressionOptimizer` — expression simplification

**Registered actions (from `plugin.xml:126-133`):**
```xml
<action id="grammars.IntroduceRule" use-shortcut-of="ExtractMethod"/>
<action id="grammars.IntroduceToken" use-shortcut-of="IntroduceConstant"/>
```

## 8. Inspections

**Source: `src/org/intellij/grammar/inspection/`**

8 inspections registered (all enabled by default, WARNING level):

| Inspection | Class | Description |
|---|---|---|
| Unresolved reference | `BnfResolveInspection` | Unresolved rule, method, or pattern references |
| Unused rule | `BnfUnusedRuleInspection` | Rules not reachable from root or extra roots |
| Unused attribute | `BnfUnusedAttributeInspection` | Attributes with no effect |
| Suspicious token | `BnfSuspiciousTokenInspection` | Token that looks like a missing rule reference |
| Left recursion | `BnfLeftRecursionInspection` | Left recursion unsupported by generator |
| Duplicate rule | `BnfDuplicateRuleInspection` | Rules with the same name |
| Identical choice branches | `BnfIdenticalChoiceBranchesInspection` | Duplicate alternatives |
| Unreachable choice branch | `BnfUnreachableChoiceBranchInspection` | Branch masked by earlier alternative |

Suppression via comments: `//noinspection BnfUnusedRule` (supported via `BnfInspectionSuppressor`).

## 9. Intentions

**Source: `plugin.xml:84-93`**

- `BnfFlipChoiceIntention` — flip choice branches (`a | b` → `b | a`)
- `BnfConvertOptExpressionIntention` — convert `expr?` to `[expr]` and back

## 10. Additional Editor Features

**Source: `plugin.xml` and `src/org/intellij/grammar/editor/`**

| Feature | Class | Description |
|---|---|---|
| Line markers | `BnfRuleLineMarkerProvider` | Rule hierarchy navigation |
| Recursion markers | `BnfRecursionLineMarkerProvider` | Recursive rule indicators |
| Brace matching | `BnfBraceMatcher` | Matching `(){}[]<<>>` |
| Commenter | `BnfCommenter` | Line comment `//` support |
| Folding | `BnfFoldingBuilder` | Fold attribute blocks, comments |
| Word selection | `BnfWordSelectioner` | Smart word selection |
| Move left/right | `BnfMoveLeftRightHandler` | Move choice branches |
| Quote handler | `BnfQuoteHandler` | Auto-close quotes |
| Spell checking | `BnfSpellCheckingStrategy` | Spell check in strings |
| Color settings | `BnfColorSettingsPage` | Customizable colors |
| Regexp injection | `BnfStringRegexpInjector` | Regexp in string literals |
| String manipulation | `BnfStringManipulator` | String element editing |
