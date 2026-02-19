# FAQ

## Grammar Development

### How do I handle left recursion?

Grammar-Kit does not support general left recursion. If you write a directly left-recursive rule, the "employs left-recursion unsupported by generator" inspection flags it. Use expression parsing instead: list operator variants as alternatives in a single `expr` rule and apply `extends(".*expr")=expr` to activate Pratt-style parsing.

```bnf
{
  extends(".*expr")=expr
}
expr ::= plus_expr | mul_expr | literal_expr
plus_expr ::= expr '+' expr
mul_expr ::= expr '*' expr
literal_expr ::= number
```

Grammar-Kit detects rules matching the `extends` pattern and generates a Pratt parser that handles left recursion internally. See [Expression Parsing](../grammar-development/expression-parsing.md) for the full approach.

### What is the difference between private and fake rules?

`private` rules participate in parsing but produce no PSI nodes. Their matched content merges into the parent node. Use `private` for intermediate grouping rules that organize the grammar but should not appear in the tree.

`fake` rules are the opposite: they generate PSI interfaces and classes but produce no parsing code. Use `fake` to define shared base types in your PSI hierarchy. Do not combine `private` and `fake` on the same rule.

```bnf
private item_list ::= item (',' item) *    // parsed, no PSI node
fake named_element ::= id                  // PSI class only, no parsing
```

For more on PSI hierarchy design, see [PSI Customization](../code-generation/psi-customization.md).

### Why does my token show "Tokens matched by text are slower"?

Quoted strings in rule bodies that do not correspond to a named token in the `tokens` block are matched by text comparison at runtime. This works but is slower than matching by `IElementType`. Define the token in your `tokens` block to eliminate the warning:

```bnf
{
  tokens = [
    PLUS = '+'    // named token -- fast IElementType match
  ]
}
// Before: expr '+' expr    -- text match, triggers warning
// After:  expr PLUS expr   -- token match, no warning
```

### How does #auto recovery work?

Setting `recoverWhile="#auto"` on a rule generates a recovery predicate that matches everything except the rule's computed NEXT set. Grammar-Kit uses `BnfFirstNextAnalyzer` to calculate which tokens can follow the rule, then generates `!(token1 | token2 | ...)` as the recovery expression.

You can inspect the generated predicate by placing the cursor on the rule and pressing **Ctrl+Q** (Quick Documentation). See [Error Recovery and Pin](../grammar-development/error-recovery.md) for details on recovery strategies.

### When should I use left rules versus Pratt-style expression parsing?

Both approaches handle operator precedence, but they differ in structure. Pratt-style parsing (using `extends(".*expr")=expr`) works best when you have many precedence levels and want a flat PSI hierarchy. Left rules (using the `left` keyword) are simpler for grammars with fewer operators and give you explicit control over how precedence levels chain together.

The [Simple Scripting Language example](examples.md#simple-scripting-language) uses left rules. The [Expression Calculator example](examples.md#expression-calculator) uses Pratt parsing. See [Expression Parsing](../grammar-development/expression-parsing.md) for a detailed comparison.

## Code Generation

### Why are my method mixins not working with Gradle?

The Gradle grammar-kit plugin runs a single-pass generation. Method mixins require two passes: the first pass discovers the mixin class's methods, and the second pass adds those methods to the generated PSI interfaces. Only IDE generation (**Ctrl+Shift+G**) supports two-pass mode.

If you need method mixins in a Gradle build, generate the PSI code from the IDE and commit it to version control. See [Gradle vs IDE Generation](../integration/gradle-vs-ide.md) for a full comparison of capabilities.

### How do I split a large grammar across multiple files?

Use parser class override blocks to direct rules into separate parser classes:

```bnf
// Rules above go into the default parser class

;{
  parserClass="org.example.Parser2"
}
// Rules below this block generate into Parser2.java
```

The semicolon before `{` marks this as a global attribute block rather than a rule attribute. Each block can specify a different `parserClass`, splitting the generated code across multiple files. See [Attributes System](../code-generation/attributes.md) for the full attribute syntax.

### How do I target a specific Java version?

Set the `java` generation option in your grammar's header:

```bnf
{ generate=[java="8"] }
```

Java 8 and above generate lambda expressions for token sets and other constructs. Java 6 generates anonymous inner classes instead. The default since Grammar-Kit 2020.3 is Java 11.

## IDE Integration

### How do I create a ParserDefinition?

Implement `ParserDefinition` and register it in `plugin.xml`. The minimal implementation needs six methods:

```java
public class MyParserDefinition implements ParserDefinition {
  public Lexer createLexer(Project project) {
    return new MyLexer();
  }
  public PsiParser createParser(Project project) {
    return new MyParser();
  }
  public IFileElementType getFileNodeType() {
    return FILE;  // static IFileElementType constant
  }
  public TokenSet getWhitespaceTokens() {
    return TokenSet.create(MyTypes.SPACE);
  }
  public TokenSet getCommentTokens() {
    return TokenSet.create(MyTypes.COMMENT);
  }
  public PsiElement createElement(ASTNode node) {
    throw new UnsupportedOperationException();
    // Grammar-Kit uses the factory in the types holder class
  }
  public PsiFile createFile(FileViewProvider viewProvider) {
    return new MyFile(viewProvider);
  }
}
```

Register it in `plugin.xml`:

```xml
<lang.parserDefinition language="MyLang"
    implementationClass="org.example.MyParserDefinition"/>
```

For a complete walkthrough, see [Parser Definition](../integration/parser-definition.md).

### How do I suppress a Grammar-Kit inspection?

Add a comment directly above the rule:

```bnf
//noinspection BnfUnusedRule
unused_helper ::= something
```

This follows the same `//noinspection` convention used throughout IntelliJ-based tools.

## Troubleshooting

### My generated parser does not compile: element types not found

The lexer must return the same `IElementType` constants that Grammar-Kit generates in your `elementTypeHolderClass`. Common causes:

- The JFlex file imports from the wrong types class.
- The `elementTypePrefix` in the grammar does not match the token names in the JFlex file.
- The JFlex file was generated before the BNF file, so it references outdated constants.

Regenerate the `.flex` file from your grammar, then regenerate the lexer. Make sure the import in the flex file points to the correct `elementTypeHolderClass`.

### Live Preview does not work with my external rules

Live Preview only supports the built-in `eof` and `anything` external rules. External rules that reference static Java methods require compiled code, which Live Preview does not have access to. Meta rules and their arguments do work in Live Preview because they are resolved within the grammar itself.

If you need to test rules that depend on external methods, generate the parser and write a unit test instead. See [Testing](../integration/testing.md).

### How do I use stub indexes with Grammar-Kit?

Grammar-Kit supports two approaches for stub-based PSI elements.

The direct approach specifies the stub type explicitly:

```bnf
my_class ::= 'class' id '{' item* '}' {
  implements=["com.intellij.psi.StubBasedPsiElement<MyClassStub>"]
  mixin="org.example.MyClassMixin<MyClassStub>"
}
```

The shorthand approach uses `stubClass`:

```bnf
my_class ::= 'class' id '{' item* '}' {
  stubClass="org.example.MyClassStub"
  extends="org.example.MyBaseStubElement<?>"
}
```

In the shorthand form, `<?>` is replaced with the stub class automatically. Both approaches require `elementTypeFactory` to produce `IStubElementType` instances instead of the default `IElementType`. See [PSI Customization](../code-generation/psi-customization.md) for implementation details.
