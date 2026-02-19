# Topic Summary: Expression Parsing

## Documentation Outline Reference
Section 2.3: Expression Parsing
Source: info/documentation-outline.md (lines 208-242)

## Learning Objectives
Based on outline and evidence:
- Understand the difference between expression and statement parsing
- Learn to implement operator precedence using Grammar-Kit patterns
- Master associativity control for different operator types
- Apply expression optimization techniques for efficient PSI trees
- Build complex expression parsers with mixed operator types

## Prerequisites
- Basic BNF syntax (Section 2.1)
- Rule design principles (Section 2.2)
- Understanding of PSI tree structure
- Basic knowledge of operator precedence concepts

## Content Structure
Following documentation outline:

1. **Expression parsing fundamentals** - Supported by examples.md (lines 8-54)
   - Expression vs. statement parsing examples
   - Operator types with code samples
   - Precedence and associativity concepts from code-evidence.md
   - Expression grammar patterns from testData examples

2. **Implementing precedence** - Supported by examples.md (lines 56-126) and code-evidence.md (lines 55-61)
   - Traditional precedence climbing with deep nesting example
   - Layer-based approach using private groups
   - Priority attributes and generated tables
   - Operator precedence tables in parser comments

3. **Associativity control** - Supported by examples.md (lines 128-206) and code-evidence.md (lines 62-67)
   - Left associative operators (default behavior)
   - Right associative operators with attribute
   - Non-associative operators preventing chaining
   - Mixed associativity in single expression tree

4. **Expression optimization** - Supported by examples.md (lines 208-309) and code-evidence.md (lines 68-75)
   - Avoiding deep PSI trees comparison
   - Using extends for flat structure with examples
   - The expression parsing idiom pattern
   - Binary and n-ary operations syntax

5. **Complex expressions** - Supported by examples.md (lines 311-441) and code-evidence.md (lines 76-82)
   - Mixing operator types (prefix, infix, postfix)
   - Ternary operators implementation
   - Function calls and indexing patterns
   - Type constraints in expressions
   - Contextual expressions (lambda, let)

## Evidence Mapping
- Outline bullet "Expression vs. statement parsing" → examples.md lines 38-54
- Outline bullet "Operator types" → code-evidence.md lines 8-15, examples.md lines 311-340
- Outline bullet "Traditional precedence climbing" → examples.md lines 58-68
- Outline bullet "Layer-based approach" → examples.md lines 70-101
- Outline bullet "Priority attributes" → code-evidence.md lines 55-61, examples.md lines 103-126
- Outline bullet "Left associative operators" → examples.md lines 130-145
- Outline bullet "Right associative operators" → examples.md lines 147-159
- Outline bullet "Using extends for flat structure" → examples.md lines 230-256
- Outline bullet "The expression parsing idiom" → examples.md lines 258-288
- Outline bullet "Ternary operators" → examples.md lines 342-366
- Outline bullet "Function calls and indexing" → examples.md lines 368-389
- Missing outline item "Operator precedence tables" → Partially in code-evidence.md line 29

## Key Takeaways
- Grammar-Kit uses a priority-based approach where rules listed first have lower precedence
- The `extends` attribute is essential for creating flat, efficient PSI trees
- Left recursion with the `left` modifier creates optimal parsing for chains
- Private rule groups organize operators of the same precedence level
- The expression parsing idiom combines all optimizations into a standard pattern
- Different operator types (prefix, infix, postfix) can coexist in one grammar
- Associativity is controlled per-operator with the `rightAssociative` attribute

## Documentation Notes
- Focus on the practical "expression parsing idiom" pattern that users should adopt
- Include side-by-side comparisons of deep vs. flat PSI tree approaches
- Provide complete, runnable examples for each precedence implementation method
- Address common mistakes found in examples.md anti-patterns section (lines 486-555)
- Emphasize performance benefits of proper expression grammar design
- Include visual representation of operator precedence table if possible
- Reference the theoretical foundation (Pratt parsing) for interested readers
- Show real-world examples from ExprParser.bnf and FleetExprParser.bnf