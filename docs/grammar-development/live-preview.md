# Live Preview

Live Preview provides instant visual feedback as you develop your grammar, showing how Grammar-Kit parses your test input in real-time. This feature eliminates the generate-compile-test cycle during initial design.

## Opening Live Preview

To start Live Preview, place your cursor in a BNF file and use:

- **Windows/Linux**: `Ctrl+Alt+P`
- **macOS**: `Meta+Alt+P`

This action:

1. Creates a `.preview` file adjacent to your BNF file
2. Splits the editor horizontally
3. Shows your BNF grammar on top and the preview editor below
4. Opens the Structure view showing the parsed PSI tree

The preview updates automatically when you modify the BNF file, with a 500ms debounce to avoid excessive parsing during rapid edits.

## Understanding the Preview Interface

The bottom pane contains an editable text area where you enter sample input to test your grammar. As you type, Grammar-Kit parses the content and displays the resulting PSI structure in the Structure view. The Structure view (typically on the left side of the IDE) shows the parsed PSI tree for your preview content. This tree updates in real-time, allowing you to verify rule matching, check PSI node hierarchy, validate element boundaries, and debug parsing issues.

Use evaluator highlighting to debug specific rules:

- **Windows/Linux**: `Ctrl+Alt+F7`
- **macOS**: `Meta+Alt+F7`

With your cursor on a rule in the BNF file, this feature highlights all text in the preview that matches that rule. Green highlighting indicates successfully matched expressions, while red highlighting shows failed match attempts.

## Preview Token Recognition

Live Preview uses a simplified lexer that extracts tokens from your BNF file's tokens section. The preview lexer automatically categorizes tokens based on patterns:

| Token Type | Detection Pattern | Example |
|------------|------------------|---------|
| **String** | Quoted text patterns | `"keyword"` or `'literal'` |
| **Number** | Numeric patterns | `NUMBER='regexp:\d+'` |
| **Comment** | Tokens ending with "comment" | `LINE_COMMENT` or `BlockComment` |
| **Keyword** | Java identifier patterns | `IF` or `WHILE` |
| **Whitespace** | Space/newline patterns not used in rules | `WS='regexp:\s+'` |

When multiple tokens could match the same input, the preview lexer follows these rules:

1. Longer matches take precedence
2. Tokens defined earlier in the tokens section win ties
3. Explicitly quoted strings in rules create implicit tokens

The preview lexer automatically skips tokens that match only whitespace characters (space or newline) and are not referenced in any grammar rule.

## Preview Limitations

Live Preview provides rapid feedback but has important limitations compared to production parsers. The preview lexer uses basic regex matching only and cannot handle stateful lexing or JFlex advanced features. It may tokenize differently than your production lexer.

Preview cannot use external token types from JFlex files, access custom token definitions from Java code, or handle tokens defined outside the BNF file. While preview shows basic error recovery using `pin` and `recoverWhile` attributes, complex recovery strategies may behave differently in production.

Preview is optimized for small inputs. Large files may cause slower updates, IDE responsiveness issues, or incomplete parsing.

## Rapid Iteration Workflow

Live Preview enables an efficient grammar development workflow. Start with a simple grammar structure:

```bnf
{
  tokens = [
    NUMBER='regexp:\d+'
    ID='regexp:[a-zA-Z_]\w*'
    WS='regexp:\s+'
  ]
}

file ::= statement*
statement ::= assignment | expression
assignment ::= ID '=' expression
expression ::= NUMBER | ID
```

Enter test input in the preview:

```
x = 42
y = x
```

Verify the Structure view shows the expected PSI tree. Enhance your grammar step by step:

```bnf
expression ::= add_expr
add_expr ::= mult_expr ('+' mult_expr)*
mult_expr ::= primary ('*' primary)*
primary ::= NUMBER | ID | '(' expression ')'
```

Test each addition with appropriate input. Add error recovery attributes:

```bnf
statement ::= assignment | expression {recoverWhile=statement_recover}
assignment ::= ID '=' expression {pin=2}
private statement_recover ::= !(ID | NUMBER)
```

Test with broken input to verify recovery behavior. Once your grammar handles all test cases correctly in preview:

1. Generate the parser (`Ctrl+Shift+G` / `Cmd+Shift+G`)
2. Create a proper lexer (JFlex or manual)
3. Implement `ParserDefinition`
4. Test with production data

## Preview vs. Production Differences

Preview may split tokens differently. For example, `"string"` might be three tokens in preview (`"`, `string`, `"`) but a single `STRING_LITERAL` token in production. Preview's comment detection is pattern-based, while production lexers can handle nested comments, documentation comments, and comment-like content in strings.

Preview treats any identifier-like token as a potential keyword, while production lexers typically define specific keyword sets, handle context-sensitive keywords, and optimize keyword recognition.

## Best Practices

Structure your grammar to work well with preview:

```bnf
{
  tokens = [
    // Define tokens explicitly for preview
    PLUS='+'
    MINUS='-'
    STAR='*'
    SLASH='/'
    
    // Use clear patterns
    NUMBER='regexp:\d+(\.\d+)?'
    ID='regexp:[a-zA-Z_]\w*'
    STRING='regexp:"[^"]*"'
    
    // Name whitespace tokens conventionally
    WS='regexp:\s+'
  ]
}
```

Test edge cases including empty input, single token input, deeply nested structures, and error recovery scenarios. When a rule isn't matching as expected:

1. Place cursor on the rule
2. Press `Ctrl+Alt+F7` / `Meta+Alt+F7`
3. Check what text is highlighted
4. Adjust rule or input accordingly

Follow this development pattern: prototype in preview with simple tokens, validate structure and parsing behavior, generate parser when grammar stabilizes, then refine with production lexer and tests.

## Next Steps

After mastering Live Preview, learn about [Parser Generation](../code-generation/parser-generation.md) to create production parsers from your tested grammar.