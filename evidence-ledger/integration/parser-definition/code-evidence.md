# Section 4.1.1: Parser Definition — Code Evidence

## 1. BnfParserDefinition Implementation

**Source: `src/org/intellij/grammar/BnfParserDefinition.java:28-78`**

Grammar-Kit's own `ParserDefinition` serves as the reference implementation:

```java
public class BnfParserDefinition implements ParserDefinition {
  public static final IFileElementType BNF_FILE_ELEMENT_TYPE = new IFileElementType("BNF_FILE", BnfLanguage.INSTANCE);

  @Override public @NotNull Lexer createLexer(Project project) { return new BnfLexer(); }
  @Override public @NotNull PsiParser createParser(Project project) { return new GrammarParser(); }
  @Override public @NotNull IFileElementType getFileNodeType() { return BNF_FILE_ELEMENT_TYPE; }
  @Override public @NotNull TokenSet getWhitespaceTokens() { return BnfTokenSets.WS; }
  @Override public @NotNull TokenSet getCommentTokens() { return BnfTokenSets.COMMENTS; }
  @Override public @NotNull TokenSet getStringLiteralElements() { return BnfTokenSets.LITERALS; }
  @Override public @NotNull PsiElement createElement(ASTNode astNode) {
    throw new UnsupportedOperationException(astNode.getElementType().toString());
  }
  @Override public @NotNull PsiFile createFile(@NotNull FileViewProvider fileViewProvider) {
    return new BnfFileImpl(fileViewProvider);
  }
  @Override public @NotNull SpaceRequirements spaceExistenceTypeBetweenTokens(ASTNode n1, ASTNode n2) {
    if (n1.getElementType() == BnfTypes.BNF_LINE_COMMENT) return SpaceRequirements.MUST_LINE_BREAK;
    return SpaceRequirements.MAY;
  }
}
```

Key points:
- `createElement()` throws `UnsupportedOperationException` — PSI factory in the element types holder is used instead.
- `IFileElementType` is a static constant with the language instance.
- `createFile()` returns a custom `BnfFileImpl`.

## 2. Token Sets

**Source: `src/org/intellij/grammar/BnfTokenSets.java:11-28`**

```java
public final class BnfTokenSets {
  public static final TokenSet WS = TokenSet.WHITE_SPACE;
  public static final TokenSet COMMENTS = TokenSet.create(BNF_LINE_COMMENT, BNF_BLOCK_COMMENT);
  public static final TokenSet LITERALS = TokenSet.create(BnfTypes.BNF_STRING);
  public static final TokenSet PARENS_L = TokenSet.create(BNF_LEFT_PAREN, BNF_LEFT_BRACE, BNF_LEFT_BRACKET, BNF_EXTERNAL_START);
  public static final TokenSet PARENS_R = TokenSet.create(BNF_RIGHT_PAREN, BNF_RIGHT_BRACE, BNF_RIGHT_BRACKET, BNF_EXTERNAL_END);
  public static final TokenSet OPERATORS = TokenSet.create(BNF_OP_AND, BNF_OP_EQ, BNF_OP_NOT, BNF_OP_ONEMORE, BNF_OP_OPT, BNF_OP_OR, BNF_OP_ZEROMORE);
}
```

## 3. Plugin Registration

**Source: `resources/META-INF/plugin.xml:14-18`**

```xml
<fileType name="BNF" implementationClass="org.intellij.grammar.BnfFileType" fieldName="INSTANCE" extensions="bnf" language="BNF"/>
<lang.parserDefinition language="BNF" implementationClass="org.intellij.grammar.BnfParserDefinition"/>
<lang.ast.factory language="BNF" implementationClass="org.intellij.grammar.BnfASTFactory"/>
```

Registration pattern: `lang.parserDefinition` extension point with language ID.

## 4. Plugin Dependencies

**Source: `resources/META-INF/plugin.xml:9-12`**

```xml
<depends>com.intellij.modules.lang</depends>
<depends optional="true" config-file="plugin-copyright.xml">com.intellij.copyright</depends>
<depends optional="true" config-file="plugin-java.xml">com.intellij.java</depends>
<depends optional="true" config-file="plugin-uml.xml">com.intellij.diagram</depends>
```

Minimum dependency: `com.intellij.modules.lang`.

## 5. LivePreviewParserDefinition

**Source: `src/org/intellij/grammar/livePreview/LivePreviewParserDefinition.java:27-94`**

Shows how ParserDefinition works with dynamically generated languages in Live Preview mode.

## 6. LightPsi: Standalone Parsing

**Source: `src/org/intellij/grammar/LightPsi.java:49-82`**

`LightPsi` enables parsing without a full IntelliJ application:
```java
public static @Nullable PsiFile parseFile(@NotNull String name, @NotNull String text, @NotNull ParserDefinition parserDefinition)
public static @NotNull ASTNode parseText(@NotNull String text, @NotNull ParserDefinition parserDefinition)
public static @NotNull SyntaxTraverser<LighterASTNode> parseLight(@NotNull String text, @NotNull ParserDefinition parserDefinition)
```

Used in command-line generation and testing scenarios.
