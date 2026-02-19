# Live Preview Workflow

Live Preview lets you test a grammar against sample input without generating a parser or writing a lexer. You edit a `.bnf` file on one side, type test input on the other, and see the resulting parse tree update in real time. This makes it the fastest way to iterate on grammar rules during early development.

The recommended workflow is to prototype your grammar in Live Preview first, then generate the lexer and parser once the rules are stable. After that, you refine the `.flex` and `.bnf` files separately in a production environment with real tests.

## Opening and Using Live Preview

Press **Ctrl-Alt-P** (Windows/Linux) or **Cmd-Alt-P** (macOS) with a `.bnf` file open. Grammar-Kit splits the editor horizontally and opens a preview file named `<grammar>.bnf.preview` in the new pane. Type sample input in this preview pane to test your grammar.

| Action | Windows/Linux | macOS |
|---|---|---|
| Open Live Preview | Ctrl-Alt-P | Cmd-Alt-P |
| Start/Stop Grammar Highlighting | Ctrl-Alt-F7 | Cmd-Alt-F7 |

Both actions are also available from the **Tools** menu and the editor context menu.

When you edit the grammar, Live Preview reparses the preview input automatically after a 500ms delay. You do not need to regenerate anything. The action works during IDE indexing, so you can start testing immediately after opening a project.

## How the Preview Lexer Works

Live Preview builds its own lexer from the `tokens` block in your grammar. It does not use JFlex. Instead, it compiles each token definition into a Java regular expression and applies a longest-match algorithm: at each position in the input, the token whose pattern matches the most characters wins. Any characters that no token matches produce a `BAD_CHARACTER` error.

The lexer classifies tokens automatically using heuristics. You do not need to configure highlighting or whitespace handling for the preview to work.

| Token pattern | Detected type | Effect |
|---|---|---|
| Matches `" "` or `"\n"` and is unused in rules | Whitespace | Hidden, treated as whitespace |
| Matches `"1234"` | Number | Number highlighting |
| Matches `"\"sdf\""` or `"'sdf'"` | String | String highlighting |
| Name ends with "comment" (case-insensitive) | Comment | Comment highlighting |
| Text is a valid Java identifier | Keyword | Keyword highlighting |

The whitespace rule is the most important one to understand. A regexp token like `space='regexp:\s+'` that does not appear in any grammar rule is automatically treated as whitespace. If you reference that token in a rule, it stops being whitespace and becomes a regular token.

Here is a JSON grammar that works well in Live Preview:

```bnf
{
  tokens = [
    space='regexp:\s+'
    string = "regexp:\"[^\"]*\"|'[^']*'"
    number = "regexp:(\+|\-)?\p{Digit}*"
    id = "regexp:\p{Alpha}\w*"
    comma = ","
    colon = ":"
    brace1 = "{"
    brace2 = "}"
    brack1 = "["
    brack2 = "]"
  ]
  extends("array|object|json")=value
}

root ::= json
json ::= array | object  { hooks=[wsBinders="null, null"] }
value ::= string | number | json {name="value" hooks=[leftBinder="GREEDY_LEFT_BINDER"]}

array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1 extends=json}
private item ::= json {recoverWhile=recover}
object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1 extends=json}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}
name ::= id | string {name="name" hooks=[rightBinder="GREEDY_RIGHT_BINDER"]}
private recover ::= !(',' | ']' | '}' | '[' | '{')
```

The `space` token uses `regexp:\s+` and does not appear in any rule, so Live Preview treats it as whitespace automatically. The `id` token matches Java identifiers, so words like `true` or `null` get keyword highlighting. Comment tokens named with a "comment" suffix (like `comment='regexp://.*'`) are highlighted as comments.

## IDE Tools for Live Preview

Several IDE tools work with the preview file, giving you visibility into the parse tree and grammar behavior.

The **Structure** tool window and **File Structure** popup (Ctrl-F12 / Cmd-F12) display the PSI tree for the preview input. Each node shows its element type and a snippet of the matched text. Error nodes are marked so you can spot parsing failures at a glance. You can also open the **PSI Viewer** dialog for a more detailed view of the tree.

**Grammar-at-caret highlighting** connects the preview pane back to the grammar. Press **Ctrl-Alt-F7** (Windows/Linux) or **Cmd-Alt-F7** (macOS) while the preview editor is focused to toggle this feature. When active, Grammar-Kit highlights the BNF expressions in your grammar file that correspond to the caret position in the preview. Matched expressions use one highlight color and unmatched expressions use another, so you can see exactly which rules succeeded or failed at a given position.

Live Preview also automatically creates brace pairs for `{}`, `()`, `[]`, and `<>` if matching tokens exist in your grammar. This gives you basic brace matching in the preview pane without any configuration.

## Limitations

Live Preview interprets your grammar at runtime rather than generating compiled code. It supports most Grammar-Kit features, including `pin`, `recoverWhile`, `#auto` recovery, `extends`, hooks, and [expression parsing](expression-parsing.md) with left rules. However, there are boundaries you should know about.

**External rules do not work.** The preview parser cannot call static methods from your `parserUtilClass`. If a rule references an external method, the preview parser returns false for that rule. Only two built-in external expressions are supported: `eof` (checks for end-of-file) and `anything` (skips tokens). See [External Rules](external-rules.md) for more on this topic.

**The lexer uses Java regex, not JFlex.** Live Preview compiles your token patterns as Java regular expressions. JFlex supports features that Java regex does not, and Grammar-Kit attempts some obvious conversions, but complex JFlex patterns may not behave the same way. Once your grammar rules are stable, generate a `.flex` file and switch to testing with the real lexer.

**When to move past Live Preview.** Live Preview is designed for rapid prototyping. Once you need custom external rules, complex lexer states, or production-grade performance testing, generate the lexer and parser, create a `ParserDefinition`, and test against real files. The typical progression is:

1. Prototype grammar rules in Live Preview
2. Generate the `.flex` file and compile it to a `.java` lexer
3. Create a `ParserDefinition` and set up parser tests
4. Refine the `.flex` and `.bnf` separately with real test cases

This workflow lets you move fast early and get precise later. Live Preview is most valuable in steps 1 and 2, where the grammar is still changing frequently.
