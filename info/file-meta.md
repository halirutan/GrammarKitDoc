# GrammarKit Documentation-Relevant Files

## Documentation Files
README.md | Main docs: usage instructions, syntax overview, rule modifiers, meta rules, tokens, error recovery attrs
TUTORIAL.md | Live Preview tutorial: pin/recoverWhile examples, expression grammar with left rules, workflow summary
HOWTO.md | Advanced docs: parser code mapping, recoverWhile usage, external rules, expression parsing, PSI hierarchy, stubs
CHANGELOG.md | Version history with feature changes and fixes
LICENSE.md | Apache 2.0 license info
CODE_OF_CONDUCT.md | JetBrains community guidelines reference

## Grammar Definition Files
grammars/Grammar.bnf | BNF grammar self-definition: complete syntax, all modifiers, attrs, tokens, extends/implements patterns
grammars/JFlex.bnf | JFlex grammar definition: lexer sections, options, macros, rules, expressions, regex patterns

## Attribute Description Files (resources/messages/attributeDescriptions/)
pin.html | pin attr: sequence pinning contract, parenthesized list example
recoverWhile.html | recoverWhile attr: recovery predicate contract, #auto mode, usage with pin
extends.html | extends attr: PSI hierarchy, AST collapsing, fake rules, stub example
implements.html | implements attr: PSI interface list example
mixin.html | mixin attr: impl class hierarchy injection example
methods.html | methods attr: PSI accessors /path syntax, method mix-ins, renaming accessors
hooks.html | hooks attr: whitespace binders (left/right/both), custom hooks, logHook
generate.html | generate attr: full options table (psi, tokens, visitor, java version, names, first-check, etc)
tokens.html | tokens attr: regexp tokens, simple tokens, keyword tokens
elementType.html | elementType attr: shared element types, existing PSI integration
elementTypeFactory.html | elementTypeFactory attr: custom IElementType factory method
elementTypeClass.html | elementTypeClass attr: IElementType subclass for composite nodes
elementTypeHolderClass.html | elementTypeHolderClass attr: types holder class with constants
elementTypePrefix.html | elementTypePrefix attr: prefix for generated element type constants
tokenTypeClass.html | tokenTypeClass attr: IElementType subclass for tokens
tokenTypeFactory.html | tokenTypeFactory attr: custom token type factory method
parserClass.html | parserClass attr: generated parser class, splitting grammar across files
parserUtilClass.html | parserUtilClass attr: parser util class, external method resolution
parserImports.html | parserImports attr: additional static imports for parser
psiPackage.html | psiPackage attr: PSI interface package name
psiImplPackage.html | psiImplPackage attr: PSI impl package name
psiClassPrefix.html | psiClassPrefix attr: prefix for PSI class names
psiImplClassSuffix.html | psiImplClassSuffix attr: suffix for PSI impl classes
psiImplUtilClass.html | psiImplUtilClass attr: method mix-in utility class
psiVisitorName.html | psiVisitorName attr: visitor class name
psiTreeUtilClass.html | psiTreeUtilClass attr: tree util class override
rightAssociative.html | rightAssociative attr: operator associativity for expressions
extraRoot.html | extraRoot attr: marking extra root rules for parse_extra_roots()
stubClass.html | stubClass attr: stub index support, StubBasedPsiElement generation
fallbackStubElementType.html | fallbackStubElementType attr: fallback stub type class
consumeTokenMethod.html | consumeTokenMethod attr: token matching method (regular/smart/fast)
generatePsi.html | generatePsi attr (deprecated): toggle PSI class generation
generateTokens.html | generateTokens attr (deprecated): toggle token constant generation
generateTokenAccessors.html | generateTokenAccessors attr: toggle token getter methods
generateFirstCheck.html | generateFirstCheck attr: FIRST-based lookahead optimization depth
extendedPin.html | extendedPin attr: parse sequence tail after pin (default true)
name.html | name attr: rule display name in error messages
classHeader.html | classHeader attr: file header text or license file

## Inspection Descriptions (resources/inspectionDescriptions/)
BnfLeftRecursion.html | Inspection: detects left recursion causing StackOverflowError
BnfSuspiciousToken.html | Inspection: highlights tokens that may be rule references
BnfUnusedRule.html | Inspection: detects unused rules
BnfDuplicateRule.html | Inspection: checks rule name uniqueness
BnfResolve.html | Inspection: unresolved rule/token references
BnfUnusedAttribute.html | Inspection: detects unused attributes
BnfIdenticalChoiceBranches.html | Inspection: identical choice branches detection
BnfUnreachableChoiceBranch.html | Inspection: unreachable choice branch detection

## Intention Descriptions (resources/intentionDescriptions/)
BnfFlipChoiceIntention/description.html | Intention: flip choice branch arguments
BnfConvertOptExpressionIntention/description.html | Intention: convert optional expression syntax

## Lexer Templates (resources/templates/)
lexer.flex.template | JFlex lexer template: Velocity template for generating .flex files
fleet.lexer.flex.template | Fleet-specific JFlex lexer template variant

