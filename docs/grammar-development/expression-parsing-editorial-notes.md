# Editorial Notes for Expression Parsing Documentation

## Missing from Documentation (Found in Evidence)

1. **Expression Marker Annotation**: The evidence mentions `BnfExpressionMarkerAnnotator` for IDE features, but this is not covered in the documentation.

2. **Expression Optimization Refactoring**: Evidence indicates there's an expression optimization refactoring feature in the IDE that's not documented.

3. **Convert Optional Expression Intention**: Evidence mentions this IDE feature but it's not in the documentation.

4. **Operator Types in Generated Parser**: Evidence specifies BINARY, PREFIX, POSTFIX, N_ARY operator types used in the generated parser, but these aren't explicitly mentioned.

5. **External and Meta Rules**: Evidence shows `external special_expr ::= meta_special_expr` pattern but documentation only briefly mentions it in examples without explanation.

6. **Methods Attribute Details**: Evidence shows `methods=[testExpr="expr[0]"]` but documentation doesn't explain what this does.

7. **Is-Not Expressions**: Evidence mentions `is_not_expr ::= expr IS NOT expr` pattern not covered in docs.

8. **consumeTokenFast Method**: Documentation mentions this but doesn't explain that it specifically skips operator nodes (as stated in evidence).

## Not in Evidence (Found in Documentation)

1. **"helping the parser optimize its internal state management"**: The documentation adds this explanation for `extraRoot` but evidence only says it "marks expression boundaries".

2. **"allowing maximum flexibility"**: Documentation adds subjective language about lambda expressions that's not in evidence.

3. **"natural method chaining"**: Documentation uses "natural" which is subjective and not in evidence.

## Technical Accuracy Issues

1. **consumeTokenMethod Description**: Documentation says it "optimizes token consumption" but evidence specifically states it "Skip[s] operator nodes" - the documentation should be more precise.

2. **Priority Table Location**: Documentation doesn't mention that the priority table appears in generated parser comments, which is specified in evidence.

## Style Improvements Made

- Removed redundant phrases and filler words
- Fixed "N-ary" capitalization consistency
- Added missing empty lines before lists
- Removed subjective adjectives ("natural", "maximum")
- Consolidated the "Next Steps" section into a single paragraph
- Fixed "vs" to "vs." for consistency
- Removed unnecessary explanations that weren't in evidence
- Made sentences more direct and concise