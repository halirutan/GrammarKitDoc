# Section 2.5: Live Preview Workflow — Code Evidence

## 1. Action Registration and Keyboard Shortcuts

**Source: `resources/META-INF/plugin.xml:114-125`**

Live Preview is registered as action `grammar.LivePreview`:

```xml
<action id="grammar.LivePreview" class="org.intellij.grammar.actions.LivePreviewAction">
  <keyboard-shortcut keymap="$default" first-keystroke="control alt P"/>
</action>
```

Grammar-at-caret highlighting is registered as `grammar.HighlightGrammarAtCaretAction`:

```xml
<action id="grammar.HighlightGrammarAtCaretAction"
        class="org.intellij.grammar.actions.HighlightGrammarAtCaretAction">
  <add-to-group group-id="EditorPopupMenu" anchor="last"/>
  <keyboard-shortcut keymap="$default" first-keystroke="control alt F7"/>
</action>
```

Both actions are accessible from:
- Tools menu (via `grammar.file.group`)
- Editor popup menu
- Project view popup menu

**Keyboard shortcuts (from `README.md:38,71-72`):**

| Action | Windows/Linux | macOS |
|---|---|---|
| Open Live Preview | Ctrl-Alt-P | Cmd-Alt-P |
| Start/Stop Grammar Highlighting | Ctrl-Alt-F7 | Cmd-Alt-F7 |

## 2. LivePreviewAction Implementation

**Source: `src/org/intellij/grammar/actions/LivePreviewAction.java:20-39`**

- Extends `DumbAwareAction` — works during indexing.
- Only enabled when the current file is a `BnfFile` (`.bnf` files only).
- Delegates to `LivePreviewHelper.getInstance().showFor(bnfFile)`.

## 3. LivePreviewHelper: Core Orchestrator

**Source: `src/org/intellij/grammar/livePreview/LivePreviewHelper.java:54-178`**

### Opening a Preview

`showFor(BnfFile)` method (lines 85-95):
1. Calls `parseFile(bnfFile, "")` to create a virtual file with the preview language.
2. The preview file is named `<grammar>.bnf.preview`.
3. Splits the editor window horizontally (`SwingConstants.HORIZONTAL`).
4. Opens the preview file in the new split pane.

### Auto-Reparse on Grammar Change

Constructor (lines 64-77):
- Uses a `MergingUpdateQueue` with 500ms delay.
- Listens to all document changes via `EditorFactory.getEventMulticaster()`.
- When a `.bnf` file changes, triggers `reparseAllLivePreviews(file, document)`.
- The reparse finds all open preview editors associated with the grammar and calls `FileContentUtilCore.reparseFiles(files)`.

### Language Registration

`getLanguageFor(BnfFile)` (lines 105-111):
- Checks for an existing `LivePreviewLanguage` instance for the file.
- If none exists, creates a new one via `LivePreviewLanguage.newInstance()`.
- Registers `StructureViewBuilder` and `ParserDefinition` extensions for the language.

### Grammar-at-Caret Expression Collection

`collectExpressionsAtOffset()` (lines 143-178):
- Creates a `LivePreviewLexer` and `LivePreviewParser` for the grammar.
- Overrides `generateNodeCall()` to track which BNF expressions match at the caret offset.
- Reports each `BnfExpression` with a boolean indicating match success.
- Throws `ProcessCanceledException` when the processor returns false (to stop early).

## 4. LivePreviewLanguage: Dynamic Language Instance

**Source: `src/org/intellij/grammar/livePreview/LivePreviewLanguage.java:42-187`**

- Extends `Language` and implements `DependentLanguage`.
- Base instance registered with ID `"BNF_LP"` (line 46).
- Each grammar gets a unique language instance, created dynamically via ASM bytecode generation (lines 143-183).
- `MyClassLoader` generates unique subclasses using ASM `ClassWriter` — each class is named `LivePreviewLanguage$$_N` (N is an atomic counter).
- Display name is `"'<filename>.bnf' grammar"` (line 72).
- Uses `VirtualFilePointer` to track the grammar file (or a direct `SoftReference` in test mode).
- `findInstance(PsiFile)` iterates all registered languages to find one matching the grammar file's `VirtualFile`.
- `getPreviewEditors(Project)` / `getGrammarEditors(Project)` find open editors of the respective types.

## 5. LivePreviewLexer: Pattern-Based Tokenization

**Source: `src/org/intellij/grammar/livePreview/LivePreviewLexer.java:31-223`**

### Token Construction (lines 42-58)
- Reads token definitions from the BnfFile via `collectTokenPattern2Name()`.
- Creates `Token` instances, cached via `CachedValuesManager`.
- Each token stores: constant name, compiled `Pattern`, and `IElementType`.

### Token Classification (Token constructor, lines 162-188)
- **Regexp tokens** (`regexp:...`): Compiled directly as Java regex.
- **Simple tokens**: Text is escaped to a regex pattern.
- **Keyword detection**: If the token text is a valid Java identifier (`StringUtil.isJavaIdentifier()`), it is classified as a `KeywordType`.

