# Parser Definition

Every IntelliJ language plugin needs a `ParserDefinition` to connect the parser and lexer to the platform. This class tells the IDE how to create tokens, build PSI trees, and categorize whitespace and comments for your language. Grammar-Kit generates the parser and PSI classes; `ParserDefinition` is the glue that ties them into the platform.

## Implementing ParserDefinition

The `ParserDefinition` interface requires you to supply a lexer, a parser, token sets, and factory methods for PSI elements and files. Grammar-Kit's own BNF language provides a clear reference implementation:

```java
public class MyParserDefinition implements ParserDefinition {

  public static final IFileElementType FILE =
      new IFileElementType("MY_FILE", MyLanguage.INSTANCE);

  @Override
  public @NotNull Lexer createLexer(Project project) {
    return new MyLexer();
  }

  @Override
  public @NotNull PsiParser createParser(Project project) {
    return new MyParser();
  }

  @Override
  public @NotNull IFileElementType getFileNodeType() {
    return FILE;
  }

  @Override
  public @NotNull TokenSet getWhitespaceTokens() {
    return MyTokenSets.WHITESPACE;
  }

  @Override
  public @NotNull TokenSet getCommentTokens() {
    return MyTokenSets.COMMENTS;
  }

  @Override
  public @NotNull TokenSet getStringLiteralElements() {
    return MyTokenSets.STRINGS;
  }

  @Override
  public @NotNull PsiElement createElement(ASTNode node) {
    return MyTypes.Factory.createElement(node);
  }

  @Override
  public @NotNull PsiFile createFile(@NotNull FileViewProvider viewProvider) {
    return new MyFile(viewProvider);
  }
}
```

`createLexer()` and `createParser()` return the lexer and parser that Grammar-Kit generated for you. `getFileNodeType()` returns a static `IFileElementType` constant bound to your `Language` instance. Define it once and reuse it; creating multiple instances for the same language causes errors.

The `createElement()` method delegates to the generated `Factory` class inside your element types holder (typically named `MyTypes`). Grammar-Kit generates this factory automatically when `generatePsi` is enabled. If your grammar uses a custom `elementTypeFactory`, the factory method in the types holder handles all dispatch, so `createElement()` can simply delegate.

`createFile()` returns an instance of your `PsiFile` subclass. This class is not generated and you write it yourself. It typically extends `PsiFileBase` and passes your language and file type to the superclass constructor.

## Defining Token Sets

Token sets classify tokens for the platform. The IDE uses them to skip whitespace and comments during PSI tree operations, reference resolution, and formatting. Organize your token sets in a dedicated class:

```java
public final class MyTokenSets {
  public static final TokenSet WHITESPACE = TokenSet.WHITE_SPACE;
  public static final TokenSet COMMENTS =
      TokenSet.create(MyTypes.LINE_COMMENT, MyTypes.BLOCK_COMMENT);
  public static final TokenSet STRINGS =
      TokenSet.create(MyTypes.STRING_LITERAL);
}
```

`TokenSet.WHITE_SPACE` handles standard whitespace. For comments, create a set from the comment token types your lexer produces. The platform treats tokens in `getCommentTokens()` similarly to whitespace during tree walks and reference searches, so include all comment variants. The string literal set is used by features like spell checking and language injection.

You can define additional token sets for your own use, such as operator sets or keyword sets, but only the three sets returned by `ParserDefinition` methods affect platform behavior directly.

## Registration

Register the parser definition, file type, and AST factory in your `plugin.xml`:

```xml
<extensions defaultExtensionNs="com.intellij">
  <fileType name="My"
            implementationClass="com.example.MyFileType"
            fieldName="INSTANCE"
            extensions="my"
            language="My"/>
  <lang.parserDefinition
            language="My"
            implementationClass="com.example.MyParserDefinition"/>
</extensions>
```

The `language` attribute must match the string ID you pass to your `Language` subclass constructor. Your plugin must declare a dependency on `com.intellij.modules.lang` in the `<depends>` section, which provides the language extension points.

!!! note
    If your language needs an AST factory (for example, to create custom `ASTNode` subclasses), register it separately with the `lang.ast.factory` extension point.

## Standalone Parsing with LightPsi

Grammar-Kit includes `LightPsi`, a lightweight utility that creates a minimal IntelliJ environment for parsing outside a running IDE. This is useful for command-line code generation and unit tests that do not need the full platform:

```java
PsiFile file = LightPsi.parseFile("test.my", sourceText, new MyParserDefinition());
ASTNode tree = LightPsi.parseText(sourceText, new MyParserDefinition());
```

`LightPsi` sets up a `CoreApplicationEnvironment` and `CoreProjectEnvironment` with just enough infrastructure for parsing. It does not provide project-level services, so features like reference resolution and type checking are not available in this mode.

For full integration testing, use the IntelliJ test framework instead. See [Testing](testing.md) for details on setting up parser and feature tests.
