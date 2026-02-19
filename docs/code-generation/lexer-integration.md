# Lexer Integration

The parser generator produces `IElementType` constants that a lexer must recognize and return. Grammar-Kit integrates with JFlex to generate a lexer from the token definitions in your grammar. The workflow has two steps: generate a `.flex` file from the grammar, then compile it with JFlex to produce the Java lexer class.

## Defining Tokens

Tokens are declared in the `tokens` attribute of the grammar header. Each entry maps a token name to either a literal value or a regular expression pattern:

```bnf
{
  tokens=[
    PLUS="+"
    MINUS="-"
    number='regexp:\d+(\.\d*)?'
    id='regexp:\p{Alpha}\w*'
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"
    comment='regexp://.*'
  ]
}
```

Token entries fall into three categories. **Explicit tokens with patterns** use the `regexp:` prefix and define a regular expression for matching (e.g., `number='regexp:\d+'`). **Explicit tokens with literal values** specify the exact text (e.g., `PLUS="+"`). Any unquoted name used in a rule that does not match a rule name is treated as an **implicit keyword token** where the name equals the value.

Quoted strings that appear in rules but are not declared in the `tokens` list are matched by text at runtime rather than by `IElementType`. This text-based matching is slower because the parser compares character sequences instead of object identity.

!!! tip
    Declare all tokens explicitly in the `tokens` attribute. This avoids text-based matching and gives the lexer generator complete information about your language's token set.

## Generating the Flex File

Open your `.bnf` file and select "Generate JFlex Lexer" from the context menu. Grammar-Kit creates a `.flex` file named `_<GrammarName>Lexer.flex` (with a leading underscore) in the same directory as the grammar file by default. A save dialog lets you choose a different location.

The generated file uses a Velocity template and produces a standard JFlex specification:

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
ID=[:letter:][a-zA-Z_0-9]*

%%
<YYINITIAL> {
  {WHITE_SPACE}    { return WHITE_SPACE; }

  "+"              { return PLUS; }
  "-"              { return MINUS; }

  {NUMBER}         { return NUMBER; }
  {ID}             { return ID; }
}

[^] { return BAD_CHARACTER; }
```

The generated lexer implements the `FlexLexer` interface, enables full Unicode support with `%unicode`, and imports token constants from the `elementTypeHolderClass`. Literal tokens become quoted string matches; regexp tokens become JFlex macro definitions and references. Unrecognized input returns `BAD_CHARACTER`.

Grammar-Kit converts Java regex syntax to JFlex syntax automatically. The most common conversions:

| Java pattern | JFlex equivalent |
|---|---|
| `\d` | `[0-9]` |
| `\w` | `[a-zA-Z_0-9]` |
| `\s` | `[ \t\n\x0B\f\r]` |
| `\p{Alpha}` | `[:letter:]` |
| `\p{Digit}` | `[:digit:]` |
| `\p{Lower}` | `[:lowercase:]` |
| `\p{Upper}` | `[:uppercase:]` |
| `\p{Alnum}` | `([:letter:]\|[:digit:])` |
| `\p{ASCII}` | `[\x00-\x7F]` |

!!! warning
    The generated flex file is a starting point. Complex lexing logic -- multi-line comments, string interpolation, lexer states -- must be added manually. Once you edit the flex file, re-generating it from the grammar overwrites your changes.

## Compiling the Lexer

Open the `.flex` file and select "Run JFlex Generator" from the context menu. Grammar-Kit downloads JFlex (version 1.9.2 from the JetBrains cache) if it is not already available, creates a global library named "JFlex & idea-flex.skeleton", and runs JFlex with the `idea-flex.skeleton` file. Output appears in the Messages tool window.

JFlex reads the `%class` directive and `package` statement from the flex file to determine the output class name and location. The generated Java file goes into the source directory matching the package.

You can customize how token type instances are created. By default, Grammar-Kit generates constructor calls using the class specified by `tokenTypeClass`:

```bnf
{
  tokenTypeClass="com.example.lang.MyTokenType"
}
// Generates: new MyTokenType("PLUS")
```

To use a factory method instead, set `tokenTypeFactory`:

```bnf
{
  tokenTypeFactory="com.example.lang.MyTypeFactory.getTokenType"
}
// Generates: MyTypeFactory.getTokenType("PLUS")
```

## JFlex IDE Support

Grammar-Kit provides full IDE support for `.flex` files, including syntax highlighting with customizable colors, code completion for `%directives`, find usages and rename refactoring for state and macro definitions, structure view, brace matching, and Java code injection in action blocks.

The JFlex file format is itself parsed by a Grammar-Kit grammar (`JFlex.bnf`), so editing flex files benefits from the same infrastructure that Grammar-Kit provides for BNF grammars.

!!! tip
    The flex file typically requires manual editing for features like multi-line comments, nested strings, or lexer states. Grammar-Kit's JFlex support makes this editing experience comparable to editing any other structured language file.

For Gradle-based lexer generation in CI/CD pipelines, see [Gradle Plugin Setup](../integration/gradle-setup.md). For details on token definition syntax in BNF grammars, see [BNF Grammar Syntax](../grammar-development/grammar-syntax.md).
