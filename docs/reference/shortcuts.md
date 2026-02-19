# Keyboard Shortcuts

This page lists the keyboard shortcuts available when working with Grammar-Kit in IntelliJ IDEA.

## Grammar-Kit Actions

These shortcuts are specific to Grammar-Kit and work when editing `.bnf` or `.flex` files.

| Action | Windows / Linux | macOS | Description |
|---|---|---|---|
| Generate Parser | ++ctrl+shift+g++ | ++cmd+shift+g++ | Generate parser and PSI code from the current grammar |
| Live Preview | ++ctrl+alt+p++ | ++cmd+alt+p++ | Open the [Live Preview](../grammar-development/live-preview.md) panel for the current grammar |
| Grammar Highlighting | ++ctrl+alt+f7++ | ++cmd+alt+f7++ | Toggle grammar-at-caret highlighting, which links the Live Preview cursor position to the matching grammar expression |

## Refactoring

Grammar-Kit registers refactoring actions that use standard IntelliJ shortcut mappings.

| Action | Windows / Linux | macOS | Description |
|---|---|---|---|
| Introduce Rule | ++ctrl+alt+m++ | ++cmd+alt+m++ | Extract the selected expression into a new rule (uses the Extract Method shortcut) |
| Introduce Token | ++ctrl+alt+c++ | ++cmd+alt+c++ | Extract the selected token into a named token constant (uses the Introduce Constant shortcut) |
| Inline Rule | ++ctrl+alt+n++ | ++cmd+alt+n++ | Inline a rule reference, replacing it with the rule's body |

## Navigation and Information

These are standard IntelliJ actions that Grammar-Kit enhances with grammar-specific behavior.

| Action | Windows / Linux | macOS | Description |
|---|---|---|---|
| File Structure | ++ctrl+f12++ | ++cmd+f12++ | Show the file structure popup with all rules in the current grammar |
| Quick Documentation | ++ctrl+q++ | ++cmd+j++ | Show documentation for the element at the caret, including FIRST and NEXT sets for rules |

## Context Menu Actions

These actions are available from the right-click context menu and the **Tools** menu. They do not have default keyboard shortcuts.

| Action | Availability | Description |
|---|---|---|
| Generate JFlex Lexer | Context menu on a `.bnf` file | Generates a `.flex` lexer specification from the grammar's token definitions |
| Run JFlex Generator | Context menu on a `.flex` file | Runs the JFlex generator to produce a Java lexer class |
| Generate Parser Util Class | Context menu / Tools menu | Creates a parser utility class template for custom parse methods |

All keyboard shortcuts follow the standard IntelliJ IDEA keymap. If you have customized your keymap, the actual keys may differ from the defaults listed here.
