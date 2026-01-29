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