### Token Type Guessing (`guessDelegateType`, lines 200-218)
Heuristic logic for automatic syntax highlighting:
- Matches `" "` or `"\n"` → `TokenType.WHITE_SPACE` (only if not used in grammar rules)
- Matches `"1234"` → `NUMBER`
- Matches `"\"sdf\""` or `"'sdf'"` → `STRING`
- Name ends with "comment" (case-insensitive) and not used in grammar → `COMMENT`

### Whitespace Handling (from `TUTORIAL.md:79-80`)
> The LivePreviewLexer treats as whitespace any space or new-line matching regexp token that is not used anywhere in the rules.

This is the key insight: a `regexp:\s+` token named `space` that doesn't appear in any rule body is automatically treated as whitespace.

### Lexer Algorithm (lines 77-108)
- Uses `Matcher.lookingAt()` for each token pattern at the current position.
- The **longest match** wins (greedy matching).
- Unmatched characters produce `TokenType.BAD_CHARACTER`.
- Stateless (state is always 0).

## 6. LivePreviewParser: Interpreter-Based Parsing

**Source: `src/org/intellij/grammar/livePreview/LivePreviewParser.java:35-668`**

### Initialization (lines 87-119)
- Obtains the grammar root rule (first rule in file).
- Creates `GenOptions` from the grammar file attributes.
- Builds `RuleGraphHelper`, `ExpressionHelper`, and `BnfFirstNextAnalyzer`.
- Collects `RuleType` element types and `TokenType` element types.
- Sets up recursion detection via `BitSet` arrays (one per input offset position).

### Recursion Detection (lines 121-132)
- For each rule call at a given offset, sets a bit in the bitset.
- If the bit is already set, reports "Endless recursion detected for '<rule>'" and returns false.

### Expression Parsing (lines 134-312)
Implements the full Grammar-Kit parsing logic interpretively:
- Handles all BNF expression types: `BNF_CHOICE`, `BNF_SEQUENCE`, `BNF_OP_OPT`, `BNF_OP_ZEROMORE`, `BNF_OP_ONEMORE`, `BNF_OP_AND`, `BNF_OP_NOT`.
- Supports `pin`, `recoverWhile` (including `#auto`), `hooks`, and `extends` (via `type_extends_`).
- Supports left rules (with `_LEFT_`, `_LEFT_INNER_`, `_UPPER_` modifiers).
- Supports expression parsing (Pratt-style) via `generateExpressionRoot()`.

### External Rule Support (lines 424-512)
- Meta rules with arguments are fully supported.
- Hard-coded external expressions: `eof` (check end-of-file) and `anything` (skip tokens).
- External rules referencing static methods in `parserUtilClass` are **not supported** in Live Preview — returns false (lines 346-350).
- This is documented: `"// not supported"`.

### Auto-Recovery (lines 647-667)
- For `recoverWhile="#auto"`, calculates FIRST/NEXT tokens using `BnfFirstNextAnalyzer`.
- Generates a predicate that checks `!nextTokenIsFast(builder, nextTokens)`.

### Brace Pairs (lines 66-71)
Automatically tries to create brace pairs for `{}`, `()`, `[]`, `<>` if matching tokens exist.

## 7. LivePreviewParserDefinition: Predefined Token Categories

**Source: `src/org/intellij/grammar/livePreview/LivePreviewParserDefinition.java:27-94`**

Defines base IElementType constants:
- `COMMENT` — for comments
- `STRING` — for string literals
- `NUMBER` — for numbers
- `KEYWORD` — for keywords (Java identifiers used as tokens)

Token sets:
- Whitespace: `TokenSet.WHITE_SPACE`
- Comments: `TokenSet.create(COMMENT)`
- String literals: `TokenSet.create(STRING)`

PSI elements are `ASTWrapperPsiElement` instances. Files are `PsiFileBase` with `LivePreviewFileType`.

## 8. LivePreviewStructureViewFactory: PSI Tree Display

**Source: `src/org/intellij/grammar/livePreview/LivePreviewStructureViewFactory.java:40-153`**

- Provides a Structure View for preview files.
- Each PSI element shows: `ClassName: 'first 30 chars of text'` for rule types.
- Leaf elements show: `elementType: 'text'`.
- Error elements show: `PsiErrorElement: 'error description'`.
- Rule types display `BnfIcons.RULE` icon.
- Error elements are highlighted with `CodeInsightColors.ERRORS_ATTRIBUTES`.

## 9. LivePreviewSyntaxHighlighterFactory: Highlighting

**Source: `src/org/intellij/grammar/livePreview/LivePreviewSyntaxHighlighterFactory.java:26-56`**

