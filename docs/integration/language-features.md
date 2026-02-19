# Language Features

Once your parser definition is registered, the IntelliJ Platform provides extension points for syntax highlighting, navigation, completion, refactoring, and code analysis. This page describes how Grammar-Kit's own BNF language uses these extension points. Use the same patterns when building language support on top of your generated parser.

## Syntax Highlighting

Highlighting happens in two layers. The lexer-based `SyntaxHighlighter` assigns colors to token types and runs on every keystroke. An `Annotator` adds semantic highlighting by inspecting the PSI tree after parsing.

For the lexer layer, create a `SyntaxHighlighter` subclass that maps each token type to a `TextAttributesKey`. Grammar-Kit defines 16 attribute keys for its BNF language, each based on a standard platform default so users get reasonable colors without configuration:

| Attribute Key | Based On | Highlights |
|---|---|---|
| `COMMENT` | `LINE_COMMENT` | Comments |
| `STRING` | `STRING` | String literals |
| `KEYWORD` | `MARKUP_ATTRIBUTE` | Keywords and modifiers |
| `RULE` | `KEYWORD` | Rule names |
| `TOKEN` | `STRING` | Explicit tokens |
| `EXTERNAL` | `STATIC_METHOD` | External references |
| `OP_SIGN` | `OPERATION_SIGN` | Operators |

For the annotator layer, implement `Annotator` (with `DumbAware` if your highlighting does not need indices). The annotator walks PSI elements and applies highlighting based on context. Grammar-Kit's `BnfAnnotator` distinguishes between regular rules and meta rules, explicit and implicit tokens, and attribute values versus patterns. It also produces a warning annotation for tokens matched by text rather than type, since text matching is slower at runtime.

!!! tip
    Provide a `ColorSettingsPage` so users can customize your language's colors in **Settings > Editor > Color Scheme**.

## Structure, Navigation, and Completion

The `StructureViewFactory` extension gives users an outline of the file. Grammar-Kit's structure view shows rules and attribute blocks as top-level entries, with individual attributes nested inside their blocks. Implement `StructureViewBuilder` and `TreeBasedStructureViewBuilder` to define what PSI elements appear and how they display.

For navigation, the `FindUsagesProvider` extension point enables "Find Usages" on your named elements. Grammar-Kit enables usage search on rules and attributes. The `DocumentationProvider` extension powers quick documentation (++ctrl+q++). Grammar-Kit shows computed FIRST and NEXT token sets for rules, and HTML descriptions for attributes.

Code completion uses `CompletionContributor`. Grammar-Kit registers three providers: one for attribute names inside `{...}` blocks, one for token and identifier references, and one for rule references. The contributor also integrates with parser-based keyword completion through `GeneratedParserUtilBase.CompletionState`, which suggests context-aware keywords based on what the parser expects at the caret position.

Register each feature in `plugin.xml`:

```xml
<lang.findUsagesProvider language="My"
    implementationClass="com.example.MyFindUsagesProvider"/>
<lang.documentationProvider language="My"
    implementationClass="com.example.MyDocumentationProvider"/>
<completion.contributor language="My"
    implementationClass="com.example.MyCompletionContributor"/>
<lang.structureViewExtension
    implementationClass="com.example.MyStructureViewFactory"/>
```

## Refactoring and Intentions

Grammar-Kit supports several refactoring operations through standard IntelliJ extension points. The `RefactoringSupportProvider` enables in-place rename for named elements. Three additional refactorings cover common grammar editing tasks:

- Inline Rule (uses the Inline refactoring shortcut) replaces a rule reference with the rule's body.
- Introduce Rule (uses the Extract Method shortcut) extracts a selected expression into a new rule.
- Introduce Token (uses the Introduce Constant shortcut) extracts a token literal into the tokens list.

Two intentions provide quick transforms directly from the editor:

- Flip Choice swaps the order of alternatives in a choice expression (`a | b` becomes `b | a`).
- Convert Optional Expression toggles between `expr?` and `[expr]` syntax.

Additional editor features include brace matching for `(){}[]<<>>`, line commenting with `//`, code folding for attribute blocks and comments, smart word selection, and moving choice branches left or right. These are each registered through their own extension points (`lang.braceMatcher`, `lang.commenter`, `lang.foldingBuilder`, and so on).

## Code Analysis

Grammar-Kit ships eight inspections that catch common grammar problems at warning level. All are enabled by default:

| Inspection | Detects |
|---|---|
| Unresolved reference | Missing rule, method, or pattern references |
| Unused rule | Rules not reachable from root or extra roots |
| Unused attribute | Attributes that have no effect |
| Suspicious token | A token that looks like a missing rule reference |
| Left recursion | Left recursion unsupported by the generator |
| Duplicate rule | Multiple rules with the same name |
| Identical choice branches | Duplicate alternatives in a choice |
| Unreachable choice branch | A branch masked by an earlier alternative |

Suppress individual inspections with a comment on the line above:

```
//noinspection BnfUnusedRule
unused_rule ::= something
```

When building inspections for your own language, extend `LocalInspectionTool` and register each inspection as an `<localInspection>` in `plugin.xml`. You can provide quick fixes by attaching `IntentionAction` instances to the problems you report. For further details on testing these features, see [Testing](testing.md).
