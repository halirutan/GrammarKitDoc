# Section 6.4: Glossary — Code Evidence

## Parser and Grammar Terms

| Term | Definition | Source |
|---|---|---|
| **BNF** | Backus-Naur Form; a notation for context-free grammars | Standard terminology |
| **EBNF** | Extended BNF; adds quantifiers (`?`, `+`, `*`), grouping, optional syntax | `README.md:8-10` |
| **Rule** | A named grammar production that defines a syntactic construct | `grammars/Grammar.bnf:64` |
| **Token** | An atomic lexical element returned by the lexer | `KnownAttribute.java:51` (tokens attr) |
| **Expression** | The right-hand side of a rule definition | `grammars/Grammar.bnf:94` |
| **Sequence** | Ordered list of grammar options that must match in order | `grammars/Grammar.bnf:95` |
| **Choice** | Alternative branches separated by `\|` | `grammars/Grammar.bnf:102` |
| **Quantifier** | `?` (optional), `+` (one-or-more), `*` (zero-or-more) | `grammars/Grammar.bnf:103-104` |
| **Predicate** | `&` (positive look-ahead) or `!` (negative look-ahead) | `grammars/Grammar.bnf:106-107` |
| **Pin** | Marks a point in a sequence after which errors are tolerated | `attributeDescriptions/pin.html` |
| **Recovery** | Mechanism to skip tokens after a parse error | `attributeDescriptions/recoverWhile.html` |
| **Left recursion** | A rule that can invoke itself as its first element | `BnfLeftRecursionInspection.java:38` |
| **FIRST set** | Tokens that can begin parsing a given rule | `BnfFirstNextAnalyzer.java:40` |
| **NEXT set** | Tokens that can follow a given rule | `BnfFirstNextAnalyzer.java:41` |
| **Pratt parsing** | Operator-precedence parsing technique for expressions | `HOWTO.md:124-223` |

## Grammar-Kit Specific Terms

| Term | Definition | Source |
|---|---|---|
| **Private rule** | Rule that generates no AST node; children merge into parent | `README.md:132` |
| **Left rule** | Rule that takes the previous sibling and becomes its parent | `README.md:135` |
| **Fake rule** | Rule that generates only PSI classes, no parser code | `README.md:141` |
| **Meta rule** | Parametrized rule that accepts parse functions as arguments | `README.md:139` |
| **External rule** | Rule with hand-written parse function | `README.md:138` |
| **Upper rule** | Rule that takes the parent node and replaces it | `README.md:137` |
| **Inner rule** | Used with left; takes previous sibling as child | `README.md:136` |
| **Mixin** | Implementation class mixed into PSI hierarchy | `attributeDescriptions/mixin.html` |
| **Method mix-in** | Static method from `psiImplUtilClass` injected into PSI | `HOWTO.md:323-341` |
| **Element type** | `IElementType` constant identifying an AST node type | `BnfConstants.java:24` |
| **Token type** | `IElementType` subclass for lexer tokens | `attributeDescriptions/tokenTypeClass.html` |
| **Element type holder** | Generated class containing all `IElementType` constants | `KnownAttribute.java:48` |
| **Extra root** | Additional parsing entry point within a grammar | `attributeDescriptions/extraRoot.html` |
| **Live Preview** | Real-time grammar testing mode without code generation | `TUTORIAL.md:47` |
| **Grammar highlighting** | Feature linking preview caret to grammar expressions | `GrammarAtCaretPassFactory.java` |

## IntelliJ Platform Terms

| Term | Definition | Source |
|---|---|---|
| **PSI** | Program Structure Interface; the parsed tree representation | `BnfConstants.java:25-26` |
| **AST** | Abstract Syntax Tree; low-level tree structure | `BnfConstants.java:28` |
| **PsiBuilder** | Builder interface for constructing parse trees | `BnfConstants.java:19` |
| **IElementType** | Type identifier for AST/PSI nodes | `BnfConstants.java:24` |
| **IFileElementType** | Element type for the file root node | `BnfParserDefinition.java:30` |
| **TokenSet** | Immutable set of `IElementType` values | `BnfConstants.java:22` |
| **ParserDefinition** | Interface connecting lexer, parser, and PSI factory | `BnfParserDefinition.java:28` |
| **LightPsiParser** | Optimized parser interface for lightweight parsing | `BnfConstants.java:21` |
| **ASTWrapperPsiElement** | Default PSI element wrapping an AST node | `BnfConstants.java:29` |
| **StubBasedPsiElementBase** | Base class for stub-indexed PSI elements | `BnfConstants.java:39` |
| **CompositePsiElement** | Merged AST/PSI tree element | `BnfConstants.java:30` |
| **GeneratedParserUtilBase** | Runtime support class for generated parsers | `BnfConstants.java:18` |
| **FlexLexer** | JFlex-generated lexer interface | Lexer template |

## File Extensions

| Extension | Type | Description |
|---|---|---|
| `.bnf` | BNF Grammar | Grammar-Kit grammar definition |
| `.flex` | JFlex Lexer | JFlex lexer specification |
| `.preview` | Live Preview | Live Preview virtual file |
