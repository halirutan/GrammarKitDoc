# Section 6.3: Keyboard Shortcuts — Code Evidence

## 1. Registered Actions with Shortcuts

**Source: `resources/META-INF/plugin.xml:111-133`**

### Grammar-Kit Specific Actions

| Action ID | Class | Shortcut (default) | Description |
|---|---|---|---|
| `grammar.LivePreview` | `LivePreviewAction` | **Ctrl-Alt-P** | Open Live Preview |
| `grammar.HighlightGrammarAtCaretAction` | `HighlightGrammarAtCaretAction` | **Ctrl-Alt-F7** | Toggle grammar-at-caret highlighting |
| `grammars.IntroduceRule` | `BnfIntroduceRuleAction` | Uses **ExtractMethod** shortcut | Extract/introduce rule |
| `grammars.IntroduceToken` | `BnfIntroduceTokenAction` | Uses **IntroduceConstant** shortcut | Extract/introduce token |

### Standard IntelliJ Shortcuts Used by Grammar-Kit

**Source: `README.md:38-40, 63-72`**

| Action | Windows/Linux | macOS | Description |
|---|---|---|---|
| Generate Parser | **Ctrl-Shift-G** | **Cmd-Shift-G** | Generate parser code |
| Live Preview | **Ctrl-Alt-P** | **Cmd-Alt-P** | Open Live Preview |
| Grammar Highlighting | **Ctrl-Alt-F7** | **Cmd-Alt-F7** | Toggle grammar-at-caret |
| File Structure | **Ctrl-F12** | **Cmd-F12** | File structure popup |
| Quick Documentation | **Ctrl-Q** | **Cmd-J** | Show FIRST/NEXT sets |
| Introduce Rule | **Ctrl-Alt-M** | **Cmd-Alt-M** | Extract rule (ExtractMethod) |
| Introduce Token | **Ctrl-Alt-C** | **Cmd-Alt-C** | Extract token (IntroduceConstant) |
| Inline Rule | **Ctrl-Alt-N** | **Cmd-Alt-N** | Inline rule refactoring |

## 2. Action Groups

**Source: `plugin.xml:112-133`**

- `grammar.file.group` — Main group added to: Tools menu, Editor popup, Project view popup
- `grammar.RefactoringGroup` — Added to: IntroduceActionsGroup (first position)

## 3. Context Menu Actions

**Source: `README.md:39-41`**

Context menu provides:
- Generate JFlex Lexer — from `.bnf` file context menu
- Run JFlex Generator — from `.flex` file context menu
- Generate Parser Util Class — creates parser utility class template
