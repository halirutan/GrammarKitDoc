# Section 2.5: Live Preview Workflow -- Topic Summary

## Purpose

Explain how to use Live Preview as a rapid feedback tool during grammar development. Cover the mechanics of the preview lexer and parser, the IDE tools available, and the boundaries of what Live Preview can and cannot do compared to a generated parser.

## Audience

IntelliJ plugin developers building a new grammar or iterating on an existing one. Assumes familiarity with BNF grammar basics (covered in Section 2.1) and error recovery concepts (Section 2.4).

## Page Structure

### H1: Live Preview Workflow

Opening paragraph: What Live Preview does and where it fits in the development cycle. Keep it concrete. Reference the recommended workflow (prototype in Live Preview, then generate flex/parser).

### H2: Opening and Using Live Preview

How to open it (Ctrl-Alt-P / Cmd-Alt-P), what happens (split editor, .bnf.preview file), how the auto-reparse works (500ms delay). Mention DumbAware (works during indexing). Cover the keyboard shortcuts table.

### H2: How the Preview Lexer Works

Token construction from the grammar's `tokens` block. Explain the key behaviors: longest-match algorithm, whitespace auto-detection (unused regexp tokens), keyword detection (Java identifiers), and the heuristic type guessing (number, string, comment). Include the token type detection table.

### H2: IDE Tools for Live Preview

Structure view, File Structure popup, PSI Viewer, grammar-at-caret highlighting (Ctrl-Alt-F7 / Cmd-Alt-F7). Explain matched vs. unmatched highlighting. Keep this practical.

### H2: Limitations

What the preview parser does NOT support: external rules referencing static methods, JFlex-specific lexer features, complex regex conversions. Only `eof` and `anything` are supported as external expressions. Explain when to switch from Live Preview to a generated parser with a real lexer.

## Key Evidence to Include

- Keyboard shortcuts: Ctrl-Alt-P (open), Ctrl-Alt-F7 (grammar highlighting)
- Auto-reparse: 500ms MergingUpdateQueue
- Token type heuristics table (whitespace, number, string, comment, keyword)
- Whitespace rule: unused regexp tokens matching space/newline become whitespace
- Supported parser features: pin, recoverWhile, extends, hooks, expression parsing
- Not supported: external static methods, JFlex features
- Hard-coded externals: `eof`, `anything`
- Brace pairs auto-created for {}()[]<>

## Examples to Include

- JSON grammar (Example 1) as the primary walkthrough example
- Tutorial grammar (Example 2) for expression parsing
- Auto-recovery grammar (Example 3) for #auto recovery
- Workflow steps from examples.md

## Cross-References

- Section 2.1 (Grammar Syntax) for token definitions
- Section 2.4 (Error Recovery) for pin and recoverWhile
- Section 2.3 (Expression Parsing) for left rules
- Section 2.6 (External Rules) for external rule limitations
- Section 1.4 (Quick Start) for the recommended workflow overview
