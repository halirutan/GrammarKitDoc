# Quick Start Tutorial

This tutorial walks through building a complete language plugin for IntelliJ IDEA using Grammar-Kit. You write a grammar for a simple calculator language, generate parser and lexer code, wire up the plugin classes, and verify that everything works. The result is a working plugin that parses `.calc` files with syntax highlighting and error recovery.

Before starting, [install Grammar-Kit](installation.md) and set up an IntelliJ plugin development project. This tutorial assumes you are comfortable with Java development and have a basic understanding of [what Grammar-Kit does](index.md).

## Your First Grammar

Create a file called `Calc.bnf` in your project with the following grammar:

```bnf
// Calc.bnf — A simple calculator language.
// Supports: numbers, +, -, *, /, parentheses, semicolons.
{
  // --- Package and class names for code generation ---
  parserClass="com.example.calc.parser.CalcParser"
  elementTypeHolderClass="com.example.calc.psi.CalcTypes"
  psiPackage="com.example.calc.psi"
  psiImplPackage="com.example.calc.psi.impl"
  psiVisitorName="CalcVisitor"

  // --- Token definitions ---
  tokens=[
    SEMI=';'
    PLUS='+'
    MINUS='-'
    MULT='*'
    DIV='/'
    LP='('
    RP=')'

    space='regexp:\s+'
    comment='regexp://.*'
    number='regexp:\d+(\.\d*)?'
  ]
}

// --- Rules ---
root ::= statement *
private statement ::= expr ';' {pin=1 recoverWhile=statement_recover}
private statement_recover ::= !(number | '(' | ';')

expr ::= add_expr
add_expr ::= mul_expr (('+'|'-') mul_expr) *
mul_expr ::= primary_expr (('*'|'/') primary_expr) *
primary_expr ::= number | paren_expr
paren_expr ::= '(' expr ')' {pin=1}
```

A `.bnf` file has two sections: a header attributes block in curly braces, followed by the grammar rules. The header controls code generation and defines tokens. The rules describe the language structure.

The header attributes tell Grammar-Kit where to put the generated code:

| Attribute | Value | Purpose |
|---|---|---|
| `parserClass` | `com.example.calc.parser.CalcParser` | Generated parser class |
| `elementTypeHolderClass` | `com.example.calc.psi.CalcTypes` | Token and element type constants |
| `psiPackage` | `com.example.calc.psi` | PSI interface package |
| `psiImplPackage` | `com.example.calc.psi.impl` | PSI implementation package |
| `psiVisitorName` | `CalcVisitor` | Generated visitor class name |

Always set these attributes explicitly. Without them, Grammar-Kit generates code into a `generated` package with default names, which makes the output harder to find and organize.

The `tokens` block defines the lexical elements of the language. Simple tokens like `SEMI=';'` match exact characters. Regexp tokens like `number='regexp:\d+(\.\d*)?'` use the `regexp:` prefix and match patterns. The `space` and `comment` regexp tokens are special: because no grammar rule references them, Grammar-Kit's Live Preview auto-detects them as whitespace and comments.

| Token | Definition | Purpose |
|---|---|---|
| `SEMI=';'` | Simple token | Exact character match |
| `number='regexp:\d+(\.\d*)?'` | Regexp token | Matches `42`, `3.14`, `100.` |
| `space='regexp:\s+'` | Regexp token | Auto-whitespace in Live Preview |
| `comment='regexp://.*'` | Regexp token | Auto-comment in Live Preview |

The rules section defines how tokens combine into language constructs. The basic syntax elements are:

- Sequence: `rule ::= part1 part2 part3` matches parts in order
- Choice: `rule ::= part1 | part2 | part3` matches any alternative
- Optional: `[optional_part]` or `optional_part?`
- Repetition: `part *` (zero or more) or `part +` (one or more)
- Grouping: `(group_a | group_b) rest`

Rules reference other rules by name (like `mul_expr` in the `add_expr` rule) and tokens by their quoted value (like `'+'`) or their name (like `SEMI`). The `private` modifier on a rule means it does not create its own PSI node; instead, its children are included directly in the parent node.

