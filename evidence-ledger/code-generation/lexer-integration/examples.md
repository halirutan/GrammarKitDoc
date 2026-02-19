# Section 3.3: Lexer Integration — Examples

## Example 1: Token Definitions in Grammar

**Source: `testData/generator/ExprParser.bnf:11-19`**

```bnf
{
  tokens=[
    space='regexp:\s+'
    comment='regexp://.*'
    number='regexp:\d+(\.\d*)?'
    id='regexp:\p{Alpha}\w*'
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"
    syntax='regexp:;|\.|\+|-|\*\*|\*|==|=|/|,|\(|\)|\^|\!=|\!|>=|<=|>|<'
  ]
}
```

Token types:
- `space` — regexp token, auto-whitespace in Live Preview
- `comment` — regexp token, auto-comment detection
- `number`, `id`, `string` — regexp tokens with patterns
- `syntax` — catch-all syntax token (simple approach)

## Example 2: Generated JFlex Template Output

**Source: `resources/templates/lexer.flex.template`**

For a grammar with tokens `PLUS='+'`, `NUMBER='regexp:\d+'`, `ID='regexp:\w+'`:

```flex
package com.example.lang;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;

import static com.intellij.psi.TokenType.BAD_CHARACTER;
import static com.intellij.psi.TokenType.WHITE_SPACE;
import static com.example.lang.MyTypes.*;

%%

%{
  public _MyLangLexer() {
    this((java.io.Reader)null);
  }
%}

%public
%class _MyLangLexer
%implements FlexLexer
%function advance
%type IElementType
%unicode

EOL=\R
WHITE_SPACE=\s+

NUMBER=[0-9]+
ID=[a-zA-Z_0-9]+

%%
<YYINITIAL> {
  {WHITE_SPACE}    { return WHITE_SPACE; }

  "+"              { return PLUS; }

  {NUMBER}         { return NUMBER; }
  {ID}             { return ID; }
}

[^] { return BAD_CHARACTER; }
```

## Example 3: Java Regex to JFlex Conversion

**Source: `BnfGenerateLexerAction.java:218-256`**

| Java Pattern | JFlex Equivalent |
|---|---|
| `\d` | `[0-9]` |
| `\D` | `[^0-9]` |
| `\s` | `[ \t\n\x0B\f\r]` |
| `\w` | `[a-zA-Z_0-9]` |
| `\p{Alpha}` | `[:letter:]` |
| `\p{Digit}` | `[:digit:]` |
| `\p{Lower}` | `[:lowercase:]` |
| `\p{Upper}` | `[:uppercase:]` |
| `\p{Alnum}` | `([:letter:]\|[:digit:])` |
| `\p{ASCII}` | `[\x00-\x7F]` |

## Example 4: Token Type Configuration

**Source: `attributeDescriptions/tokenTypeClass.html`, `attributeDescriptions/tokenTypeFactory.html`**

```bnf
// Custom token type class (constructor-based)
{
  tokenTypeClass="org.intellij.grammar.psi.BnfTokenType"
}
// Generates: new BnfTokenType("TOKEN_NAME")

// Factory method (instead of constructor)
{
  tokenTypeFactory="com.sample.SampleElementFactory.getTokenType"
}
// Generates: SampleElementFactory.getTokenType("TOKEN_NAME")
```

## Example 5: JFlex File Structure (Grammar-Kit's Own Lexer)

The Grammar-Kit plugin itself parses JFlex files with a Grammar-Kit grammar (`grammars/JFlex.bnf`), providing:
- Syntax highlighting with customizable colors
- Code completion for `%directives`
- Find usages for state and macro definitions
- Refactoring (rename) support
- Structure view
- Brace matching
- Java code injection in action blocks

## Example 6: Token Types — Explicit vs Implicit

**Source: `README.md:176-185`**

```bnf
{
  tokens=[
    PLUS='+'        // Explicit: name and value defined
    NUMBER          // Implicit keyword: name equals value
  ]
}
rule ::= NUMBER '+' NUMBER    // '+' matched by PLUS (fast, by type)
rule2 ::= NUMBER "plus" NUMBER // "plus" matched by text (slow)
```

Text-matched tokens (quoted strings not in `tokens` list) span potentially multiple real lexer tokens and trigger the annotator warning: "Tokens matched by text are slower than tokens matched by types."