Maps token types to highlighting colors:
| Token Type | Highlight Attribute |
|---|---|
| `COMMENT` | `DefaultLanguageHighlighterColors.LINE_COMMENT` |
| `STRING` | `DefaultLanguageHighlighterColors.STRING` |
| `NUMBER` | `DefaultLanguageHighlighterColors.NUMBER` |
| `KEYWORD` | `DefaultLanguageHighlighterColors.KEYWORD` |
| `BAD_CHARACTER` | `DefaultLanguageHighlighterColors.INVALID_STRING_ESCAPE` |

## 10. GrammarAtCaretPassFactory: Bidirectional Highlighting

**Source: `src/org/intellij/grammar/livePreview/GrammarAtCaretPassFactory.java:36-120`**

- Implements `TextEditorHighlightingPassFactory`.
- Only activates for `BnfFile` instances.
- When enabled (via `GRAMMAR_AT_CARET_KEY`), highlights grammar expressions in the BNF editor that correspond to the caret position in the preview editor.
- Uses two highlight styles:
  - **Matched expressions**: `EditorColors.SEARCH_RESULT_ATTRIBUTES`
  - **Unmatched expressions**: `EditorColors.WRITE_SEARCH_RESULT_ATTRIBUTES`

## 11. HighlightGrammarAtCaretAction: Toggle Control

**Source: `src/org/intellij/grammar/actions/HighlightGrammarAtCaretAction.java:27-63`**

- Toggles the `GRAMMAR_AT_CARET_KEY` on the preview editor.
- Only enabled when the current file is a Live Preview file.
- Action text changes to "Start" or "Stop" based on current state.
- Triggers `DaemonCodeAnalyzer.restart()` to refresh highlighting.

## 12. LiveHooksHelper: Hook Support in Preview

**Source: `src/org/intellij/grammar/livePreview/LiveHooksHelper.java:22-78`**

- Registers hooks from `GeneratedParserUtilBase.Hook` fields.
- Supports whitespace binder hooks: `GREEDY_LEFT_BINDER`, `GREEDY_RIGHT_BINDER`.
- Hooks are looked up by name from static fields using reflection.
- Hook params can reference `WhitespacesBinders` constants.
- Wraps hook execution in try/catch, reporting "hook crashed" as builder error on failure.

## 13. LivePreviewFileType

**Source: `src/org/intellij/grammar/livePreview/LivePreviewFileType.java:20-48`**

- File type name: `"BNF_LP"`
- Default extension: `"preview"`
- Uses `BnfIcons.FILE` icon.

## 14. Test Data Examples

### Json.bnf (`testData/livePreview/Json.bnf`)
Demonstrates hooks, extends, pin, and recovery in Live Preview:
```bnf
json ::= array | object  { hooks=[wsBinders="null, null"] }
value ::= string | number | json {name="value" hooks=[leftBinder="GREEDY_LEFT_BINDER"]}
array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1 extends=json}
```

### AutoRecovery.bnf (`testData/livePreview/AutoRecovery.bnf`)
Demonstrates `#auto` recovery in Live Preview:
```bnf
item ::= number {recoverWhile="#auto"}
```

### LivePreviewTutorial.bnf (`testData/livePreview/LivePreviewTutorial.bnf`)
Complete tutorial grammar with expression parsing, used in TUTORIAL.md.

### Case153.bnf — Expression parsing:
```bnf
expr ::= primary | add_group
plus_expr ::= expr '+' expr
```

## 15. Documented Limitations

**Source: `TUTORIAL.md:75-80`**

1. "Flex file shall be edited manually as it is likely to contain complex logic that is absent in `*.bnf`. This also implies that Live Preview is not useful at step 4 (perfecting flex & bnf in production environment) as it requires supporting 2 different lexers."

2. Live Preview uses Java regex patterns, while JFlex supports only a subset. Grammar-Kit attempts "some obvious conversions." (`README.md:240-241`)

3. External rules referencing static methods are **not supported** in Live Preview. The `LivePreviewParser.generateNodeCall()` returns false for external rules (see `LivePreviewParser.java:346-350`).

4. Only hard-coded external expressions `eof` and `anything` are supported.

## 16. Recommended Workflow

**Source: `TUTORIAL.md:68-73`**

1. Prototype the grammar in Live Preview
2. Generate initial `*.flex` to sources and generate a `*.java` lexer from it
3. Create `ParserDefinition` and/or setup lexer and parser tests
4. Perfect the `*.flex` & `*.bnf` separately in production environment

## 17. Live Preview IDE Integration

**Source: `TUTORIAL.md:47-48, README.md:63-64`**

Tools available during Live Preview:
- **Structure toolwindow** — shows PSI tree (`LivePreviewStructureViewFactory`)
- **File Structure popup** (Ctrl-F12/Cmd-F12)
- **PSI Viewer dialog** — observe PSI tree as grammar is modified
- **Grammar Highlighting** (Ctrl-Alt-F7/Cmd-Alt-F7) — highlights grammar expressions at caret in preview
- **Language injection** — the preview language can be injected into other files for testing