The `pin` and `recoverWhile` attributes on the `statement` rule enable error recovery. When `pin=1` is set, the parser commits to the rule after matching the first element. If subsequent elements fail, the parser reports an error but does not abandon the rule entirely. The `recoverWhile` attribute tells the parser to skip unexpected tokens until it sees something that could start a new statement (a number, `(`, or `;`). These attributes are covered in depth in [Error Recovery](grammar-development/error-recovery.md).

This grammar uses traditional precedence layers (`add_expr` calls `mul_expr`, which calls `primary_expr`) rather than Grammar-Kit's `left`/`extends` expression parsing idiom. That approach is more concise for complex expression languages and is covered in [Expression Parsing](grammar-development/expression-parsing.md).

### Testing with Live Preview

Live Preview lets you test the grammar against sample input without generating any code. Open `Calc.bnf` in the editor and press Ctrl+Alt+P (Cmd+Alt+P on macOS). A split editor opens with the grammar on one side and a preview pane on the other. Type an expression like `1 + 2;` in the preview pane, and Grammar-Kit parses it in real time using the grammar rules.

Two additional tools help during prototyping. The structure view (Ctrl+F12 / Cmd+F12) shows the PSI tree for the preview input. Grammar highlighting at caret (Ctrl+Alt+F7 / Cmd+Alt+F7 in the preview editor) highlights the grammar rules that match the current caret position in the preview.

Live Preview uses a simplified tokenizer built from the `regexp` tokens in the header block. This is sufficient for prototyping, but it does not match the behavior of a real JFlex lexer. Once your grammar stabilizes, switch to a generated JFlex lexer for accurate tokenization.

## Generating Parser Code

With the grammar tested in Live Preview, generate the parser and PSI classes:

1. Open `Calc.bnf` in the editor.
2. Press Ctrl+Shift+G (Cmd+Shift+G on macOS), or right-click the file and select **Generate Parser Code**.
3. A notification confirms success: `"Calc.bnf generated (size)"` with the output directory.

The generated files appear in the `gen/` directory (configurable via the `grammar.kit.gen.dir` system property):

```
gen/
  com/example/calc/
    parser/
      CalcParser.java            ← Parser (static parse methods)
    psi/
      CalcTypes.java             ← IElementType constants
      CalcVisitor.java           ← PSI visitor
      CalcExpr.java              ← PSI interface (from expr rule)
      CalcAddExpr.java           ← PSI interface (from add_expr rule)
      CalcMulExpr.java           ← PSI interface (from mul_expr rule)
      CalcPrimaryExpr.java       ← PSI interface (from primary_expr rule)
      CalcParenExpr.java         ← PSI interface (from paren_expr rule)
      impl/
        CalcExprImpl.java        ← PSI implementation
        CalcAddExprImpl.java     ← PSI implementation
        CalcMulExprImpl.java     ← PSI implementation
        CalcPrimaryExprImpl.java ← PSI implementation
        CalcParenExprImpl.java   ← PSI implementation
```

Grammar-Kit generates one PSI interface and one implementation class for each public rule. Private rules like `statement` and `statement_recover` produce no PSI classes.

`CalcTypes.java` contains the element type and token type constants that the parser, lexer, and `ParserDefinition` all reference:

```java
// Generated by Grammar-Kit — do not edit.
package com.example.calc.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.example.calc.psi.impl.*;

public interface CalcTypes {
  // Element types (one per public rule)
  IElementType ADD_EXPR = new CalcElementType("ADD_EXPR");
  IElementType EXPR = new CalcElementType("EXPR");
  IElementType MUL_EXPR = new CalcElementType("MUL_EXPR");
  IElementType PAREN_EXPR = new CalcElementType("PAREN_EXPR");
  IElementType PRIMARY_EXPR = new CalcElementType("PRIMARY_EXPR");

  // Token types (one per named token)
  IElementType DIV = new CalcTokenType("DIV");
  IElementType LP = new CalcTokenType("LP");
  IElementType MINUS = new CalcTokenType("MINUS");
  IElementType MULT = new CalcTokenType("MULT");
  IElementType NUMBER = new CalcTokenType("NUMBER");
  IElementType PLUS = new CalcTokenType("PLUS");
  IElementType RP = new CalcTokenType("RP");
  IElementType SEMI = new CalcTokenType("SEMI");

  // Factory method (creates PSI elements from AST nodes)
  // ...
}
```

