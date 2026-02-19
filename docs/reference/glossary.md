# Glossary

Terms used throughout the Grammar-Kit documentation, organized alphabetically.

## A

**AST (Abstract Syntax Tree)**
:   The low-level tree structure that represents parsed source code. In IntelliJ, the AST sits beneath the PSI layer. Grammar-Kit generates parsers that build AST nodes, which are then wrapped by PSI elements.

**ASTWrapperPsiElement**
:   The default base class for generated PSI elements. It wraps an AST node and delegates tree operations to it. Override this through the `extends` or `mixin` attributes.

## B

**BNF (Backus-Naur Form)**
:   A notation for describing context-free grammars. Grammar-Kit uses an extended variant (EBNF) that adds quantifiers (`?`, `+`, `*`), grouping, and optional syntax.

## C

**Choice**
:   Alternative branches in a rule, separated by `|`. The parser tries each branch in declaration order.

**CompositePsiElement**
:   A merged AST/PSI tree element used in some IntelliJ implementations. An alternative to the wrapper approach of `ASTWrapperPsiElement`.

**consumeTokenMethod**
:   A rule-level [attribute](attributes.md) that controls which method the generated parser calls to consume tokens. Use `consumeTokenFast` to skip error position recording in performance-sensitive rules.

## E

**EBNF (Extended Backus-Naur Form)**
:   An extension of BNF that adds quantifiers (`?`, `+`, `*`), optional groups (`[ ]`), and other convenience syntax. Grammar-Kit's `.bnf` files use EBNF notation.

**Element type**
:   An `IElementType` constant that identifies a kind of AST node. Grammar-Kit generates one element type per public rule and collects them in the element type holder class.

**Element type holder**
:   A generated class (configured by `elementTypeHolderClass`) that contains all `IElementType` constants for a grammar. Both composite element types (for rules) and token types are declared here.

**Expression**
:   The right-hand side of a rule definition, consisting of sequences, choices, and quantified terms.

**External rule**
:   A rule declared with the `external` modifier. No parsing code is generated; the parse function is hand-written and referenced by name. See [External Rules](../grammar-development/external-rules.md).

**Extra root**
:   An additional parsing entry point within a grammar, marked with the `extraRoot` attribute. Extra roots let you parse embedded fragments or secondary structures within the same file.

## F

**Fake rule**
:   A rule declared with the `fake` modifier. Only PSI classes are generated; no parsing code is produced. Fake rules are used to create abstract PSI base classes for expression hierarchies.

**FIRST set**
:   The set of tokens that can appear at the beginning of a rule. Grammar-Kit computes FIRST sets automatically and uses them for lookahead optimization. View a rule's FIRST set with Quick Documentation (++ctrl+q++ / ++cmd+j++).

## G

**GeneratedParserUtilBase**
:   The runtime support class that generated parsers depend on. It provides token consumption, error recovery, and other parsing utilities. Override it through the `parserUtilClass` attribute.

**Grammar highlighting**
:   An IDE feature that links the Live Preview caret position to the corresponding grammar expression. Toggle it with ++ctrl+alt+f7++ / ++cmd+alt+f7++.

## I

**IElementType**
:   The IntelliJ platform class that identifies AST node types. Grammar-Kit generates `IElementType` constants for each rule and token.

**IFileElementType**
:   A specialized `IElementType` for the root node of a file's parse tree.

**Inner rule**
:   A rule declared with the `inner` modifier. Used together with `left`, it takes the previous sibling and becomes its child rather than its parent.

## J

**JFlex**
:   A lexer generator that produces Java lexer classes from `.flex` specifications. Grammar-Kit integrates with JFlex for lexer generation and provides IDE support for `.flex` files.

## L

**Left recursion**
:   A grammar pattern where a rule can invoke itself as its first element. Grammar-Kit handles left recursion through the expression parsing framework using `extends` and `left` rules, rather than direct left-recursive definitions.