## Test Data - Generator Examples (testData/generator/)
ExprParser.bnf | Expression parser: left recursion, extends, extraRoot, rightAssociative, fake rules, n-ary ops
ExternalRules.bnf | External/meta rules: external rule syntax, meta rules with params, comma_list pattern
Autopin.bnf | Auto-pinning: pin patterns on rule names, pattern-based extends, external refs
AutoRecovery.bnf | Auto recovery: #auto recoverWhile, parenthesized list with pin
BindersAndHooks.bnf | Hooks: leftBinder, rightBinder, wsBinders, custom hooks with parserImports
PsiGen.bnf | PSI generation: extends patterns, elementType, mixin, implements, fake rules, external_type
Stub.bnf | Stub support: stubClass attr, extends with StubBase, multiple stub elements
PsiAccessors.bnf | PSI accessors: methods attr paths (/expr[0], /expr[last]), nested accessors, fake rules
GenOptions.bnf | Generator options: generate attr (java, fqn, visitor-value, token-case, element-case)
LeftAssociative.bnf | Left modifier: left, inner, private combinations for AST restructuring
ConsumeMethods.bnf | Consume methods: consumeTokenMethod attr (regular/smart/fast) inheritance
UpperRules.bnf | Upper modifier: upper rule behavior, PSI factory generation toggle
Small.bnf | Basic examples: external, private, empty rules, parserImports
UtilMethods.bnf | Util methods: psiImplUtilClass method mix-ins pattern
TokenChoice.bnf | Token choices: token set generation from top-level choices
TokenSequence.bnf | Token sequences: pin pattern on choice branches
Fixes.bnf | Various fixes: edge cases in grammar patterns

## Test Data - Live Preview Examples (testData/livePreview/)
LivePreviewTutorial.bnf | Tutorial grammar: tokens, extends, name, pin, recoverWhile, left rules for expressions
Json.bnf | JSON grammar: extends, hooks (wsBinders, leftBinder, rightBinder), pin, recoverWhile
AutoRecovery.bnf | Auto recovery demo: #auto recoverWhile in live preview

## Source Files - Core Concepts (src/org/intellij/grammar/)
KnownAttribute.java | All known attributes: complete list with types, defaults, global/local scope flags
parser/GeneratedParserUtilBase.java | Runtime engine: Parser interface, Hook interface, binders, error recovery logic

## Plugin Configuration (resources/META-INF/)
plugin.xml | Plugin descriptor: extensions, actions, file types, inspections registration

## Build Configuration
build.gradle.kts | Build config: Grammar-Kit library dependency (org.jetbrains:grammar-kit), artifacts task, publishing
gradle.properties | Plugin metadata: version 2023.3-dev, requires IntelliJ 2023.3+, plugin name "Grammar-Kit"

## Visual Documentation
images/livePreview.png | Screenshot: Live Preview feature interface showing real-time grammar testing
images/editor.png | Screenshot: BNF editor interface with syntax highlighting and code completion

## Test Data - Fleet Examples (testData/fleet/)
FleetExternalRules.bnf | External rules: meta rule references, list parsing patterns
FleetPsiGen.bnf | PSI generation: psiClassPrefix, implements, extends attrs, element type customization
FleetExprParser.bnf | Expression parsing: operator precedence patterns
IFileTypeGeneration.bnf | File type generation example

## Test Data - Parser Examples (testData/parser/)
BrokenEverything.bnf | Error handling test cases
BrokenAttr.bnf | Invalid attribute syntax examples
ExternalExpression.bnf | External expression parsing patterns
Fixes.bnf | Grammar correction examples
AlternativeSyntax.bnf | Alternative BNF syntax forms
BrokenAttrBeforeEOF.bnf | EOF handling edge cases

## Test Data - Additional Live Preview (testData/livePreview/)
Case153.bnf | Live preview test case: specific parser behavior
Case75.bnf | Live preview test case: edge case handling
Case254.bnf | Live preview test case: complex parsing scenario
LiveFixes.bnf | Live preview fixes and corrections
UpperRules.bnf | Upper rule modifier behavior in live preview

## Test Data - JFlex Examples (testData/jflex/parser/)
ParserFixes.flex | JFlex lexer definition example
ParserFixes2.flex | Additional JFlex lexer patterns

## Source Files - Core Implementation (src/org/intellij/grammar/)
BnfFileType.java | BNF file type: .bnf extension, language registration
generator/ParserGenerator.java | Parser generation: core code generation from BNF, attribute processing
generator/ExpressionHelper.java | Expression parsing: operator precedence, associativity handling
generator/RuleGraphHelper.java | Grammar analysis: rule dependencies, left recursion detection, cardinality
psi/impl/GrammarUtil.java | Grammar utilities: rule navigation, attribute access helpers
psi/impl/GrammarPsiImplUtil.java | PSI utilities: reference resolution, rule type determination

## Source Files - Actions (src/org/intellij/grammar/actions/)
GenerateAction.java | Generate Parser Code action: batch generation, progress reporting, output directories
LivePreviewAction.java | Live Preview action: opens preview window for BNF files in editor menu