`CalcParser.java` contains a static method for each grammar rule. Each method takes a `PsiBuilder` (the token stream interface) and an `int` recursion level (a guard against infinite recursion). Sub-expressions within a rule get suffixed names like `add_expr_0`. Avoid naming your own rules with this pattern (such as `expr_0`) because it conflicts with the generated names.

```java
// Generated by Grammar-Kit — do not edit.
package com.example.calc.parser;

import com.intellij.lang.PsiBuilder;
import com.intellij.lang.PsiParser;
// ...

public class CalcParser implements PsiParser {
  // One static method per rule:
  // static boolean root(PsiBuilder b, int l) { ... }
  // static boolean expr(PsiBuilder b, int l) { ... }
  // static boolean add_expr(PsiBuilder b, int l) { ... }
  // static boolean mul_expr(PsiBuilder b, int l) { ... }
  // static boolean primary_expr(PsiBuilder b, int l) { ... }
  // static boolean paren_expr(PsiBuilder b, int l) { ... }
  //
  // Sub-expressions get suffixed names:
  // static boolean add_expr_0(PsiBuilder b, int l) { ... }
}
```

The generated PSI interfaces, implementations, and visitor class are covered in detail in the PSI customization section. For this tutorial, the defaults work without modification.

!!! note
    Mark the `gen/` directory as a Generated Sources Root in IntelliJ IDEA so the generated code compiles alongside your source code.

## Creating a Language Plugin

The generated parser and PSI classes need a set of plugin classes to connect them to the IntelliJ Platform: a lexer, language and file type definitions, a parser definition, syntax highlighting, and `plugin.xml` registrations.

### Generating the Lexer

Grammar-Kit generates a JFlex lexer definition from the token block in your grammar:

1. Right-click `Calc.bnf` and select **Generate JFlex Lexer**. This creates `_CalcLexer.flex`.
2. Right-click `_CalcLexer.flex` and select **Run JFlex Generator**. This creates `_CalcLexer.java`. (JFlex 1.9.2 is downloaded automatically if needed.)

The generated `.flex` file converts the `regexp:` token definitions from Java regex syntax to JFlex syntax (for example, `\d` becomes `[0-9]` and `\s` becomes `[ \t\n\x0B\f\r]`). It implements the `FlexLexer` interface and returns `IElementType` constants from `CalcTypes`:

```flex
package com.example.calc.parser;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;

import static com.intellij.psi.TokenType.BAD_CHARACTER;
import static com.intellij.psi.TokenType.WHITE_SPACE;
import static com.example.calc.psi.CalcTypes.*;

%%

%{
  public _CalcLexer() {
    this((java.io.Reader)null);
  }
%}

%public
%class _CalcLexer
%implements FlexLexer
%function advance
%type IElementType
%unicode

EOL=\R
WHITE_SPACE=\s+

NUMBER=[0-9]+(\.[0-9]*)?
COMMENT=//.*

%%
<YYINITIAL> {
  {WHITE_SPACE}    { return WHITE_SPACE; }

  ";"              { return SEMI; }
  "+"              { return PLUS; }
  "-"              { return MINUS; }
  "*"              { return MULT; }
  "/"              { return DIV; }
  "("              { return LP; }
  ")"              { return RP; }

  {NUMBER}         { return NUMBER; }
  {COMMENT}        { return COMMENT; }

}

[^] { return BAD_CHARACTER; }
```

The `BAD_CHARACTER` fallback at the end handles any input the lexer does not recognize. You can edit the `.flex` file manually for more complex lexing requirements.

### Plugin Classes

The Calc plugin requires six hand-written Java classes. Each one is short and follows a standard pattern.

`CalcLanguage.java` defines the language singleton. The `"Calc"` string is the language ID, referenced by all other registrations:

```java
package com.example.calc;

import com.intellij.lang.Language;

public class CalcLanguage extends Language {

    public static final CalcLanguage INSTANCE = new CalcLanguage();

    private CalcLanguage() {
        super("Calc");
    }
}
```

`CalcFileType.java` maps the `.calc` file extension to the Calc language:

```java
package com.example.calc;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public class CalcFileType extends LanguageFileType {

    public static final CalcFileType INSTANCE = new CalcFileType();

    private CalcFileType() {
        super(CalcLanguage.INSTANCE);
    }

    @Override
    public @NotNull String getName() {
        return "Calc";
    }

    @Override
    public @NotNull String getDescription() {
        return "Calc language file";
    }

    @Override
    public @NotNull String getDefaultExtension() {
        return "calc";
    }

    @Override
    public Icon getIcon() {
        return null; // Add a 16x16 icon later
    }
}
```