**Left rule**
:   A rule declared with the `left` modifier. It takes the previous sibling AST node and becomes its parent, which is the mechanism for left-associative binary operators.

**LightPsiParser**
:   An optimized parser interface in the IntelliJ platform. Generated parsers implement this interface for lightweight parsing.

**Live Preview**
:   A Grammar-Kit feature that lets you test a grammar in real time without generating code. Open it with ++ctrl+alt+p++ / ++cmd+alt+p++. See [Live Preview](../grammar-development/live-preview.md).

## M

**Meta rule**
:   A rule declared with the `meta` modifier. It accepts parse functions as parameters, enabling reusable grammar patterns like generic lists. Parameters are referenced with `<<param>>` syntax.

**Method mix-in**
:   A static method from the `psiImplUtilClass` that is injected into a generated PSI class. Defined through the `methods` attribute on a rule.

**Mixin**
:   A hand-written implementation class that replaces the generated implementation in the PSI hierarchy. Set through the `mixin` attribute on a rule. See [PSI Customization](../code-generation/psi-customization.md).

## N

**NEXT set**
:   The set of tokens that can appear after a rule completes. Grammar-Kit uses NEXT sets for `#auto` recovery and displays them in Quick Documentation.

## P

**ParserDefinition**
:   An IntelliJ platform interface that connects the lexer, parser, and PSI factory. You implement this interface to register your language's parser with the IDE.

**Pin**
:   A rule-level [attribute](attributes.md) that marks a position in a sequence after which the parser commits to the match and reports errors instead of backtracking. Essential for error recovery. See [Error Recovery](../grammar-development/error-recovery.md).

**Pratt parsing**
:   An operator-precedence parsing technique. Grammar-Kit uses a variant of Pratt parsing for expression rules, configured through `extends` attributes and rule ordering. See [Expression Parsing](../grammar-development/expression-parsing.md).

**Predicate**
:   A lookahead test that succeeds or fails without consuming input. `&` is a positive predicate (match required), `!` is a negative predicate (match must fail).

**Private rule**
:   A rule declared with the `private` modifier. No AST node is generated; the rule's child nodes fold directly into the parent node.

**PsiBuilder**
:   The IntelliJ platform interface for constructing parse trees incrementally. Generated parsers use `PsiBuilder` to create markers and build the AST.

**PSI (Program Structure Interface)**
:   The IntelliJ platform's high-level parsed tree representation. PSI elements wrap AST nodes and provide typed accessors, navigation, and modification APIs. Grammar-Kit generates PSI interfaces and implementation classes from grammar rules.

## Q

**Quantifier**
:   A suffix operator that controls repetition: `?` (zero or one), `+` (one or more), `*` (zero or more).

## R

**Recovery**
:   The mechanism by which the parser skips tokens after encountering an error, controlled by the `recoverWhile` attribute and `pin`. See [Error Recovery](../grammar-development/error-recovery.md).

**Rule**
:   A named grammar production that defines a syntactic construct. Rules are the building blocks of a `.bnf` grammar.

## S

**Sequence**
:   An ordered list of grammar terms that must match consecutively.

**StubBasedPsiElementBase**
:   A base class for PSI elements that support stub-based indexing. Used when the `stubClass` attribute is set on a rule.

## T

**Token**
:   An atomic lexical element returned by the lexer. Tokens are the smallest units the parser works with: keywords, operators, identifiers, literals.

**Token type**
:   An `IElementType` subclass that identifies a kind of token. Configured through `tokenTypeClass` or `tokenTypeFactory`.

**TokenSet**
:   An immutable set of `IElementType` values used in the IntelliJ platform for grouping related token types (e.g., all whitespace tokens, all comment tokens).

## U

**Upper rule**
:   A rule declared with the `upper` modifier. It takes the parent AST node and replaces it. This is a rarely used advanced feature.

## File Extensions

| Extension | Description |
|---|---|
| `.bnf` | Grammar-Kit grammar definition file |
| `.flex` | JFlex lexer specification file |