## Source Files - Live Preview (src/org/intellij/grammar/livePreview/)
LivePreviewHelper.java | Live preview impl: real-time grammar testing without code generation

## Source Files - JFlex Support (src/org/intellij/jflex/)
parser/JFlexFileType.java | JFlex file type: .flex extension, lexer definition support
parser/JFlexParserDefinition.java | JFlex parsing: syntax highlighting, structure view for .flex files
editor/JFlexCompletionContributor.java | JFlex completion: keywords, % directives, context-aware suggestions
editor/JFlexAnnotator.java | JFlex highlighting: macros, states, classes, unresolved references
psi/impl/JFlexPsiImplUtil.java | JFlex references: macro/state resolution, YYINITIAL handling

## Source Files - BNF Language Support (src/org/intellij/grammar/)
BnfParserDefinition.java | BNF language: .bnf files, whitespace/comment handling, line breaks required after comments
BnfCompletionContributor.java | Code completion: attributes, rules, tokens, keywords (private/external/meta), parser util methods
BnfStructureViewFactory.java | Structure view (Ctrl+F12): rules, attributes, sortable tree
BnfDocumentationProvider.java | Quick docs (Ctrl+Q): FIRST/FOLLOW sets, recovery predicates, expression priority
BnfFindUsagesProvider.java | Find usages (Alt+F7): rule references, attribute usages
analysis/BnfFirstNextAnalyzer.java | Grammar analysis: FIRST/FOLLOW sets, predicates, error recovery support

## Source Files - Editor Features (src/org/intellij/grammar/editor/)
BnfAnnotator.java | Syntax annotations: rule types, tokens, external refs, pin/recovery markers, string token warnings
BnfSyntaxHighlighter.java | Color scheme: 20+ configurable elements (rules, tokens, attributes, markers)
BnfColorSettingsPage.java | Color settings: IDE preferences page with preview, customizable syntax colors

## Source Files - Refactoring (src/org/intellij/grammar/refactor/)
BnfIntroduceTokenAction.java | Introduce Token: Refactor → Introduce → Token menu action
BnfIntroduceRuleAction.java | Introduce Rule: extract expression to new rule, works in injected fragments
BnfInlineRuleProcessor.java | Inline Rule: replace references with rule body, handles meta rules

## Source Files - Generator Configuration (src/org/intellij/grammar/generator/)
BnfConstants.java | Generator constants: regexp: prefix, #auto recovery, default imports
GenOptions.java | Generate options: psi/tokens/visitor flags, names style, Java version, case options
Names.java | Variable names: short (b,l,m), long (builder,level), classic (builder_,level_)
Case.java | Case transforms: UPPER (TOKEN_NAME), LOWER (token_name), CAMEL (TokenName), AS_IS

## Source Files - Additional Actions (src/org/intellij/grammar/actions/)
BnfGenerateLexerAction.java | Generate JFlex Lexer: creates .flex from BNF tokens, uses template
BnfRunJFlexAction.java | Run JFlex Generator: processes .flex files, downloads JFlex, batch support

## Source Files - Configuration (src/org/intellij/grammar/config/)
Options.java | Plugin settings: gen.dir (default "gen"), jflex.args, parser depth limit, injection settings

## Source Files - PSI API (src/org/intellij/grammar/psi/)
BnfFile.java | BNF file API: getRules(), getRule(name), getAttributes(), rule/attribute lookup
impl/BnfFileImpl.java | BNF implementation: rule/attribute caching, pattern matching, inheritance

## Resources
messages/GrammarKitBundle.properties | UI strings: action names, inspection names, intention names, error messages

## Test Data - Additional Generator Examples (testData/generator/)
StubFallback.bnf | Stub generation: custom stub classes, element type factories, stub inheritance
SelfBnf.bnf | Grammar-Kit's own BNF grammar: self-hosted parser generation
SelfFlex.bnf | JFlex grammar in BNF: lexer definition example
ExternalRulesLambdas.bnf | Meta rules: complex external rules, lambdas, multi-parser generation
PsiStart.bnf | Multiple entry points: extraRoot attribute usage
TokenChoiceNoSets.bnf | Generation control: fine-grained token set generation options

## Test Data - Expression Parser (testData/parser/expression/)
Simple.expr | Expression test cases: various parsing scenarios and error handling

## Source Files - Inspections (src/org/intellij/grammar/inspection/)
BnfResolveInspection.java | Unresolved references: detects undefined rules and tokens
BnfUnusedRuleInspection.java | Unused rules: finds unreachable and never-referenced rules
BnfLeftRecursionInspection.java | Left recursion: warns about unsupported direct left recursion

## Source Files - Utilities (src/org/intellij/grammar/)
LightPsi.java | Standalone parsing: API for testing and command-line parser usage
generator/RuleMethodsHelper.java | Rule methods: generates parser methods for rules
generator/ParserGeneratorUtil.java | Token consumption: fast/smart/default strategies, error recovery
psi/impl/BnfElementFactory.java | Element creation: programmatic BNF element construction API

## Bootstrap Files
antlr-based-bootstrap/peg/Grammar.g | ANTLR grammar: Grammar-Kit's bootstrap grammar for historical reference
