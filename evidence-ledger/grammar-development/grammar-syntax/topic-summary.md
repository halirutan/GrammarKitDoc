# Topic Summary: BNF Grammar Syntax

## Documentation Outline Reference
Section 2.1: BNF Grammar Syntax
Source: info/documentation-outline.md

## Learning Objectives
Based on outline and evidence:
- Understand the structure of BNF grammar files in Grammar-Kit
- Learn to write grammar rules using sequences, choices, and quantifiers
- Master token definitions including literal, named, and regexp tokens
- Apply rule modifiers for PSI generation control
- Recognize token precedence requirements for Live Preview

## Prerequisites
- Basic understanding of parsing concepts (helpful but optional)
- IntelliJ IDEA basics (from Section 1.1)
- Grammar-Kit plugin installed (from Section 1.2)
- Familiarity with regular expressions (for regexp tokens)

## Content Structure
Following documentation outline:
1. **Grammar structure** - Supported by code-evidence.md
   - Header attributes → Evidence: lines 9-20
   - Token definitions → Evidence: lines 84-92
   - Grammar rules → Evidence: lines 24-28
   - Rule modifiers → Evidence: lines 54-62

2. **Rule syntax** - Supported by examples.md
   - Sequences and choices → Examples: lines 70-93
   - Quantifiers (?, +, *) → Examples: lines 95-120
   - Grouping with parentheses → Examples: lines 122-143
   - Predicates (& and !) → Examples: lines 145-169

3. **Token types** - Supported by code-evidence.md and examples.md
   - Literal tokens (quoted strings) → Evidence: lines 66-70, Examples: lines 24-34
   - Named tokens → Evidence: lines 72-75, Examples: lines 24-34
   - Regexp tokens → Evidence: lines 77-81, Examples: lines 36-47
   - Token precedence in Live Preview → Evidence: lines 113-119

## Evidence Mapping
- Outline bullet "Header attributes" → Supported by code-evidence.md lines 15-20
- Outline bullet "Token definitions" → Supported by code-evidence.md lines 84-92, examples.md lines 22-68
- Outline bullet "Grammar rules" → Supported by code-evidence.md lines 24-28, examples.md lines 6-20
- Outline bullet "Rule modifiers" → Supported by code-evidence.md lines 54-62, examples.md lines 171-204
- Outline bullet "Sequences and choices" → Supported by code-evidence.md lines 30-35, examples.md lines 70-93
- Outline bullet "Quantifiers" → Supported by code-evidence.md lines 37-41, examples.md lines 95-120
- Outline bullet "Grouping with parentheses" → Supported by code-evidence.md lines 43-47, examples.md lines 122-143
- Outline bullet "Predicates" → Supported by code-evidence.md lines 49-53, examples.md lines 145-169
- Outline bullet "Literal tokens" → Supported by code-evidence.md lines 66-70, examples.md lines 24-34
- Outline bullet "Named tokens" → Supported by code-evidence.md lines 72-75
- Outline bullet "Regexp tokens" → Supported by code-evidence.md lines 77-81, examples.md lines 36-47
- Outline bullet "Token precedence" → Supported by code-evidence.md lines 113-119

## Key Takeaways
- BNF files have a clear structure: header attributes, token definitions, then grammar rules
- Grammar-Kit extends standard BNF with PEG-like features (predicates, quantifiers)
- Regexp tokens are required for Live Preview functionality
- Rule modifiers control PSI node generation and parsing behavior
- Token declaration order matters for precedence in Live Preview

## Documentation Notes
- Focus on syntax and structure only - no attribute details or Live Preview usage
- Include the basic grammar file structure example early (examples.md lines 6-20)
- Present quantifiers progressively: optional (?), then one-or-more (+), then zero-or-more (*)
- Address common mistakes with anti-patterns section (examples.md lines 226-257)
- Use `grammars/Grammar.bnf` as authoritative syntax reference
- Emphasize regexp token requirement for Live Preview without explaining Live Preview itself
- Keep examples minimal and focused on syntax demonstration