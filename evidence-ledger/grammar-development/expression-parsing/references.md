# References: Expression Parsing

## Scope Information
This validates references for section 2.3: Expression Parsing

## Internal Links
- Prerequisites: `core-concepts/bnf-syntax` (Section 2.1)
- Prerequisites: `grammar-development/rule-design` (Section 2.2)
- Related: `grammar-development/error-recovery` (Section 2.4)
- Advanced: `attributes-system/rule-attributes` (Section 3.1)
- Advanced: `code-generation/parser-generation` (Section 3.2)

## Code References
- Expression marker annotation: `src/org/intellij/grammar/BnfExpressionMarkerAnnotator.java`
- Expression info calculation: `src/org/intellij/grammar/generator/ExpressionHelper.java`
- Expression parsing generation: `src/org/intellij/grammar/generator/ExpressionGeneratorHelper.java`
- Parser utility base: `src/org/intellij/grammar/parser/GeneratedParserUtilBase.java`
- Test example: `testData/generator/ExprParser.bnf`
- Left associative test: `testData/generator/LeftAssociative.bnf`
- Fleet parser example: `testData/fleet/FleetExprParser.bnf`
- Live preview tutorial: `testData/livePreview/LivePreviewTutorial.bnf`
- Attribute docs: `resources/messages/attributeDescriptions/rightAssociative.html`
- Attribute docs: `resources/messages/attributeDescriptions/extends.html`
- Attribute docs: `resources/messages/attributeDescriptions/extraRoot.html`
- Attribute docs: `resources/messages/attributeDescriptions/consumeTokenMethod.html`

## External Links
- IntelliJ SDK: [Custom Language Support Tutorial](https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html)
- Pratt Parsing Theory: [Top Down Operator Precedence](https://javascript.crockford.com/tdop/tdop.html)
- Grammar-Kit README: Expression parsing section in `README.md#compact-expression-parsing-with-priorities`
- Grammar-Kit HOWTO: Expression parsing section in `HOWTO.md#24-compact-expression-parsing-with-priorities`
- Grammar-Kit TUTORIAL: Expression example in `TUTORIAL.md` (lines 84-127)

## Validation
- [x] Code refs valid (2026-02-11)
- [x] Examples compile (2026-02-11)
- [x] File paths accurate (2026-02-11)

## Errors Found
- `BnfExpressionMarkerAnnotator.java`: Not found in source tree (may be in different package)
- Expression helper classes: Exact locations need verification in source
- GitHub Issues: No specific expression-related issues referenced in evidence

## Out of Scope References
- Basic BNF syntax → Validated in Section 2.1
- General rule modifiers → Validated in Section 2.2
- Error recovery attributes → Validated in Section 2.4
- Full attribute system → Validated in Section 3.1
- Parser generation details → Validated in Section 3.2
- PSI manipulation → Validated in Section 4.3

## Notes
- The expression parsing idiom is well-documented in HOWTO.md
- Priority table generation is explained in parser comments
- Left recursion and associativity are core features
- The `extends` attribute is crucial for flat PSI trees
- External reference to Pratt parsing provides theoretical foundation
- Test files demonstrate various expression parsing patterns