`CalcFile.java` connects the language and file type through a `PsiFileBase` subclass:

```java
package com.example.calc;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import org.jetbrains.annotations.NotNull;

public class CalcFile extends PsiFileBase {

    public CalcFile(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, CalcLanguage.INSTANCE);
    }

    @Override
    public @NotNull FileType getFileType() {
        return CalcFileType.INSTANCE;
    }
}
```

`CalcParserDefinition.java` is the central integration point. It tells the IntelliJ Platform how to create a lexer, parser, and PSI elements for Calc files:

```java
package com.example.calc;

import com.intellij.lang.ASTNode;
import com.intellij.lang.ParserDefinition;
import com.intellij.lang.PsiParser;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.project.Project;
import com.intellij.psi.FileViewProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IFileElementType;
import com.intellij.psi.tree.TokenSet;
import com.example.calc.parser.CalcParser;
import com.example.calc.parser._CalcLexer;
import com.example.calc.psi.CalcTypes;
import com.intellij.lexer.FlexAdapter;
import org.jetbrains.annotations.NotNull;

public class CalcParserDefinition implements ParserDefinition {

    public static final IFileElementType FILE =
        new IFileElementType("CALC_FILE", CalcLanguage.INSTANCE);

    @Override
    public @NotNull Lexer createLexer(Project project) {
        return new FlexAdapter(new _CalcLexer());
    }

    @Override
    public @NotNull PsiParser createParser(Project project) {
        return new CalcParser();
    }

    @Override
    public @NotNull IFileElementType getFileNodeType() {
        return FILE;
    }

    @Override
    public @NotNull TokenSet getWhitespaceTokens() {
        return TokenSet.WHITE_SPACE;
    }

    @Override
    public @NotNull TokenSet getCommentTokens() {
        return TokenSet.create(CalcTypes.COMMENT);
    }

    @Override
    public @NotNull TokenSet getStringLiteralElements() {
        return TokenSet.EMPTY;
    }

    @Override
    public @NotNull PsiElement createElement(ASTNode node) {
        return CalcTypes.Factory.createElement(node);
    }

    @Override
    public @NotNull PsiFile createFile(@NotNull FileViewProvider viewProvider) {
        return new CalcFile(viewProvider);
    }
}
```

The `createLexer()` method wraps the JFlex lexer in a `FlexAdapter` because JFlex generates a `FlexLexer`, not the `Lexer` type that the IntelliJ Platform expects. The `createElement()` method delegates to the generated factory in `CalcTypes`, which maps AST nodes to the correct PSI implementation classes.

`CalcSyntaxHighlighter.java` maps token types to editor colors using `TextAttributesKey` constants. Each key falls back to a standard color from `DefaultLanguageHighlighterColors`:

```java
package com.example.calc;

import com.intellij.lexer.FlexAdapter;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import com.example.calc.parser._CalcLexer;
import com.example.calc.psi.CalcTypes;
import org.jetbrains.annotations.NotNull;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;

public class CalcSyntaxHighlighter extends SyntaxHighlighterBase {

    public static final TextAttributesKey NUMBER =
        createTextAttributesKey("CALC_NUMBER",
            DefaultLanguageHighlighterColors.NUMBER);

    public static final TextAttributesKey COMMENT =
        createTextAttributesKey("CALC_COMMENT",
            DefaultLanguageHighlighterColors.LINE_COMMENT);

    public static final TextAttributesKey OPERATION =
        createTextAttributesKey("CALC_OPERATION",
            DefaultLanguageHighlighterColors.OPERATION_SIGN);

    public static final TextAttributesKey PARENTHESES =
        createTextAttributesKey("CALC_PARENTHESES",
            DefaultLanguageHighlighterColors.PARENTHESES);

    public static final TextAttributesKey BAD_CHAR =
        createTextAttributesKey("CALC_BAD_CHARACTER",
            DefaultLanguageHighlighterColors.INVALID_STRING_ESCAPE);

    @Override
    public @NotNull Lexer getHighlightingLexer() {
        return new FlexAdapter(new _CalcLexer());
    }

    @Override
    public TextAttributesKey @NotNull [] getTokenHighlights(IElementType type) {
        if (type.equals(CalcTypes.NUMBER)) {
            return pack(NUMBER);
        }
        if (type.equals(CalcTypes.COMMENT)) {
            return pack(COMMENT);
        }
        if (type.equals(CalcTypes.PLUS) || type.equals(CalcTypes.MINUS) ||
            type.equals(CalcTypes.MULT) || type.equals(CalcTypes.DIV)) {
            return pack(OPERATION);
        }
        if (type.equals(CalcTypes.LP) || type.equals(CalcTypes.RP)) {
            return pack(PARENTHESES);
        }
        if (type.equals(TokenType.BAD_CHARACTER)) {
            return pack(BAD_CHAR);
        }
        return TextAttributesKey.EMPTY_ARRAY;
    }
}
```

