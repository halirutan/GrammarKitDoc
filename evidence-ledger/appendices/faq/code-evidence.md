# Section 7.C: FAQ — Code Evidence

## Grammar Development Questions

### Q: How do I handle left recursion?
**Source: `BnfLeftRecursionInspection.java:38`, `HOWTO.md:124-223`**

Grammar-Kit does not support general left recursion. The inspection warns: `"'<rule>' employs left-recursion unsupported by generator"`. Use expression parsing instead:
```bnf
expr ::= plus_expr | literal_expr
plus_expr ::= expr '+' expr   // handled by Pratt parser
```
Rules with `extends(".*_expr")=expr` are detected as expression rules and handled via Pratt parsing.

### Q: What's the difference between `private` and `fake` rules?
**Source: `README.md:131-147`**

- `private` rules participate in parsing but create no AST nodes; their children are merged into the parent.
- `fake` rules generate PSI classes only; no parsing code is produced. They exist purely for PSI hierarchy shaping.
- `fake` should NOT be combined with `private`.

### Q: Why does my token show "Tokens matched by text are slower"?
**Source: `BnfAnnotator.java:140-151`**

Quoted strings in rule bodies that don't correspond to named tokens are matched by text comparison at runtime, which is slower than matching by `IElementType`. Define tokens in the `tokens` attribute to avoid this.

### Q: How does `#auto` recovery work?
**Source: `BnfDocumentationProvider.java:56-69`, `BnfFirstNextAnalyzer.java`**

`recoverWhile="#auto"` generates a recovery predicate that matches `!(NEXT_SET)`. The NEXT set is computed by `BnfFirstNextAnalyzer.calcNext(rule)`. You can see the generated predicate via Quick Documentation (Ctrl-Q).

## Code Generation Questions

### Q: Why aren't my method mixins working with Gradle?
**Source: `README.md:44-51`**

The Gradle grammar-kit plugin does not implement two-pass generation. Method mixins require the first pass to discover the mixin class's methods, then the second pass generates PSI interfaces including those methods. Use IDE generation (Ctrl-Shift-G) for method mixins.

### Q: How do I split a large grammar across multiple files?
**Source: `attributeDescriptions/parserClass.html`**

Use `;{parserClass="..."}` blocks:
```bnf
;{
  parserClass="org.example.Parser2"
}
// Rules after this generate into Parser2.java
```
The semicolon before `{` is required to mark it as a global attribute block.

### Q: How do I generate Java 8 lambdas?
**Source: `CHANGELOG.md:110`, `GenOptions.java:131`**

```bnf
{ generate=[java="8"] }
```
Default since 2020.3 is Java 11, which also generates lambdas. Use `java="6"` for anonymous classes.

## IDE Integration Questions

### Q: How do I create a ParserDefinition?
**Source: `BnfParserDefinition.java:28-78`**

Implement `ParserDefinition` with:
- `createLexer()` — return your JFlex-generated lexer
- `createParser()` — return your Grammar-Kit-generated parser
- `getFileNodeType()` — return a static `IFileElementType` constant
- `getWhitespaceTokens()` / `getCommentTokens()` — return token sets
- `createElement()` — throw `UnsupportedOperationException` (factory in types holder is used)
- `createFile()` — return your `PsiFile` subclass

Register in `plugin.xml`: `<lang.parserDefinition language="..." implementationClass="..."/>`

### Q: How do I suppress an inspection?
**Source: `BnfInspectionSuppressor.java`, `CHANGELOG.md:152`**

Add a comment before the rule: `//noinspection BnfUnusedRule`

## Troubleshooting Questions

### Q: Generated parser doesn't compile — element types not found?
**Source: `README.md:219-243`**

The lexer must return the same `IElementType` constants generated in `elementTypeHolderClass`. Make sure your JFlex file imports from the correct types class and returns constants with the correct `elementTypePrefix`.

### Q: Live Preview doesn't work with my external rules?
**Source: `LivePreviewParser.java:346-350`**

External rules that reference static methods are NOT supported in Live Preview. Only `eof` and `anything` built-in externals work. Meta rules and their arguments do work.

### Q: How do I use stub indexes with Grammar-Kit?
**Source: `HOWTO.md:346-381`, `testData/generator/Stub.bnf`**

Two approaches:
1. Direct: `implements=[..., "StubBasedPsiElement<MyStub>"]` + `mixin="MyStubElement<MyStub>"`
2. Shorthand: `stubClass="MyStub"` + `extends="MyBase<?>"` (the `<?>` is replaced with stub class)

Both require `elementTypeFactory` to create `IStubElementType` instances.
