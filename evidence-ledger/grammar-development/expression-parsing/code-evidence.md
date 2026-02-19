# Code Evidence: Expression Parsing

## Scope Information
This evidence covers section 2.3: Expression Parsing

## Grammar Syntax
- Expression root rule: `expr ::= assign_expr | add_group | mul_group | primary_group`
- Left recursive operators: `left add_expr ::= plus_op factor`
- Binary operators: `plus_expr ::= expr '+' expr`
- N-ary operators: `exp_expr ::= expr ('**' expr) +`
- Postfix operators: `factorial_expr ::= expr '!'`
- Prefix operators: `unary_min_expr ::= '-' expr`
- Operator groups: `private add_group ::= plus_expr | minus_expr`
- Fake rules for PSI: `fake ref_expr ::= expr? '.' identifier`

## User-Configurable Attributes
- `extends(".*expr")=expr`: Flatten PSI tree structure
- `rightAssociative=true`: Right-to-left associativity
- `left`: Left recursive rule modifier
- `private`: Hide operators from PSI
- `extraRoot=true`: Mark expression root
- `elementType`: Override PSI element type
- `consumeTokenMethod`: Optimize token consumption

## IDE Features
- Expression marker annotation (BnfExpressionMarkerAnnotator)
- Expression optimization refactoring
- Convert optional expression intention
- Priority table in generated parser comments

## User-Visible Behavior
- Priority increases top to bottom in grammar
- Left recursion creates flat PSI trees
- Private rules group same-priority operators
- Extends attribute collapses redundant nodes
- N-ary syntax requires `(<op> expr) +` format
- Fake rules define PSI interface without parsing
- Expression root never appears in AST

## Example Locations
- `testData/generator/ExprParser.bnf`: Complete expression parser
- `testData/livePreview/LivePreviewTutorial.bnf`: Tutorial expression grammar
- `testData/generator/LeftAssociative.bnf`: Left associative examples
- `testData/fleet/FleetExprParser.bnf`: Fleet expression parser

## Expression Parsing Patterns
- Traditional precedence: Nested rule groups
- Layer-based approach: Private operator groups
- Mixed operators: `expr ::= prefix_group | infix_group | postfix_group`
- Ternary operator: `elvis_expr ::= expr '?' expr ':' expr`
- Function calls: `call_expr ::= ref_expr arg_list`
- Qualification: `qualification_expr ::= expr '.' identifier`
- Between operator: `between_expr ::= expr BETWEEN add_group AND add_group`

## Precedence Implementation
- Operator priority table generated in comments
- Priority-driven while loop in expr_0 method
- BINARY, PREFIX, POSTFIX, N_ARY operator types
- Lower priority number = higher precedence
- Same priority operators in private groups

## Associativity Control
- Default: Left associative (left-to-right)
- `rightAssociative=true`: Right-to-left parsing
- `left` modifier: Enable left recursion
- Mixed associativity in same expression tree

## PSI Tree Optimization
- `extends` attribute flattens hierarchy
- `elementType` reuses PSI types
- `fake` rules define interfaces only
- Private rules excluded from PSI
- `extraRoot` marks expression boundaries
- `consumeTokenMethod="consumeTokenFast"`: Skip operator nodes

## Complex Expression Features
- External rules: `external special_expr ::= meta_special_expr`
- Meta rules: `meta special_expr ::= 'multiply' '(' expr ',' expr ')'`
- Contextual methods: `methods=[testExpr="expr[0]"]`
- Is-not expressions: `is_not_expr ::= expr IS NOT expr`
- Argument lists: `arg_list ::= '(' [ !')' expr (',' expr) * ] ')'`

## Missing Documentation
- No docs for expression helper classes
- Priority calculation algorithm undocumented
- Expression info caching mechanism unclear
- Operator conflict resolution not documented