`CalcSyntaxHighlighterFactory.java` is a factory class required by the extension point:

```java
package com.example.calc;

import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.openapi.fileTypes.SyntaxHighlighterFactory;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;

public class CalcSyntaxHighlighterFactory extends SyntaxHighlighterFactory {

    @Override
    public @NotNull SyntaxHighlighter getSyntaxHighlighter(
            Project project, VirtualFile virtualFile) {
        return new CalcSyntaxHighlighter();
    }
}
```

### Registering in plugin.xml

Register the file type, parser definition, and syntax highlighter in your `plugin.xml`:

```xml
<idea-plugin>
    <id>com.example.calc</id>
    <name>Calc Language</name>
    <vendor>Example</vendor>
    <description>Support for the Calc expression language.</description>

    <depends>com.intellij.modules.lang</depends>

    <extensions defaultExtensionNs="com.intellij">
        <!-- File type: maps .calc files to the Calc language -->
        <fileType name="Calc"
                  implementationClass="com.example.calc.CalcFileType"
                  fieldName="INSTANCE"
                  extensions="calc"
                  language="Calc"/>

        <!-- Parser: connects grammar to the IDE -->
        <lang.parserDefinition
                  language="Calc"
                  implementationClass="com.example.calc.CalcParserDefinition"/>

        <!-- Syntax highlighting -->
        <lang.syntaxHighlighterFactory
                  language="Calc"
                  implementationClass="com.example.calc.CalcSyntaxHighlighterFactory"/>
    </extensions>
</idea-plugin>
```

Three registrations are required at minimum: `fileType`, `lang.parserDefinition`, and `lang.syntaxHighlighterFactory`. The `com.intellij.modules.lang` dependency is also required for language support features.

!!! warning
    The `language="Calc"` attribute in `plugin.xml` must match the string in the `CalcLanguage` constructor exactly. This comparison is case-sensitive: `"Calc"` and `"calc"` are different language IDs.

### Project Layout

The complete file layout includes both hand-written and generated files:

```
my-calc-plugin/
  src/
    com/example/calc/
      CalcLanguage.java              ← You write this
      CalcFileType.java              ← You write this
      CalcFile.java                  ← You write this
      CalcParserDefinition.java      ← You write this
      CalcSyntaxHighlighter.java     ← You write this
      CalcSyntaxHighlighterFactory.java ← You write this
      parser/
        _CalcLexer.flex              ← Generated, then hand-edited
        _CalcLexer.java              ← Generated from .flex by JFlex
  gen/
    com/example/calc/
      parser/
        CalcParser.java              ← Generated from .bnf
      psi/
        CalcTypes.java               ← Generated from .bnf
        CalcVisitor.java             ← Generated from .bnf
        CalcExpr.java                ← Generated from .bnf
        CalcAddExpr.java             ← Generated from .bnf
        CalcMulExpr.java             ← Generated from .bnf
        CalcPrimaryExpr.java         ← Generated from .bnf
        CalcParenExpr.java           ← Generated from .bnf
        impl/
          CalcExprImpl.java          ← Generated from .bnf
          CalcAddExprImpl.java       ← Generated from .bnf
          CalcMulExprImpl.java       ← Generated from .bnf
          CalcPrimaryExprImpl.java   ← Generated from .bnf
          CalcParenExprImpl.java     ← Generated from .bnf
  resources/
    META-INF/
      plugin.xml                     ← You write this
  grammars/
    Calc.bnf                         ← You write this
```

Both `src/` and `gen/` must be on the classpath for the project to compile.

## Testing Your Parser

Run the plugin using a standard IntelliJ plugin run configuration. In the sandbox IDE instance, create a file with a `.calc` extension and verify that syntax highlighting appears.

Try these sample inputs to exercise different parts of the grammar:

```
1 + 2;
3 * 4 + 5;
(10 - 3) * 2;
```

```
// Compute a result
(1 + 2) * (3 + 4);
100 / (5 - 3);
3.14 * 2;
```

To test error recovery, try input with a deliberate error:

```
1 + 2;
+ ;
3 * 4;
```

The second line (`+ ;`) has no left operand. The parser reports an error on that line but recovers at the semicolon and parses the third line successfully.

The PSI tree for a simple expression like `1 + 2;` looks like this:

```
CalcFile
  Expr(ADD_EXPR)
    Expr(PRIMARY_EXPR)
      PsiElement(number)('1')
    PsiElement(PLUS)('+')
    Expr(PRIMARY_EXPR)
      PsiElement(number)('2')
  PsiElement(SEMI)(';')
```

Public rules become PSI nodes in the tree. Private rules (like `statement`) are transparent and do not appear. Tokens appear as `PsiElement` leaves.

Open **Tools > View PSI Structure** to inspect the parse tree for any file in your project. This is useful for verifying that the grammar produces the expected structure. You can also use the structure view (Ctrl+F12 / Cmd+F12) for a quick tree outline.

For automated regression testing, extend `ParsingTestCase` from the IntelliJ test framework. This base class lets you provide input text and compare the resulting PSI tree against an expected dump file. See the [IntelliJ SDK Parsing Test documentation](https://plugins.jetbrains.com/docs/intellij/parsing-test.html) for setup details.

Grammar-Kit also provides built-in inspections in the BNF editor that catch common grammar problems: left recursion, unresolved references, unused rules, duplicate rules, suspicious tokens, and identical or unreachable choice branches. These inspections run as you edit the grammar and appear as warnings in the editor.

### Common Mistakes

Without `parserClass`, `elementTypeHolderClass`, `psiPackage`, and `psiImplPackage` in the header, the generated code lands in a `generated` package with generic names. Always set these attributes explicitly.

A recovery predicate like `!(number)` skips the entire file if the input has no numbers. Include all possible statement starters and delimiters in the predicate: `!(number | '(' | ';')`.

The generator creates methods like `expr_0` for sub-expressions of `expr`. If you name your own rule `expr_0`, it conflicts with the generated name. Use descriptive names like `primary_expr` or `literal` instead.

JFlex generates a `FlexLexer`, not a `Lexer`. Wrap it with `new FlexAdapter(new _CalcLexer())` in `createLexer()`. Similarly, the string in `CalcLanguage`'s constructor (`"Calc"`) must match `language="Calc"` in `plugin.xml` exactly, including case.

### Workflow Summary

The full sequence from grammar to working plugin:

1. Create `Calc.bnf` with tokens and rules.
2. Open Live Preview (Ctrl+Alt+P) to test the grammar interactively.
3. Generate parser code (Ctrl+Shift+G).
4. Generate the JFlex lexer (right-click `.bnf` > **Generate JFlex Lexer**), then generate the Java lexer (right-click `.flex` > **Run JFlex Generator**).
5. Write `CalcLanguage`, `CalcFileType`, `CalcFile`, and `CalcParserDefinition`.
6. Write `CalcSyntaxHighlighter` and `CalcSyntaxHighlighterFactory`.
7. Register everything in `plugin.xml`.
8. Run the plugin and open a `.calc` file.

The recommended long-term workflow is: prototype the grammar in Live Preview, generate the initial `.flex` file and Java lexer, create the `ParserDefinition` and set up tests, then perfect the `.flex` and `.bnf` separately in the production environment.

For next steps, see [BNF Grammar Syntax](grammar-development/grammar-syntax.md) for the full syntax reference, [Expression Parsing](grammar-development/expression-parsing.md) for the `left`/`extends` idiom, [Error Recovery](grammar-development/error-recovery.md) for advanced `pin` and `recoverWhile` patterns, or [Gradle Integration](integration/gradle-setup.md) for build automation.
